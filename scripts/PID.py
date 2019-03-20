#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
Created on Sun Mar 17 13:50:10 2019

@author: chenanyi
"""

from __future__ import division
from __future__ import absolute_import
import rospy
from std_msgs.msg import Float64
from ackermann_msgs.msg import AckermannDriveStamped

ErrorP = 0.0    
integral = 0.0
derivative = 0.0
Kp = 1.0
Ki = 0.0
Kd = -0.95

def callback(slope): 
    global integral,Error,ErrorP,derivative,Kp,Ki,Kd
    error = 30 , errorp =6
    current_slope = slope.data
    Error = current_slope 
    integral = integral + Error
    derivative = Error - ErrorP
    steering_angle =  (Kp * Error) + (Ki * integral) + (Kd * derivative)
 
    ads = AckermannDriveStamped()
#    ads.header.frame_id = '/map'
    ads.header.stamp = rospy.Time.now()
    ads.drive.steering_angle = steering_angle
    ads.drive.speed = 0.5
    pid_pub.publish(ads)
    
def listener():
    global pid_pub
    pub_topic = u'/vesc/high_level/ackermann_cmd_mux/input/nav_0'
    pid_pub = rospy.Publisher(pub_topic, AckermannDriveStamped, queue_size=1)
    rospy.init_node(u'pid_control',anonymous=True)
    rospy.Subscriber(u"slope_topic" ,Float64, callback)
    rospy.spin()
    
if __name__ == u'__main__':
    listener()