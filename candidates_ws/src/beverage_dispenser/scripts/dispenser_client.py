#! /usr/bin/env python3

import rospy
import actionlib
import beverage_dispenser.msg
from dispenser_utils import Beverages, ResultMessage

class DispenserClient(object):

    def __init__(self, name):
        self._action_name = name
        self._client = actionlib.SimpleActionClient(self._action_name, beverage_dispenser.msg.BeverageDispenserAction)
        self._client.wait_for_server()
        rospy.loginfo("Client - Connected with Server.")
        self.test_action_server()
    
    def test_action_server(self):
        # Creates a goal to send to the action server.
        goal = beverage_dispenser.msg.BeverageDispenserGoal(beverage_type=Beverages.Lemonade.value)

        # Sends the goal to the action server.
        self._client.send_goal(goal)
        rospy.loginfo("Client - Goal Sended")

        # Waits for the server to finish performing the action.
        self._client.wait_for_result()

        # Prints out the result of executing the action.
        result = self._client.get_result()  # A BeverageDispenserResult
        rospy.loginfo("Client - Result:" + ResultMessage(result.result).name)
        
if __name__ == '__main__':
    rospy.init_node('DispenserClient', anonymous = True)
    client = DispenserClient('BeverageDispenser')
    rospy.spin()
