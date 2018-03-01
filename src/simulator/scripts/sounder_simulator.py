#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import math
from quadtree import Point, Quadtree
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64


def recupere_pos(msg):
    pos = Point((msg.position.x, msg.position.y))
    points = qtree.rech_autour(pos, dist_caract)

    dist_min = 999
    point_plus_proche = points[0]
    for p in points:
        dist = math.sqrt((pos.x-p.x)**2 + (pos.y-p.y)**2)
        if dist < dist_min:
            point_plus_proche = p
            dist = dist_min
    pub.publish(Float64(point_plus_proche.donnees))

# Récupération des points du mesh et importation dans un quadtree
print("Loading map...")
xmin, xmax, ymin, ymax = 999, -999, 999, -999
points = []
with open(os.path.join(os.pardir, "mesh", "world2.xyz"), 'r') as f:
    for coord in f:
        x, y, z = coord.split()
        x, y, z = float(x), float(y), float(z)
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

        p = Point((x, y), donnees=z)
        points.append(p)

qtree = Quadtree([xmin, xmax, ymin, ymax])
for p in points:
    qtree.insert(p)

dist_caract = math.sqrt((xmax-xmin) * (ymax-ymin) / (4**(qtree.hauteur()-2)))

print("Map loaded")


# Initialisation ROS
rospy.init_node('sounder_simulation')


sub = rospy.Subscriber("simulated_pos", Pose, recupere_pos)
pub = rospy.Publisher("distance_to_depth", Float64, queue_size=1)
rospy.spin()

