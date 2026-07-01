import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np
import time

class CameraFollower(Node):
    def __init__(self):
        super().__init__('camera_follower')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()

        self.kp               = 0.001   # smooth, no overshoot
        self.center_threshold = 50      # easier to satisfy
        self.current_state    = 'search'

        self.blue_spin_start    = None
        self.blue_spin_duration = 2.0   # seconds

        self.get_logger().info("Multi-Color Follower Started!")

    def get_largest_contour(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            return largest, cv2.contourArea(largest)
        return None, 0

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Image convert failed: {e}')
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # ── Masks ─────────────────────────────────────────────────────────────
        mask_green = cv2.inRange(hsv,
                        np.array([40, 100, 100]), np.array([80, 255, 255]))

        mask_blue  = cv2.inRange(hsv,
                        np.array([100, 150, 50]),  np.array([140, 255, 255]))

        mask_red   = cv2.bitwise_or(
                        cv2.inRange(hsv, np.array([0,   120,  70]),
                                         np.array([10,  255, 255])),
                        cv2.inRange(hsv, np.array([170, 120,  70]),
                                         np.array([180, 255, 255])))

        c_green, a_green = self.get_largest_contour(mask_green)
        c_blue,  a_blue  = self.get_largest_contour(mask_blue)
        c_red,   a_red   = self.get_largest_contour(mask_red)

        twist = Twist()
        now   = time.time()
        img_cx = frame.shape[1] // 2   # image center x

        # ════════════════════════════════════════════════════════════════════
        # STATE TRANSITIONS
        # ════════════════════════════════════════════════════════════════════
        if self.current_state == 'blue_spin':
            if now - self.blue_spin_start >= self.blue_spin_duration:
                self.get_logger().info("Blue spin done. Looking for next color.")
                self.current_state = 'search'
            # block all other transitions while spinning

        else:
            if a_blue > 500:
                self.current_state   = 'blue_spin'
                self.blue_spin_start = now
                self.get_logger().info("BLUE seen → spinning!")
            elif a_green > 500:
                self.current_state = 'green_track'
            elif a_red > 500:
                self.current_state = 'red_track'
            else:
                self.current_state = 'search'

        # ════════════════════════════════════════════════════════════════════
        # STATE ACTIONS
        # ════════════════════════════════════════════════════════════════════

        # ── 🔍 SEARCH: slowly rotate to find a color ─────────────────────────
        if self.current_state == 'search':
            twist.angular.z = 0.4
            twist.linear.x  = 0.0

        # ── 🔵 BLUE: spin fast for fixed duration ────────────────────────────
        elif self.current_state == 'blue_spin':
            twist.angular.z = 2.0
            twist.linear.x  = 0.0

        # ── 🟢 GREEN: align → move forward → stop when close ─────────────────
        elif self.current_state == 'green_track':
            if c_green is not None and a_green > 500:
                M = cv2.moments(c_green)
                if M["m00"] != 0:
                    cx    = int(M["m10"] / M["m00"])
                    cy    = int(M["m01"] / M["m00"])
                    error = cx - img_cx   # + = object right, - = object left

                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                    self.get_logger().info(
                        f"GREEN | error={error} area={a_green:.0f}")

                    # Step 1: Close enough → STOP
                    if a_green >= 200000:
                        twist.linear.x  = 0.0
                        twist.angular.z = 0.0
                        self.get_logger().info("GREEN: Reached target! STOPPED.")

                    # Step 2: Not aligned → rotate only, no forward motion
                    elif abs(error) > self.center_threshold:
                        twist.angular.z = -self.kp * error
                        twist.linear.x  =  0.0
                        self.get_logger().info(
                            f"GREEN: Aligning... error={error}")

                    # Step 3: Aligned and not close → move forward
                    else:
                        twist.linear.x  =  0.12
                        twist.angular.z = -self.kp * error  # gentle correction
                        self.get_logger().info(
                            f"GREEN: Moving forward... area={a_green:.0f}")
            else:
                self.current_state = 'search'

        # ── 🔴 RED: align → oscillate forward and backward ───────────────────
        elif self.current_state == 'red_track':
            if c_red is not None and a_red > 500:
                M = cv2.moments(c_red)
                if M["m00"] != 0:
                    cx    = int(M["m10"] / M["m00"])
                    cy    = int(M["m01"] / M["m00"])
                    error = cx - img_cx

                    cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                    self.get_logger().info(
                        f"RED | error={error} area={a_red:.0f}")

                    # Align first
                    if abs(error) > self.center_threshold:
                        twist.angular.z = -self.kp * error
                        twist.linear.x  =  0.0
                        self.get_logger().info(
                            f"RED: Aligning... error={error}")
                    else:
                        # Oscillate forward/backward every 2 seconds
                        if int(now) % 4 < 2:
                            twist.linear.x =  0.15
                            self.get_logger().info("RED: Moving FORWARD")
                        else:
                            twist.linear.x = -0.15
                            self.get_logger().info("RED: Moving BACKWARD")
                        twist.angular.z = 0.0
            else:
                self.current_state = 'search'

        self.publisher.publish(twist)

        # ── HUD overlay ───────────────────────────────────────────────────────
        color_map = {
            'search':      (200, 200, 200),
            'blue_spin':   (255, 100,   0),
            'green_track': (  0, 255,   0),
            'red_track':   (  0,   0, 255),
        }
        hud_color = color_map.get(self.current_state, (255, 255, 255))
        cv2.putText(frame, f"State: {self.current_state}",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, hud_color, 2)
        cv2.putText(frame,
                    f"G:{a_green:.0f}  B:{a_blue:.0f}  R:{a_red:.0f}",
                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow("Camera View", frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = CameraFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()