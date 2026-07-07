#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Keyboard Teleop Publisher Node
# ---------------------------------------------------------------------------
# What this code does:
# This script creates a ROS2 node that reads single key presses (W, A, S, D)
# from the terminal without requiring the user to press Enter, and converts
# those key presses into geometry_msgs/Twist messages published on the
# /cmd_vel topic. Only linear.x (forward/backward speed) and angular.z
# (rotation speed) are used, since this is meant for a simple differential
# drive-style robot.
#   W -> move forward   (linear.x = +step, held for 3 seconds, then zero)
#   S -> move backward  (linear.x = -step, held for 3 seconds, then zero)
#   A -> turn left       (angular.z = +step, held for 3 seconds, then zero)
#   D -> turn right      (angular.z = -step, held for 3 seconds, then zero)
#   Q -> stop movement and shut down the node
#
# Each key press sets a FIXED velocity value (it does not accumulate). That
# velocity is published, held for exactly 3 seconds using a background timer,
# and then automatically reset to zero. Pressing a new key before the 3
# seconds elapse cancels the pending zero and restarts the 3-second hold.
# ---------------------------------------------------------------------------

# import rclpy, the ROS2 Python client library, needed to create and run a node
import rclpy
# import the Node base class that all ROS2 nodes are built from
from rclpy.node import Node
# import the Twist message type, which holds linear and angular velocity fields
from geometry_msgs.msg import Twist
# import sys, used to read raw terminal settings and exit the program cleanly
import sys
# import termios, used on Linux to change terminal input mode (no Enter needed)
import termios
# import tty, used to switch the terminal into raw/cbreak mode for single-key reads
import tty
# import threading, used to run a background timer that auto-zeroes velocity after 3 seconds
import threading


# define the class that represents our publisher node, inheriting from Node
class KeyboardTeleopPublisher(Node):
    # constructor method, runs once when an instance of this class is created
    def __init__(self):
        # call the parent Node constructor and give this node the name 'keyboard_teleop_publisher'
        super().__init__('keyboard_teleop_publisher')
        # create a publisher that sends Twist messages to the '/cmd_vel' topic, with a queue size of 10
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        # store the current linear speed (forward/backward), starting at 0.0
        self.linear_speed = 0.0
        # store the current angular speed (rotation), starting at 0.0
        self.angular_speed = 0.0
        # define the fixed speed value to use for linear movement (no accumulation)
        self.linear_step = 0.35
        # define the fixed speed value to use for angular movement (no accumulation)
        self.angular_step = 0.35
        # define how long (in seconds) a commanded velocity is held before auto-zeroing
        self.hold_duration = 2.0
        # keep a reference to the active auto-stop timer so it can be cancelled/replaced
        self.stop_timer = None
        # log a startup message so the user knows the node is ready and which keys to use
        self.get_logger().info('Use W/A/S/D to move, Q to stop and quit.')

    # method that sets a fixed velocity, publishes it, and schedules an auto-stop after 3 seconds
    def set_velocity(self, linear_x, angular_z):
        # cancel any previously scheduled auto-stop timer so it doesn't fire early or overlap
        if self.stop_timer is not None:
            # stop the existing timer thread before starting a new hold period
            self.stop_timer.cancel()
        # set the current linear speed to the fixed value passed in (no accumulation)
        self.linear_speed = linear_x
        # set the current angular speed to the fixed value passed in (no accumulation)
        self.angular_speed = angular_z
        # publish the newly set velocity immediately so the robot starts moving
        self.publish_velocity()
        # create a new timer that will call stop_robot after hold_duration seconds
        self.stop_timer = threading.Timer(self.hold_duration, self.stop_robot)
        # mark the timer as a daemon thread so it won't block program shutdown
        self.stop_timer.daemon = True
        # start the timer so the countdown to auto-zero begins now
        self.stop_timer.start()

    # method that publishes the current linear and angular speeds as a Twist message
    def publish_velocity(self):
        # create a new empty Twist message object
        msg = Twist()
        # set the message's linear.x field to the current linear speed
        msg.linear.x = self.linear_speed
        # set the message's angular.z field to the current angular speed
        msg.angular.z = self.angular_speed
        # publish the constructed Twist message on the /cmd_vel topic
        self.publisher_.publish(msg)
        # log the values that were just published, for user feedback in the terminal
        self.get_logger().info(f'Published -> linear.x: {self.linear_speed:.2f}, angular.z: {self.angular_speed:.2f}')

    # method that immediately zeroes out both speeds and publishes a stop command
    def stop_robot(self):
        # cancel any pending auto-stop timer since we are stopping right now anyway
        if self.stop_timer is not None:
            # stop the timer thread to avoid a redundant stop_robot call later
            self.stop_timer.cancel()
        # reset linear speed to zero so the robot stops moving forward/backward
        self.linear_speed = 0.0
        # reset angular speed to zero so the robot stops rotating
        self.angular_speed = 0.0
        # publish the zeroed Twist message so the robot actually receives the stop command
        self.publish_velocity()


