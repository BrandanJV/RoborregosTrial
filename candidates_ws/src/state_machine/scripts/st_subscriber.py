#!/usr/bin/env python3
import rospy
from std_msgs.msg import UInt16

from st_machine import states


def listener():
    rospy.init_node('st_subscriber', anonymous = True)
    rospy.Subscriber("party_status", UInt16, states)
    rospy.spin()

if __name__ == '__main__':
    listener()