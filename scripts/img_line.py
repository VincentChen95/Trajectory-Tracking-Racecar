#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
Created on Sun Mar 17 13:50:10 2019

@author: chenanyi
"""

from __future__ import division
from __future__ import absolute_import
import cv2
import numpy as np
import math
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
bridge = CvBridge()

def convert_image(image,cvt_type):
    if cvt_type == u'HSV':
        return cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
    elif cvt_type==u'HSL':
        return cv2.cvtColor(image,cv2.COLOR_RGB2HLS)

def select_line_color(image):
    cvt_image=convert_image(image,u'HSL')
    # yellow mask
    yellow_lower = np.uint8([10,0,100]) # h l s
    yellow_upper = np.uint8([40,255,255]) 
    yellow_mask = cv2.inRange(cvt_image,yellow_lower,yellow_upper)
    # white mask
    white_lower = np.array([0,200,0])
    white_upper = np.array([255,255,255])
    white_mask = cv2.inRange(cvt_image,white_lower,white_upper)
    # combine mask
    mask = cv2.bitwise_or(yellow_mask,white_mask)
    return cv2.bitwise_and(image,image,mask=mask)

def grayscale(img):
    u"""Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size):
    u"""Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
    u"""Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    u"""
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines_improved(img, lines, color=[255, 0, 0], thickness=10):
    line_ = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            if x2 != x1:
                slope = float(y2-y1)/float(x2-x1)
                intercept = y1-slope*x1
                length = np.sqrt((y2-y1)**2+(x2-x1)**2)
                line_.append([slope,intercept,length]) 
    if len(line_):
        line_ = np.array(line_)
        line_weight = line_[:,2]/np.sum(line_[:,2]) # weighted average using line length as weight
        _avg_slope = np.sum(line_[:,0]*line_weight) # slope
        if -0.0001 <= _avg_slope <= 0.0001:
            _avg_slope = 0.0001
        elif _avg_slope <= -10000:
            _avg_slope = -10000
        elif _avg_slope >= 10000:
            _avg_slope = 10000
        avg_intercept = np.sum(line_[:,1]*line_weight) # intercept
        _y1 = img.shape[0]
        _x1 = int((img.shape[0] - avg_intercept)/_avg_slope)
        _y2 = int(img.shape[0]*0.7) # only draw 60%
        _x2 = int((_y2 - avg_intercept)/_avg_slope)
        theta = math.degrees(math.atan(_avg_slope))
        # offset
        theta += 15.
        theta = abs(90-theta)
        if theta <= 6:
            theta = 0
        cv2.putText(img, str(round(theta,2)), (_x2, _y2), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)        
        cv2.line(img, (_x1, _y1), (_x2, _y2), color, thickness)

def callback(data):
    cv_image = bridge.imgmsg_to_cv2(data,'bgr8')
    img_color_select = select_line_color(cv_image)
    img_gray = grayscale(img_color_select)
    img_blur = gaussian_blur(img_gray, 15)
    img_edge = canny(img_blur, low_threshold=50, high_threshold=150)
    rows, cols = img_edge.shape[:2]
#    vertices = np.array([[[cols*0.1, rows*0.95],[cols*0.1, rows*0.1],[cols*0.95, rows*0.95],[cols*0.95, rows*0.1]]],dtype=np.int32)
    vertices = np.array([[[cols*0.1, rows*0.95],[cols*0.4, rows*0.6],[cols*0.9, rows*0.95],[cols*0.6, rows*0.6]]],dtype=np.int32)
    ROI = region_of_interest(img_edge, vertices) 
    rho = 2
    theta=np.pi/180
    threshold=20
    minLineLength=20
    maxLineGap=50
    lines = cv2.HoughLinesP(ROI, rho, theta, threshold, np.array([]), minLineLength, maxLineGap)
    if lines is None:
        img_msg = bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        img_line_pub.publish(img_msg)
    else:
        draw_lines_improved(cv_image, lines, color=[255, 0, 0], thickness=10)
        img_wtline_msg = bridge.cv2_to_imgmsg(cv_image,encoding='bgr8')
        img_line_pub.publish(img_wtline_msg)
        
def listener():
    global img_line_pub
    img_line_pub = rospy.Publisher(u'img_line_topic', Image, queue_size=1)
    rospy.init_node(u'img_line',anonymous=True)
    rospy.Subscriber(u"/camera/color/image_raw" ,Image, callback)
    rospy.spin()
    
if __name__ == u'__main__':
    listener()
