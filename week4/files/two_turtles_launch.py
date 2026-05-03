from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='turtlesim',
            executable='turtle_teleop_key',
            name='teleop'
        ),
        # Spawn a second turtle via service call after launch
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn',
                 'turtlesim/srv/Spawn',
                 '{x: 3.0, y: 3.0, theta: 0.0, name: "turtle2"}'],
            output='screen'
        )
    ])