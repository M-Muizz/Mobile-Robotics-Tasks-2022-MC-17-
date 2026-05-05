# Lab 7: Autonomous Navigation with Nav2 and Multi-Waypoint Mission Planning

## Objective
The goal of this lab was to implement autonomous navigation for a mobile robot using the ROS 2 Nav2 stack. By integrating Adaptive Monte Carlo Localization (AMCL) with a previously saved static map, the robot was tasked with determining its global pose and autonomously navigating to designated goal poses while avoiding obstacles. 

## Core Components
The navigation stack relies on several interconnected servers to perform reliable autonomous movement. The key Nav2 components utilized in this lab include:
*   **Map Server:** Loads and provides the static map (generated during previous SLAM exercises) to the rest of the navigation stack.
*   **AMCL (Adaptive Monte Carlo Localization):** Uses a particle filter to track the robot's pose against the known map, updating based on odometry and laser scan data.
*   **Planner (Global Planner):** Computes the optimal, obstacle-free path from the robot's current pose to the goal pose based on the global costmap.
*   **Controller (Local Planner):** Generates the necessary velocity commands to safely follow the global plan while reacting to dynamic obstacles using the local costmap.
*   **BT Navigator (Behavior Tree Navigator):** Acts as the high-level orchestrator, coordinating the planner, controller, and recovery behaviors using behavior trees to execute complex navigation tasks.

## Tasks Completed
Throughout this lab, the following key milestones were successfully achieved:
*   **Single-Goal Navigation:** Initialized the robot's pose in RViz and successfully commanded it to navigate to a single goal using the 2D Goal Pose tool, validating the basic Nav2 setup.
*   **Multi-Waypoint Mission Planning:** Developed a custom Python node (`waypoint_navigator.py`) using the `nav2_simple_commander` API. This script successfully guided the robot through a predefined sequence of waypoints, demonstrating automated mission execution.
*   **Costmap Observations:** Analyzed both global and local costmaps in RViz. Observed how static obstacles are factored into the global path, and how the local costmap dynamically expands to account for the robot's footprint and sensor ranges.
*   **Recovery Behaviors:** Tested the system's robustness by intentionally blocking paths. Observed the Nav2 stack automatically triggering recovery behaviors (such as spinning or backing up) to clear the costmap and find alternative routes.

## Conclusion
Comparing this lab's navigation workflow to the SLAM workflow from Lab 5 highlights a shift from exploration to exploitation. In SLAM, the primary objective was unknown environment mapping, where the robot built its understanding of the world dynamically. In contrast, this navigation lab assumed a known, static map. The focus shifted entirely to localization (via AMCL) and path planning, allowing for precise, goal-oriented autonomy rather than map generation.
