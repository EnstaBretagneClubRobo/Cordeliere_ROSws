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
from math import cos, radians
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
#from msgs_pkg.srv import gps_location


def listener(data):
	""" Listener function which gather GPS data
	"""
	x_pos = data.position.x
	y_pos = data.position.y
	z_pos = data.position.z
	rospy.loginfo("<gps>: x = %f | y = %f | z = %f",x, y, z)


def flatten_gps(x_pos, y_pos, z_pos):
	""" Function that computes the flatten GPS position of the AUV
	"""
	global X_INIT, Y_INIT, EARTH_RADIUS, pos_GPS
	x = EARTH_RADIUS*(y_pos - Y_INIT)*cos(radians(X_INIT))
	y = EARTH_RADIUS*(x_pos - X_INIT)
	pos_GPS.x = x
	pos_GPS.y = y
	pos_GPS.z = 0.0
	rospy.loginfo("<gps_location>: x = %f | y = %f",x ,y)


if __name__ == '__main__':
	""" Main program
	"""

	## ------------- INITIALIZATION -------------

	rospy.init_node('gps_localization', anonymous=True, log_level=rospy.DEBUG)
	# In ROS, nodes are uniquely named. If two nodes with the same
	# node are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.

	rate = rospy.Rate(10)  # frenquency in Hertz

	# Server:
	pub = rospy.Publisher('gps_position', Point, queue_size=10)


	# Constants:
	EARTH_RADIUS = 6371000

	# Waits for the first GPS location to initialize the Reference,
	# by setting the X_INIT and Y_INIT
	# while ():  # TODO
	# 	X_INIT = # TODO
	# 	Y_INIT = # TODO
	X_INIT = 0
	Y_INIT = 0
	EARTH_RADIUS = 6371000
	x_pos = 1
	y_pos = 2
	z_pos = 0
	pos_GPS = Point()
	

	## ------------------ LOOP ------------------ 
	while not rospy.is_shutdown():

		rospy.Subscriber("gps", Odometry, listener)

		flatten_gps(x_pos, y_pos, z_pos)
		pub.publish(pos_GPS)

		rate.sleep()
