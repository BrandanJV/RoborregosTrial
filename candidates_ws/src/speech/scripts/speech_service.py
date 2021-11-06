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

questions = [
    "What beverage do you want?",
    "Could you repeat the beverage, please?",
]

def do_speech(params):
    question = params.question
    if question < 1 or question > 2:
        rospy.loginfo("Question Error...")
        return Beverages.Undefined.value

    rospy.loginfo("Robot Asked: " + questions[question - 1])
    
    beverage = Beverages(random.randint(1,4))
    rospy.loginfo("Robot Heard: "  + beverage.name)

    return beverage.value

def main():
    rospy.init_node("SpeechService")
    service = rospy.Service('SpeechService', SpeechService, do_speech)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
