import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_follower')
        
        self.leader_pose = None

        # Subscribe to turtle1's pose
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.leader_pose_callback,
            10
        )

        # Subscribe to turtle2's own pose
        self.follower_subscription = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self.follower_pose_callback,
            10
        )

        # Publish velocity commands to turtle2
        self.publisher = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        self.follower_pose = None
        self.timer = self.create_timer(0.1, self.follow)

    def leader_pose_callback(self, msg):
        self.leader_pose = msg

    def follower_pose_callback(self, msg):
        self.follower_pose = msg

    def follow(self):
        if self.leader_pose is None or self.follower_pose is None:
            return

        dx = self.leader_pose.x - self.follower_pose.x
        dy = self.leader_pose.y - self.follower_pose.y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_leader = math.atan2(dy, dx)
        angle_diff = angle_to_leader - self.follower_pose.theta

        # Normalize angle
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

        msg = Twist()
        if distance > 0.5:  # Only move if not too close
            msg.linear.x = min(1.5 * distance, 2.0)
            msg.angular.z = 4.0 * angle_diff
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()