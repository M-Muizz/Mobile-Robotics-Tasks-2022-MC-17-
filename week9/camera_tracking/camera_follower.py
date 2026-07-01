import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

from cv_bridge import CvBridge

import cv2
import numpy as np


class CameraFollower(Node):

    def __init__(self):
        super().__init__('camera_follower')

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.bridge = CvBridge()

        # Proportional gain
        self.kp = 0.002

        # Allowed center error
        self.center_threshold = 30

    def image_callback(self, msg):

        # Convert ROS image to OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Detect RED color
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)

        twist = Twist()

        if contours:

            # Largest contour
            largest_contour = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(largest_contour)

            if area > 500:

                M = cv2.moments(largest_contour)

                if M["m00"] != 0:

                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Draw centroid
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                    image_center_x = frame.shape[1] // 2

                    error = image_center_x - cx

                    # Proportional controller
                    twist.angular.z = self.kp * error

                    # Move forward if centered
                    if abs(error) < self.center_threshold:
                        twist.linear.x = 0.1
                    else:
                        twist.linear.x = 0.0

                    self.publisher.publish(twist)

        else:
            # Stop robot if no object detected
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.publisher.publish(twist)

        # Show camera
        cv2.imshow("Camera View", frame)

        # Show mask
        cv2.imshow("Mask", mask)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = CameraFollower()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
