# System Architecture Design Challenge

## Drinking Robot

## Description
Here is a technical description of the different nodes/actions/services the __Drinking Robot__ will execute. 

## Development team

| Name                    | Email                                                               | Github                                                       | Role      |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------ | --------- |
| Aurora Tijerina | [auro.tj@gmail.com](mailto:auro.tj@gmail.com) | [@AuroTB](https://github.com/aurotb) | Navigation & Integration |
| José Cisneros | [A01283070@itesm.mx](mailto:A01283070@itesm.mx) | [@Josecisneros001](https://github.com/Josecisneros001) | PM & Programmer |


## Table of contents

- [Drinking Robot](#drinking-robot)
  - [Description](#description)
  - [Table of contents](#table-of-contents)
  - [Development team](#development-team)
  - [Env Setup](#env-setup)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Robot modules](#robot-modules)

## Env setup
1. Install ROS Noetic : [Reference](http://wiki.ros.org/noetic/Installation/Ubuntu)

## Installation
1. **Fork the repository into your account**

2. Clone the project repository on your local machine.

   HTTP:

   ```bash
   $ git clone https://github.com/your-username/RoborregosTrial.git
   ```

3. Change to branch systemArchitectureChallenge

   ```bash
   $ git checkout systemArchitectureChallenge
   ```

## Usage
1. Enter catkin workspace
```bash
   cd candidates_ws
```

2. Build packages
```bash
   catkin_make
```

3. Run robot modules
```bash
   rosrun beverage_dispenser dispenser_server.py # Simulate Beverage Dispense System
   rosrun env_analysis env_analysis.py # Simulate Env Analysis System
   rosrun party_navigation navigation_server.py # Simulate Navigation System
   rosrun speech speech_service.py # Simulate Speech System
   rosrun state_machine st_subscriber.py #state machine of system
```

## Robot modules

- Here is some information about the robot modules, to know more about these systems, dive into their files.

   ### Env analysis
   Node publisher in charge of telling the robotic system what is happening around the robot.

   | Topic name | Message | Definition |
   | --- | --- | --- |
   | env_analysis_feedback | uint16 data | <ul><li>0 - There is no stimuli</li><li>1 - Person asked for yor attention</li><li>2 - The cup is in front of you</li></ul> |

   ### Beverage dispenser
   Action server in charge of activating and deactivating the beverage dispenser.

   | Goal message | Valid goals |
   | --- | --- |
   | **uint16 beverage\_type**: Specifies the type of beverage the user wants. | <ul><li>1 - Lemonade</li><li>2 - Coca Cola</li><li>3 - Water</li></ul> |

   ### HRI
   Service for human robot interaction through speech, which:
   - Asks what kind of beverage the person wants.
   - Retrieves the beverage

   | Request | Response |
   | --- | --- |
   | **uint16 question**: Specifies the question the robot will give the user. <ul><li>1 - What beverage do you want?</li><li>2 - Could you repeat the beverage, please?</li></ul>|<ul><li>1 - Lemonade</li><li>2 - Coca Cola</li><li>3 - Water</li><li>4 - Undefined</li></ul> |

   ### Party Navigation
   | Goal message | Valid goals |
   | --- | --- |
   | **uint16 behavior**: Specifies the navigation behavior of the robot. | <ul><li>1 - Patrol the party</li><li>2 - Stop</li></ul> |
   
   
   ### State Machine
   State machine that starts with a listener of the env_analysis and starts to send data to servers and services
   |  Input | Outputs |
   | --- | ---  |
   |  **uint16**: Data read from the node publisher of env_analysis  | <ul><li>PATROLLING</li><li>WAITING4STIMULI</li><li>STOPPED</li></ul> |
