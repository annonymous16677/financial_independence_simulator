from StateOfTheUnion import *
from printCash import *
class Environment:
    def name(self):
        noun = "with" if self.SOCIAL_SECURITY_ENABLED == 1 else "without"
        startcashinmil =  self.STARTING_CASH_IN_THOUSANDS 
        return "Start with %sk, %s %s SS, %sk house, %sk 401k, wait %sY"%(printCash(startcashinmil), self.STATE_OF_THE_UNION.name(), noun, printCash( env.COST_OF_HOUSE / 1000), printCash(round(self.INITIAL_IRA/1000)), self.YEARS_TO_WAIT )

    pass

list_of_environments = []

for state_of_the_union in [ California()]:
 for starting_cash_in_thousands in [4100]:
  for social_security_enabled in [0]:
   for cash_in_ira in [35000]:
       for ytw in [0]:
        
       
        env = Environment()
        
        env.STARTING_CASH_IN_THOUSANDS = starting_cash_in_thousands - cash_in_ira/1000.0
           
        env.COST_OF_LIVING_IN_THOUSANDS = 72
        env.COST_OF_KID_IN_THOUSANDS = 20
        env.COST_OF_KID_COLLEGE_IN_THOUSANDS_TUITION = 35
        env.COST_OF_KID_COLLEGE_IN_THOUSANDS_LIVING_QUALIFIED = 12
        env.COST_OF_KID_COLLEGE_IN_THOUSANDS_LIVING_NON_QUALIFIED = 12
        env.AGE_OF_KIDS = 35
        env.NUMBER_OF_KIDS = 2
        env.STATE_OF_THE_UNION = state_of_the_union
        
        env.INITIAL_IRA = cash_in_ira
        
        env.SOCIAL_SECURITY_ENABLED = social_security_enabled
        env.SOCIAL_SECURITY_INCOME = 20000
        env.AGE_SOCIAL_SECUIRTY_STARTS = 67
          
        env.YEARS_TO_WAIT = ytw
          
        env.COST_OF_HOUSE = 400000
        env.THIRTY_YEAR_MORTGAGE_INTEREST_RATE = 4.5
        env.FIFTEEN_YEAR_MORTGAGE_INTEREST_RATE = 3.5
        env.mortgage_interest_deduction = False
        
        list_of_environments.append(env)

        
        
