#! /usr/bin/env python
# -*- coding: utf-8 -*-
# python version 2.7

"""
	--- GPS Localization ---

Summary:
	Package containing the preprocessing of the GPS location of the AUV, in the
	case that is has surfaced. The preprocecessing contains a flatten code for
	the GPS coordinates.

	GPS    =>    gps_localization    =>    location_estimator
		  |Xgps                     |x
		  |Ygps                     |y
		  |Zgps                     |z


I/O:
	input message : nav_msgs/Odometry.msg
	output message : geometry_msgs/Vector3


# TODO: 
- gathering data from GPS simulator
- Sending properly data througth the service
- Saving X_INIT and Y_INIT
"""

import rospy
from nav_msgs.msg import Odometry


def callback(data):
	""" Callback function activated when a data is received from the GPS
	"""
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	return data


def listener():
	""" Listener function which gather GPS data
	"""
	rospy.Subscriber("GPS", Odometry, callback)


def flatten_gps(x_pos, y_pos, z_pos):
	""" Function that computes the flatten GPS position of the AUV
	"""
	global X_INIT, Y_INIT, EARTH_RADIUS
	x = EARTH_RADIUS*(y_pos - Y_INIT)*cos(X_INIT)
	y = EARTH_RADIUS*(x_pos - X_INIT)
	# rospy.loginfo()
	# return GpsLocationResponse
	return (x, y)


if __name__ == '__main__':
	""" Main program
	"""

	## ------------- INITIALIZATION -------------

	rospy.init_node('gps_localization', anonymous=True)
	# In ROS, nodes are uniquely named. If two nodes with the same
	# node are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.

	# Constants:
	EARTH_RADIUS = 6371000

	# Waits for the first GPS location to initialize the Reference,
	# by setting the X_INIT and Y_INIT
	# while ():  # TODO
	# 	X_INIT = # TODO
	# 	Y_INIT = # TODO


	## ------------------ LOOP ------------------ 
	while not rospy.is_shutdown():

		try:
			# s = rospy.Service('gps_position', GpsLocation, flatten_gps)
			print("GPS alive !")
		except rospy.ROSInterruptException:
			pass
