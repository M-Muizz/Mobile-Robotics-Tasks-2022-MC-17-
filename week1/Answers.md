# Week 1 Lab Answers

**1. Define: node, topic, package, workspace.**
- **Node:** A process that performs a specific computation or task within the ROS 2 graph.
- **Topic:** A named bus over which nodes exchange messages using a publish-subscribe model.
- **Package:** The fundamental organizational unit in ROS 2 used to bundle code, data, and build files.
- **Workspace:** A directory structure containing a set of ROS 2 packages and their build artifacts.

**2. Explain why sourcing is required. What happens if you do not source a workspace?**
Sourcing is required to update environment variables (like PATH and PYTHONPATH) so the shell can find ROS 2 commands and your custom packages. If you do not source, the terminal will return "command not found" or "package not found" errors.

**3. What is the purpose of colcon build? What folders does it generate?**
The purpose of `colcon build` is to compile source code and install it into a usable format. It generates the `build/` (intermediate files), `install/` (executables and setup scripts), and `log/` (build history) folders.

**4. In your own words, explain what the entry_points console script does in setup.py.**
The `entry_points` script acts as a registration tool that tells ROS 2 which Python function to execute when a specific command is typed into the terminal using `ros2 run`.

**5. Diagram of a Publisher and Subscriber connected by a topic.**
```text
[ Node: /talker ] --- ( Publish ) ---> [ Topic: /chat ] --- ( Subscribe ) ---> [ Node: /listener ]
```
