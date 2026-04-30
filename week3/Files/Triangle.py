import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TrianglePattern(Node):
    def __init__(self):
        super().__init__('triangle_pattern')
        self.publisher_ = self.create_publisher(
            Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.step = 0
        self.get_logger().info('Moving in a triangle...')

    def timer_callback(self):
        msg = Twist()
        phase = self.step % 2  # alternates: 0=forward, 1=turn

        if phase == 0:
            # Move forward along one side
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            time.sleep(2)
        else:
            # Turn 120 degrees (exterior angle of equilateral triangle)
            msg.linear.x = 0.0
            msg.angular.z = 2.09  # ~120 degrees in radians
            self.publisher_.publish(msg)
            time.sleep(1)

        self.step += 1

def main(args=None):
    rclpy.init(args=args)
    node = TrianglePattern()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()