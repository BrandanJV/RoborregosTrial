#!/usr/bin/env python3
import roslib
import actionlib
import rospy
import smach
import smach_ros
import sys
from smach_ros import ServiceState
from std_msgs.msg import UInt16

sys.path.insert(0, '/home/brandan/Candidates-2021/candidates_ws/src/speech/scripts')
sys.path.insert(0, '/home/brandan/Candidates-2021/candidates_ws/src/beverage_dispenser/scripts')

from speech_service_client import do_speech_client
from dispenser_client import DispenserClient

class Env_analysis(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['no_stimuli', 'to_patrol', 'to_stop'],
                                        input_keys = ['env_input'], 
                                        output_keys = ['env_output'])
    def execute(self, userdata):

        if userdata.env_input == 0:
            userdata.env_output = 0
            return 'no_stimuli'
        elif userdata.env_input == 1:
            userdata.env_output = 1
            return 'to_patrol'  
        elif userdata.env_input == 2:
            userdata.env_output = 2
            return 'to_stop'


class PATROL(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes =['patrolling', 'stop_patrolling'],
                                    input_keys = ['pat_input'],
                                    output_keys = ['pat_output'])

    def execute(self, userdata):
        if userdata.pat_input == 0:
            return 'patrolling'
        elif userdata.pat_input == 1:
            return 'patrolling'
        elif userdata.pat_input == 2:
            return 'stop_patrolling'

class STOP(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes =['stop', 'start_patrolling'],
                                    input_keys = ['stop_input'],
                                    output_keys = ['stop_output'])

    def execute(self, userdata):
        if userdata.stop_input == 0:
            return 'stop'
        elif userdata.stop_input == 1:
            return 'start_patrolling'
        elif userdata.stop_input == 2:
            return 'stop'

class no_stimuli(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes =['no_sti'])
    def execute(self, userdata):
        return 'no_sti'

class HR(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['succeeded'])

    def execute(self, userdata):
        drink = do_speech_client(1)
        #rospy.loginfo(drink)
        return 'succeeded'

class Dispenser(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes = ['success'])

    def execute(self, userdata):
        result = DispenserClient.test_action_server
        return 'success'


def states(data):
    sm_top = smach.StateMachine(outcomes=['PATROLLING', 'WAITING4STIMULI', 'STOPPED'])
    sm_top.userdata.env_input = data.data
    with sm_top:
        smach.StateMachine.add('ENV_ANALYSIS', Env_analysis(), 
                                            transitions = {'no_stimuli': 'no_stimuli',
                                                            'to_patrol': 'PATROL', 
                                                            'to_stop': 'STOP'
                                                            },
                                            remapping = {'env_input': 'env_input',
                                                            'env_output': 'env_data'})

        smach.StateMachine.add('no_stimuli', no_stimuli(),
                                                transitions = {'no_sti': 'WAITING4STIMULI'})

        smach.StateMachine.add('PATROL', PATROL(), 
                                        transitions = {'patrolling': 'PATROLLING',
                                                        'stop_patrolling': 'STOP'},
                                            remapping = {'pat_input': 'env_data',
                                                         'pat_output': 'pat_data'})

        smach.StateMachine.add('STOP', STOP(), 
                                        transitions = {'stop': 'HRI',
                                                        'start_patrolling': 'PATROL'},
                                        remapping = {'stop_input': 'env_data',
                                                    'stop_output': 'stop_data'})

        smach.StateMachine.add('HRI', HR(), transitions = {'succeeded': 'DISPENSE'})

        smach.StateMachine.add('DISPENSE', Dispenser(), transitions = {'success': "STOPPED"})
            
        sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
        sis.start()
            

    outcome = sm_top.execute()

    