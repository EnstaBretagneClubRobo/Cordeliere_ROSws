#! /usr/bin/env python
# -*- coding: utf-8 -*-
# python version 2.7

"""
    --- Logger ---

Summary:

I/O:

# TODO:
- Use the unity
"""

import rospy
from msgs_pkg.msg import State_vector


def callbackState(data):
    """ Callback function activated when a data is received from the IMU
    """
    global x, y, z, roll, pitch, yaw
    x = data.state.linear.x
    y = data.state.linear.y
    z = data.state.linear.z

    roll = data.state.angular.x
    pitch = data.state.angular.y
    yaw = data.state.angular.z



if __name__ == '__main__':
    """ Main program
    """

    # ------------- INITIALIZATION -------------

    rospy.init_node('logger', anonymous=True)
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rate = rospy.Rate(10)  # frenquency in Hertz

    # Initialization:
    x = 0
    y = 0
    z = 0
    roll = 0
    pitch = 0
    yaw = 0

    # Subscribers:
    rospy.Subscriber("state_msg", State_vector, callbackState)

    # ------------------ LOOP ------------------

    while not rospy.is_shutdown():

        # Sending data to Unity:
        # TODO

        rate.sleep()
