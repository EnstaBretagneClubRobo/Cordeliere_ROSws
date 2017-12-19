#! /usr/bin/env python
# -*- coding: utf-8 -*-
# python version 2.7

"""
    --- IMU Localization ---

Summary:
    Package containing the preprocessing of the IMU location of the AUV.
    The preprocecessing contains a kalman filter.

    IMU    =>    imu_localization    =>    location_estimator
                                     <=    location_estimator
                                     <=    controller



I/O:
    input messages : - sensor_msgs/IMU.msg
                     - 
    output message : msgs_pkg/Inertial_location.msg


# TODO:

"""


import rospy
from msgs_pkg.msg import Command, State_vector
from sensor_msgs.msg import Imu


def callbackIMU(data):
    """ Callback function activated when a data is received from the IMU
    """
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # return data
    # TODO
    pass


def callbackEstimator(data):
    """ Callback function activated when a data is received from the IMU
    """
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # return data
    # TODO
    pass


def callbackController(data):
    """ Callback function activated when a data is received from the IMU
    """
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # return data
    # TODO
    pass


def listeners():
    """ Listener function which gather IMU data
    """
    # Gathering data from the IMU:
    rospy.Subscriber("IMU", Imu, callbackIMU)
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    # Gathering data from the Estimator:
    rospy.Subscriber("Estimator", State_vector, callbackEstimator)
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    # Gathering data from the Controller:
    rospy.Subscriber("Controller", Command, callbackController)
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def kalman_filter():
    """ Function that filter the position of the AUV through Kalman filter
    """
    # TODO
    pass


if __name__ == '__main__':
    """ Main program
    """

    # ------------- INITIALIZATION -------------

    rospy.init_node('imu_localization', anonymous=True)
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rate = rospy.Rate(10)  # frenquency in Hertz

    # Constants:


    # ------------------ LOOP ------------------

    while not rospy.is_shutdown():
        # Finding data:
        listeners()

        # Filtering:
        kalman_filter()

        rate.sleep()