# function that reads a single raw keypress from the terminal without waiting for Enter
def get_key():
    # save the current terminal file descriptor settings so they can be restored later
    fd = sys.stdin.fileno()
    # store the original terminal settings in a variable for restoration after reading
    old_settings = termios.tcgetattr(fd)
    # use a try block so the terminal settings are always restored, even on error
    try:
        # switch the terminal into raw mode so single key presses are read instantly
        tty.setraw(fd)
        # read exactly one character from standard input (the key that was pressed)
        key = sys.stdin.read(1)
    # finally block guarantees terminal settings are restored no matter what happens above
    finally:
        # restore the terminal to its original (cooked) settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    # return the character that was read so the caller can process it
    return key


# main function, the entry point that sets up and runs the ROS2 node
def main(args=None):
    # initialize the ROS2 Python client library
    rclpy.init(args=args)
    # create an instance of our KeyboardTeleopPublisher node
    node = KeyboardTeleopPublisher()
    # wrap the main loop in a try block so we can clean up properly on exit/Ctrl+C
    try:
        # start an infinite loop to continuously read keys until the user quits
        while True:
            # read a single key press from the terminal
            key = get_key()
            # convert the key to lowercase so both 'w' and 'W' work the same way
            key = key.lower()
            # check if the 'q' key was pressed, meaning the user wants to quit
            if key == 'q':
                # log that the node is stopping the robot and shutting down
                node.get_logger().info('Q pressed. Stopping robot and shutting down node.')
                # call stop_robot to zero out and publish a final stop command
                node.stop_robot()
                # break out of the while loop to proceed to shutdown
                break
            # check if the 'w' key was pressed, meaning move forward
            elif key == 'w':
                # set a fixed forward velocity, publish it, and start the 3-second hold timer
                node.set_velocity(node.linear_step, 0.0)
            # check if the 's' key was pressed, meaning move backward
            elif key == 's':
                # set a fixed backward velocity, publish it, and start the 3-second hold timer
                node.set_velocity(-node.linear_step, 0.0)
            # check if the 'a' key was pressed, meaning turn left
            elif key == 'a':
                # set a fixed left-turn velocity, publish it, and start the 3-second hold timer
                node.set_velocity(0.0, node.angular_step)
            # check if the 'd' key was pressed, meaning turn right
            elif key == 'd':
                # set a fixed right-turn velocity, publish it, and start the 3-second hold timer
                node.set_velocity(0.0, -node.angular_step)
            # if any other key was pressed, ignore it and continue the loop
            else:
                # skip processing and wait for the next key press
                continue
    # catch Ctrl+C (KeyboardInterrupt) so the program can shut down gracefully
    except KeyboardInterrupt:
        # log that the node was interrupted manually by the user
        node.get_logger().info('Keyboard interrupt received. Shutting down.')
    # finally block ensures cleanup always happens, whether we quit normally or via Ctrl+C
    finally:
        # destroy the node explicitly to free up resources
        node.destroy_node()
        # shut down the ROS2 Python client library cleanly
        rclpy.shutdown()


# standard Python entry point check, so main() only runs when this file is executed directly
if __name__ == '__main__':
    # call the main function to start the node
    main()
