from enum import Enum

class Beverages(Enum):
    Lemonade = 1
    Coca_Cola = 2
    Water = 3
    Undefined = 4

class ResultMessage(Enum):
    Failed = 0
    Success = 1

class MechanismSteps(Enum):
    Searching = 1
    Giving = 2
    Restarting = 3
