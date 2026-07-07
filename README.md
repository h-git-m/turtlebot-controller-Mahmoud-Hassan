# turtlebot-controller-Mahmoud-Hassan


## 1. Step-by-Step Setup Instructions
1. Add the `turtlebot_controller` package to the `src` folder of your ROS2 workspace.
2. Open a terminal and navigate to your workspace root (e.g., from a nested folder, go back two levels).
3. Source your shell configuration to load ROS2 environment variables.
4. Build only the `turtlebot_controller` package.
5. Source the newly built workspace so ROS2 can find the package's executables.
6. Verify the package's executables are available.
7. In the 3D simulator, launch `turtlebot3_world.launch` to load the robot environment.
8. Run the keyboard controller publisher node to control the robot.
9. Use the keyboard to drive the robot (see Testing section below).
10. Open a new terminal and repeat steps 2, 3, and 5 to set up the environment there too.
11. Run the monitor node in the new terminal to observe published velocity commands.
12. Open a third terminal, source the environment, and run `rqt_graph` to visualize the running ROS2 nodes/topics.

## 2. Commands Used and What They Do
| Command | Description |
|---|---|
| `cd ../..` | Moves up two directory levels, back to the workspace root. |
| `source ~/.bashrc` | Reloads shell configuration, ensuring ROS2 environment variables are set. |
| `colcon build --packages-select turtlebot_controller` | Builds only the `turtlebot_controller` package instead of the whole workspace. |
| `source install/setup.bash` | Loads the newly built package into the current terminal's environment so ROS2 can find it. |
| `ros2 pkg executables turtlebot_controller` | Lists all runnable executables (nodes) inside the `turtlebot_controller` package. |
| `ros2 run turtlebot_controller A2_cmd_vel` | Runs the keyboard publisher node, which sends `Twist` messages to `/cmd_vel`. |
| `ros2 run turtlebot_controller A2_monitor` | Runs the subscriber node, which prints `Twist` messages received from `/cmd_vel`. |
| `ros2 run rqt_graph rqt_graph` | Opens a graphical tool showing active nodes and topic connections in the ROS2 system. |

## 3. How to Test the Nodes
1. Launch the simulator with `turtlebot3_world.launch` to load the robot.
2. In Terminal 1: run `ros2 run turtlebot_controller A2_cmd_vel` and use the keyboard:
   - `W` = move forward
   - `S` = move backward
   - `A` = rotate left
   - `D` = rotate right
   - `Q` = stop the robot and terminate the publisher node
3. In Terminal 2 (after sourcing the workspace again): run `ros2 run turtlebot_controller A2_monitor` to confirm the published velocity commands are being received correctly.
4. In Terminal 3 (after sourcing): run `ros2 run rqt_graph rqt_graph` to visually confirm `A2_cmd_vel` and `A2_monitor` are both connected to the `/cmd_vel` topic.
5. Watch the robot in the simulator to confirm its movement matches the key pressed.

A full demo of steps 8-11 (keyboard control + monitoring in Gazebo) is available here: [DEMO](A2_Demo.mov)

## 4. Expected Output
- **`ros2 pkg executables turtlebot_controller`** should list:
  ```
  turtlebot_controller A2_cmd_vel
  turtlebot_controller A2_monitor
  ```
- **`A2_cmd_vel` (publisher)**: prints the linear/angular velocity it publishes each time a valid key (W/A/S/D) is pressed, and stops/exits when `Q` is pressed.
- **`A2_monitor` (subscriber)**: prints each received `Twist` message's `linear.x` and `angular.z` values in a readable format, in real time as commands are published.
- **Simulator**: the Turtlebot moves forward/backward or rotates left/right in Gazebo, matching the key pressed, and stops when `Q` is pressed.
- **`rqt_graph`**: shows a graph with `A2_cmd_vel` and `A2_monitor` both connected to the `/cmd_vel` topic.
