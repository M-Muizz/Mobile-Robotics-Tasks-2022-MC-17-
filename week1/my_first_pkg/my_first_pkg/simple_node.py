import rclpy
from rclpy.node import Node
import os

class SimpleNode(Node):
    def __init__(self):
        super().__init__('simple_node')
        
        # --- Task 3: Print name using a ROS parameter ---
        self.declare_parameter('student_name', 'student_name not set')
        student_name = self.get_parameter('student_name').get_parameter_value().string_value
        
        if student_name == 'student_name not set':
            self.get_logger().info('student_name not set')
        else:
            self.get_logger().info(f'Student Name: {student_name}')
            
        # --- Task 1: Customize the log message ---
        self.get_logger().info('Welcome to Mobile Robotics Lab')

        # --- Task 2: Add a counter ---
        counter_file = 'run_counter.txt'
        count = 1
        
        # Read the file if it exists
        if os.path.exists(counter_file):
            with open(counter_file, 'r') as f:
                content = f.read().strip()
                if content.isdigit():
                    count = int(content) + 1
                    
        # Write the updated count back to the file
        with open(counter_file, 'w') as f:
            f.write(str(count))
            
        self.get_logger().info(f'Run count: {count}')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    # spin_once lets us create the node, log once, and exit cleanly
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()