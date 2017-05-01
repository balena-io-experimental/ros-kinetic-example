#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

# Pins for GPIO use
pinForward = 23
pinBackward = 24
pinLeft = 27
pinRight = 22
pinMusic = 17

def callback(data):
  rospy.loginfo(rospy.get_caller_id() + " - Action: %s", data.data)
  if data.data == "forward":
    rospy.loginfo("Moving forward")
    GPIO.output(pinForward, 1)
    GPIO.output(pinBackward, 0)
    GPIO.output(pinLeft, 0)
    GPIO.output(pinRight, 0)
  elif data.data == "backward":
    rospy.loginfo("Moving backward")
    GPIO.output(pinForward, 0)
    GPIO.output(pinBackward, 1)
    GPIO.output(pinLeft, 0)
    GPIO.output(pinRight, 0)
  elif data.data == "left":
    rospy.loginfo("Turning left")
    GPIO.output(pinForward, 0)
    GPIO.output(pinBackward, 0)
    GPIO.output(pinLeft, 1)
    GPIO.output(pinRight, 0)
  elif data.data == "right":
    rospy.loginfo("Turning right")
    GPIO.output(pinForward, 0)
    GPIO.output(pinBackward, 0)
    GPIO.output(pinLeft, 0)
    GPIO.output(pinRight, 1)
  elif data.data == "music":
    rospy.loginfo("Playing music")
    GPIO.output(pinMusic, 1)
    time.sleep(1)
    GPIO.output(pinMusic, 0)
  elif data.data == "stop":
    rospy.loginfo("Stopping")
    GPIO.output(pinForward, 0)
    GPIO.output(pinBackward, 0)
    GPIO.output(pinLeft, 0)
    GPIO.output(pinRight, 0)

def driver():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pinForward, GPIO.OUT)
  GPIO.setup(pinBackward, GPIO.OUT)
  GPIO.setup(pinLeft, GPIO.OUT)
  GPIO.setup(pinRight, GPIO.OUT)
  GPIO.setup(pinMusic, GPIO.OUT)
  rospy.init_node('driver')
  rospy.Subscriber("robot_action", String, callback)
  rospy.spin()

if __name__ == '__main__':
  driver()
