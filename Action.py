from Asset import *
from printCash import printCash
import math
class ActionType:
    transfer = 0
    multiplier = 1
    advanceQuarter = 2
    dividend = 3
    bankruptcy = 4

class ActionGroup:
    def __init__(self):
        self.actions = []
    def addAction(self, action):
        self.actions.append(action)
    


class Action:
    def __init__(self, action_type, source = None, destination = None, amount = None, multiplier = None, relative_dividend = None):
        self.source = source
        self.destination = destination
        if amount:
            self.amount =(amount)
        else:
            self.amount = 0
        self.multiplier = multiplier
        self.relative_dividend = relative_dividend
        self.action_type = action_type
    def __str__(self):
        
        if self.action_type == ActionType.transfer:
            return "Move %s from %s to %s"%(printCash(self.amount), assetTypeToString(self.source), assetTypeToString(self.destination))
            
        elif self.action_type == ActionType.multiplier:
            if self.multiplier == 1:
                return None
            percent = abs(round((self.multiplier - 1)*100,1))
            if self.multiplier > 1:
                verb = "up"
                sign = "+"
            else:
                verb = "down"
                sign = "-"
            if self.source == AssetType.index_cost_of_living:
                preposition = ""
            else:
                preposition = "in value "
            return  "%s went %s %s%s%s%%"%(assetTypeToString(self.source), verb,preposition, sign, percent)
        elif self.action_type == ActionType.advanceQuarter:
            return None
            return "Advance Quarter"
        elif self.action_type == ActionType.dividend:
            if self.relative_dividend == 0:
                return None
            percent = round((self.relative_dividend)*100,1)
            return  "%s generates a dividend of +%s%%"%(assetTypeToString(self.source), percent)
        elif self.action_type == ActionType.bankruptcy:
            return "Declare bankruptcy"
        else:
            raise Exception("Unknown action")
            
          
    
    
    
    