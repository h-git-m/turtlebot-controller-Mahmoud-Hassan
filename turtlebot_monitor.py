#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Cmd_Vel Subscriber Node
# ---------------------------------------------------------------------------
# What this code does:
# This script creates a ROS2 node that subscribes to the /cmd_vel topic,
# listens for incoming geometry_msgs/Twist messages, extracts the
# linear.x (forward/backward speed) and angular.z (rotation speed) values,
# and prints them to the terminal in a clear, readable format each time a
# new message is received.
# ---------------------------------------------------------------------------

# import rclpy, the ROS2 Python client library, needed to create and run a node
import rclpy
# import the Node base class that all ROS2 nodes are built from
from rclpy.node import Node
# import the Twist message type, which holds linear and angular velocity fields
from geometry_msgs.msg import Twist


# define the class that represents our subscriber node, inheriting from Node
class CmdVelSubscriber(Node):
    # constructor method, runs once when an instance of this class is created
    def __init__(self):
        # call the parent Node constructor and give this node the name 'cmd_vel_subscriber'
        super().__init__('cmd_vel_subscriber')
        # create a subscription to the '/cmd_vel' topic, using Twist messages, queue size 10
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.listener_callback, 10)
        # keep a reference to the subscription so Python's garbage collector doesn't remove it
        self.subscription

    # callback method that runs automatically every time a new Twist message arrives
    def listener_callback(self, msg):
        # extract the linear.x value (forward/backward speed) from the received message
        linear_x = msg.linear.x
        # extract the angular.z value (rotation speed) from the received message
        angular_z = msg.angular.z
        # print both values together in a clear, readable, formatted string
        print(f'Linear X (speed): {linear_x:.2f} m/s | Angular Z (rotation): {angular_z:.2f} rad/s')


# main function, the entry point that sets up and runs the ROS2 node
def main(args=None):
    # initialize the ROS2 Python client library
    rclpy.init(args=args)
    # create an instance of our CmdVelSubscriber node
    node = CmdVelSubscriber()
    # wrap the spin call in a try block so we can clean up properly on exit/Ctrl+C
    try:
        # keep the node alive and listening for incoming messages until interrupted
        rclpy.spin(node)
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
