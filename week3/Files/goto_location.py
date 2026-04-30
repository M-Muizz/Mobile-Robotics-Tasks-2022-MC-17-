import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# ---- Set your target position here ----
TARGET_X = 8.0
TARGET_Y = 8.0
# ----------------------------------------

class GoToLocation(Node):
    def __init__(self):
        super().__init__('goto_location')

        self.publisher_ = self.create_publisher(
            Twist, 'turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose, 'turtle1/pose', self.pose_callback, 10)

        self.current_pose = None
        self.reached = False
        self.get_logger().info(
            f'Navigating to ({TARGET_X}, {TARGET_Y})...')

    def pose_callback(self, pose):
        self.current_pose = pose

        if self.reached:
            return

        # Distance to target
        dist = math.sqrt(
            (TARGET_X - pose.x) ** 2 +
            (TARGET_Y - pose.y) ** 2
        )

        # Angle to target
        angle_to_target = math.atan2(
            TARGET_Y - pose.y,
            TARGET_X - pose.x
        )

        # Angle error (how much we need to turn)
        angle_error = angle_to_target - pose.theta

        # Normalize angle to [-pi, pi]
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        msg = Twist()

        if dist > 0.2:  # Not yet at target
            # Proportional control gains
            msg.linear.x = min(1.5 * dist, 2.0)   # speed up when far
            msg.angular.z = 4.0 * angle_error      # turn toward target
        else:
            # Reached target — stop
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.reached = True
            self.get_logger().info('Target reached!')

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GoToLocation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()