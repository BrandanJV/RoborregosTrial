#!/usr/bin/env python3
import sys
import rospy
import random
from std_msgs.msg import UInt16
from speech.srv import SpeechService
from enum import Enum

class Beverages(Enum):
    Lemonade = 1
    Coca_Cola = 2
    Water = 3
    Undefined = 4

def do_speech_client(question = 1):
    rospy.wait_for_service('SpeechService')
    try:
        do_speech = rospy.ServiceProxy('SpeechService', SpeechService)
        beverage = Beverages(do_speech(question).beverage)
        rospy.loginfo("Service Client, Beverage Received: "  + beverage.name)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def main():
    rospy.init_node("SpeechServiceClient")
    do_speech_client()
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
