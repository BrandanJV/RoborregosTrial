#!/usr/bin/env python3
# license removed for brevity
import rospy
import random
import time
from std_msgs.msg import UInt16

def talker():
    ''' For the env_analysis_feedback messages:
        0 - There is no stimuli
        1 - Person asked for a drink
        2 - The cup is in front of you
    '''
    rospy.init_node('env_analysis_node', anonymous=True)
    pub = rospy.Publisher('party_status', UInt16, queue_size=10)
    while not rospy.is_shutdown():
        env_analysis = random.randint(0,2)
        rospy.loginfo(env_analysis)
        pub.publish(env_analysis)
        time.sleep(10)
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass