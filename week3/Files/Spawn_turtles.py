import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn

class SpawnAndMove(Node):
    def __init__(self):
        super().__init__('spawn_and_move')

        # Publishers for all 3 turtles
        self.pub1 = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.pub3 = self.create_publisher(Twist, 'turtle3/cmd_vel', 10)

        # Spawn client
        self.spawn_client = self.create_client(Spawn, '/spawn')

        # Wait for spawn service to be ready
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

        self.spawn_turtle('turtle2', 3.0, 3.0, 0.0)
        self.spawn_turtle('turtle3', 8.0, 8.0, 0.0)

        # Timer to move all turtles
        self.timer = self.create_timer(0.1, self.move_all)
        self.step = 0
        self.get_logger().info('All turtles spawned and moving!')

    def spawn_turtle(self, name, x, y, theta):
        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = theta
        req.name = name
        self.spawn_client.call_async(req)
        self.get_logger().info(f'Spawned {name} at ({x}, {y})')

    def move_all(self):
        # Turtle 1 — circle
        msg1 = Twist()
        msg1.linear.x = 1.0
        msg1.angular.z = 1.0
        self.pub1.publish(msg1)

        # Turtle 2 — straight line (forward only)
        msg2 = Twist()
        msg2.linear.x = 1.5
        msg2.angular.z = 0.0
        self.pub2.publish(msg2)

        # Turtle 3 — spin in place
        msg3 = Twist()
        msg3.linear.x = 0.0
        msg3.angular.z = 2.0
        self.pub3.publish(msg3)

def main(args=None):
    rclpy.init(args=args)
    node = SpawnAndMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()