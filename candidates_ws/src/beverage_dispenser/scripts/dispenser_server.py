#! /usr/bin/env python3

import rospy
import actionlib
import beverage_dispenser.msg
import time
from dispenser_utils import Beverages, ResultMessage, MechanismSteps

MECHANISM_STEP_DELAY = 2 # seconds

class DispenserServer(object):
    # Create messages that are used to publish feedback/result.
    _feedback = beverage_dispenser.msg.BeverageDispenserFeedback()
    _result = beverage_dispenser.msg.BeverageDispenserResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, beverage_dispenser.msg.BeverageDispenserAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        rospy.loginfo('%s: Action Server Initialized' % (self._action_name))
      
    def execute_cb(self, goal):
        # Helper variables.
        beverage = Beverages(goal.beverage_type)
        success = True
        
        # Reset Feedback & Result variables.
        self._feedback.mechanismStep = 0
        self._result.result = 0
        
        # Publish info to the console for the user.
        rospy.loginfo('%s: Action Server Delivering, %s' % (self._action_name, beverage.name))
        
        # Start executing the action
        for step in MechanismSteps:
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Action Server Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break

            # Publish the feedback
            self._feedback.mechanismStep = step.value
            self._as.publish_feedback(self._feedback)
            rospy.loginfo('%s: Action Server Feedback STEP: %s' % (self._action_name, step.name))
            
            # The sequence is computed at 1/3 Hz for demonstration purposes.
            time.sleep(MECHANISM_STEP_DELAY)
          
        if success:
            self._result.result = ResultMessage.Success.value
            rospy.loginfo('%s: Action Server Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
        
if __name__ == '__main__':
    rospy.init_node('DispenserServer')
    server = DispenserServer('BeverageDispenser')
    rospy.spin()
