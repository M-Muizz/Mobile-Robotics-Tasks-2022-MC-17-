import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CirclePattern(Node):
    def __init__(self):
        super().__init__('circle_pattern')
        self.publisher_ = self.create_publisher(
            Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Moving in a circle...')

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0   # forward speed
        msg.angular.z = 1.0  # turning speed — both non-zero = circle
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CirclePattern()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()