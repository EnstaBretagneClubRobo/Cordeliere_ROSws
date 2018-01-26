#! /usr/bin/env python
# -*- coding: utf-8 -*-
# python version 2.7

"""
	--- Sounder Localization ---

Summary:
	Package containing the preprocessing of the Sounder location of the AUV, in the
	case that is underwater. The localization is given with interval analysis.

	Sounder           =>    sounder_localization    =>    location_estimator
		              |h                            |x
                                                    |y
		                                            |z
	Pressure_Meter    => 
                      |p

	                  => 
                      |map

I/O:
	input message : - std_msgs/Float64
					- std_msgs/Float64
					- map
	output message : geometry_msgs/Vector3


# TODO: 
- do it in C++

"""


import rospy
from std_msgs.msgs import Float64
from geometry_msgs.msg import Vector3
#from msgs_pkg.srv import gps_location


def listenerSounder(data):
	""" Listener function which gather Sounder data
	"""
	h = data
	rospy.loginfo("<Sounder>: altitude = %f", h)


def listenerPressure(data):
	""" Listener function which gather Pressure data
	"""
	p = data
	rospy.loginfo("<Pressure>: pressure = %f", p)


def evaluateDepth(p):
	""" Function that computes the depth of the AUV with the pressure
	"""
	global RHO, G
	z = 0  # TODO
	rospy.loginfo("<Depth>: z = %f", z)


if __name__ == '__main__':
	""" Main program
	"""

	## ------------- INITIALIZATION -------------

	rospy.init_node('sounder_localization', anonymous=True, log_level=rospy.DEBUG)
	# In ROS, nodes are uniquely named. If two nodes with the same
	# node are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.

	rate = rospy.Rate(10)  # frenquency in Hertz
	
	# Constants:
	G = 9.81
	RHO = 1  # kg/L

	# Publisher:
	pub = rospy.Publisher('sounder_position', Vector3, queue_size=10)
	
	# Subscribers:
	rospy.Subscriber("pressure", Float64, listenerPressure)
	rospy.Subscriber("sounder", Float64, listenerSounder)
	
	
	## ------------------ LOOP ------------------ 
	while not rospy.is_shutdown():

		z = evaluateDepth(p)

		# TODO: load the map and localize then write it into x and y

		pos_bat_msg = Vector3()

		x = 0
		y = 0
		z = 0

		pos_bat_msg.x = x
		pos_bat_msg.y = y
		pos_bat_msg.z = z

		pub.publish(pos_bat_msg)

		rate.sleep()
