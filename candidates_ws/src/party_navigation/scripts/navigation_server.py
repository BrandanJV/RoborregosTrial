#! /usr/bin/env python3

import rospy
import actionlib
import party_navigation.msg
import time
from navigation_utils import Behaviors, StatusMessage

SET_BEHAVIOR_DELAY = 2 # seconds

class NavigationServer(object):
    # Create messages that are used to publish feedback/result.
    _feedback = party_navigation.msg.NavigationFeedback()
    _result = party_navigation.msg.NavigationResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, party_navigation.msg.NavigationAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        rospy.loginfo('%s: Action Server Initialized' % (self._action_name))
      
    def execute_cb(self, goal):
        # Helper variables.
        behavior = Behaviors(goal.behavior)
        
        # Reset Feedback & Result variables.
        self._feedback.status = 0
        self._result.result = 0
        
        # Publish info to the console for the user.
        rospy.loginfo('%s: Action Server Navigation Goal Received, Behavior: %s' % (self._action_name, behavior.name))
        
        
        # check that preempt has not been requested by the client
        if self._as.is_preempt_requested():
            rospy.loginfo('%s: Action Server Navigation Preempted' % self._action_name)
            self._as.set_preempted()
            return

        # Start executing the action
        
        # Publish the feedback
        self._feedback.status = StatusMessage.Busy.value
        self._as.publish_feedback(self._feedback)
        rospy.loginfo('%s: Action Server Navigation Feedback: %s' % (self._action_name, StatusMessage.Busy.name))

        time.sleep(SET_BEHAVIOR_DELAY)
        
        # Publish the feedback
        self._feedback.status = StatusMessage.Busy.value
        self._as.publish_feedback(self._feedback)
        rospy.loginfo('%s: Action Server Navigation Feedback: %s' % (self._action_name, StatusMessage.Busy.name))
        
        time.sleep(SET_BEHAVIOR_DELAY)
          
        self._result.result = StatusMessage.Success.value
        rospy.loginfo('%s: Action Server Navigation Succeeded' % self._action_name)
        self._as.set_succeeded(self._result)
        
if __name__ == '__main__':
    rospy.init_node('NavigationServer')
    server = NavigationServer('Navigation')
    rospy.spin()
