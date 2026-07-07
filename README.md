# turtlebot-controller-Mahmoud-Hassan


https://github.com/user-attachments/assets/b9d1bcbe-43f1-4135-a6f1-5ebac707b153

1- Add "turtlebot_controller" package to your src folder in your worksapce

2- In your terminal, move to the workspace directory ex: $ cd ../.. (this will move back twice inside folders)

3- $ source ~/.bashrc

4- Build only the package you developed $ colcon build --packages-select turtlebot_controller

5- $ source install/setup.bash

6- To check executables for this package, type: $ ros2 pkg executables turtlebot_controller 

You should see: 

turtlebot_controller A2_cmd_vel (publishes Twist messages to /cmd_vel topic)
turtlebot_controller A2_monitor (subscribes to Twist messages on /cmd_vel topic)

7- In the 3D simulator, select turtlebot3_world.launch to observe the robot response when it receives command via the developed keyboard controller publisher.

8- To start keyboard controller for turtlebot, type $ ros2 run turtlebot_controller A2_cmd_vel 

9- press w move forward s move backward A rotate left D rotate right Q to stop turtlebot and terminate keyboard controller 

10- open a new terminal and repeat step #2, #3 and #5

11- to start monitoring turtle bot movements, type $ ros2 run turtlebot_controller A2_monitor

12- to create a dynamic graphical map of your ROS 2 system, open another terminal repeat step #3, then type: $ ros2 run rqt_graph rqt_graph
