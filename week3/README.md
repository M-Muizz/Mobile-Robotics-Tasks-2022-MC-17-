# MCT-454L Mobile Robotics — Lab 3

[![ROS 2](https://img.shields.io/badge/ROS_2-Humble-blue.svg)](https://docs.ros.org/en/humble/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

## Description

This project is a ROS 2 Python package named `my_turtle_package` that controls a turtle in the `turtlesim` simulator. It demonstrates fundamental ROS 2 concepts including publishers, subscribers, services, and proportional control for basic robot navigation.

## Objectives

- Understand and perform ROS 2 workspace setup.
- Implement version control using GitHub.
- Create and configure a ROS 2 Python package.
- Program various turtle movement patterns (square, circle, triangle, multiple turtles, and proportional position control).

## Prerequisites

Before starting, ensure you have the following installed:

- **ROS 2** (Humble Hawksbill or your designated distribution)
- **Python 3**
- **turtlesim** package (`ros-<distro>-turtlesim`)
- **Git**

## Workspace Setup Instructions

Create a new ROS 2 workspace and `src` directory, build it, and source the environment:

```bash
# Create the workspace and src directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create the package (if not already cloned)
ros2 pkg create --build-type ament_python my_turtle_package

# Build the workspace
cd ~/ros2_ws
colcon build

# Source the setup script
source install/setup.bash
```

## GitHub Setup Instructions

To initialize version control and push to GitHub:

```bash
# Initialize a Git repository
git init

# Add files to staging
git add .

# Commit changes
git commit -m "Initial commit for Lab 3"

# Add your remote repository (replace URL with your actual GitHub repo)
git remote add origin https://github.com/your-username/your-repo-name.git

# Push to the main branch
git branch -M main
git push -u origin main
```

## Package Structure

```text
my_turtle_package/
├── my_turtle_package/
│   ├── __init__.py
│   ├── my_node.py
│   ├── circle_triangle.py
│   ├── spawn_turtles.py
│   └── goto_location.py
├── package.xml
├── setup.cfg
├── setup.py
└── resource/
    └── my_turtle_package
```

## How to Build and Run the Package

1. Navigate to your workspace root and build the package:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select my_turtle_package
   ```

2. Source the installation script:
   ```bash
   source install/setup.bash
   ```

3. Start the `turtlesim` node in a new terminal (remember to source ROS 2):
   ```bash
   ros2 run turtlesim turtlesim_node
   ```

4. Run any of the package nodes in your workspace terminal:
   ```bash
   ros2 run my_turtle_package my_node
   # or circle_triangle, spawn_turtles, goto_location
   ```

## Nodes Description

The package contains the following four nodes:

- **`my_node.py`**: Moves the turtle in a basic, square-like pattern using simple velocity commands.
- **`circle_triangle.py`**: Demonstrates compound movement by navigating the turtle in a circular path followed by a triangular path.
- **`spawn_turtles.py`**: Interacts with the `/spawn` service to create 3 additional turtles in the simulation, then publishes distinct velocity patterns to move each of them simultaneously.
- **`goto_location.py`**: Navigates the turtle to a specific `(x, y)` coordinate using a proportional control algorithm. It computes the distance and angle errors to update linear and angular velocities dynamically.

## ROS 2 Topics and Services Used

- **Topics**:
  - `/turtle1/cmd_vel`: Used to publish velocity commands (linear and angular) to move the turtle.
  - `/turtle1/pose`: Subscribed to receive the current `(x, y, theta)` position and orientation of the turtle.
- **Services**:
  - `/spawn`: Called to create new turtles in the simulation at specified coordinates.

## How to Change the Target Location in `goto_location.py`

To modify the target destination for the turtle in `goto_location.py`:

1. Open `my_turtle_package/goto_location.py` in your preferred text editor.
2. Locate the target coordinates variables in the initialization block (e.g., `self.target_x` and `self.target_y`).
3. Update the values to your desired location within the turtlesim grid (usually between `0.0` and `11.0`):
   ```python
   self.target_x = 8.5
   self.target_y = 8.5
   ```
4. Save the file, rebuild the workspace using `colcon build`, and run the node again.

## License

This project is licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).
