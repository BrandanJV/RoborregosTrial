#! /usr/bin/env python3

import rospy
import actionlib
import party_navigation.msg
from navigation_utils import Behaviors, StatusMessage

class NavigationClient(object):

    def __init__(self, name):
        self._action_name = name
        self._client = actionlib.SimpleActionClient(self._action_name, party_navigation.msg.NavigationAction)
        self._client.wait_for_server()
        rospy.loginfo("Client Navigation - Connected with Server.")
        self.test_action_server()
    
    def test_action_server(self):
        # Creates a goal to send to the action server.
        goal = party_navigation.msg.NavigationGoal(behavior=Behaviors.Patrol.value)

        # Sends the goal to the action server.
        self._client.send_goal(goal)
        rospy.loginfo("Client Navigation - Goal Sended")

        # Waits for the server to finish performing the action.
        self._client.wait_for_result()

        # Prints out the result of executing the action.
        result = self._client.get_result()  # A NavigationResult
        rospy.loginfo("Client Navigation - Result:" + StatusMessage(result.result).name)
        
if __name__ == '__main__':
    rospy.init_node('NavigationClient', anonymous = True)
    client = NavigationClient('Navigation')
    rospy.spin()
