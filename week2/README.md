Report
1. Objective
The primary goals of this lab were to gain familiarity with the ROS 2 command-line interface (CLI), understand the operation of the Turtlesim simulator, and learn to control a robot using ROS 2 topics and services.  
2. Methodology and Steps Followed 
The following steps were executed to complete the lab:  
    Environment Setup: The ROS 2 Humble environment was sourced, and the turtlesim package was verified and installed.  
Simulation Launch: The turtlesim_node was launched to open the simulator window.  
Teleoperation: A turtle_teleop_key node was initiated in a separate terminal to move the turtle via keyboard inputs.  

Topic Exploration: Active topics were listed using ros2 topic list, and the turtle's live coordinates were monitored using ros2 topic echo /turtle1/pose.  

CLI Commands: Velocity commands were sent directly to the turtle via the ros2 topic pub command, and the simulation was cleared using a ros2 service call /reset.  

rqt Integration: The rqt GUI was utilized to explore the ROS graph and call services.  

Multi-Robot Control: The /spawn service was called within rqt to create a second turtle (turtle2), which was then controlled independently by publishing to the /turtle2/cmd_vel topic.  
3. Observations   

    Node Communication: Upon launching the simulator node, a blue background with a centered turtle appeared as expected.  

Real-time Data: Echoing the /pose topic provided a continuous stream of X, Y, and Theta values that changed instantly whenever the turtle moved.  

Command Response: The turtle responded accurately to manual Twist messages, performing circular motions when both linear and angular velocities were applied.  

Service Impact: Calling the /reset service successfully returned the turtle to its original starting coordinates and cleared all existing paths from the screen.  

Independent Behavior: After using the /spawn service, the second turtle appeared at the designated coordinates and moved independently of the first turtle when its specific velocity topic was addressed.  

4. Conclusion
The lab successfully demonstrated the core concepts of the ROS 2 ecosystem. By interacting with nodes, topics, and services through both the CLI and the rqt GUI, a fundamental understanding of simulated robotic control and inter-process communication was established.