
from TaxTable import *
class StateOfTheUnion:
    def __init__(self):
        pass
    
    def state_tax_from_income(self, income):
        pass
    
    def state_tax_from_long_term_capital_gains(self, income, cap):
        pass
        
    
    
class Texas(StateOfTheUnion):
    def state_tax_from_long_term_capital_gains(self, income, cap, tax_adj):
        return 0
    def state_tax_from_income(self, income, cap, tax_adj):
        return 0
    def name(self):
        return "Texas"
class Nevada(StateOfTheUnion):
    def state_tax_from_long_term_capital_gains(self, income, cap, tax_adj):
        return 0
    def state_tax_from_income(self, income, cap, tax_adj):
        return 0
    def name(self):
        return "Nevada"
    
class Arizona(StateOfTheUnion):
    pass
class Washington(StateOfTheUnion):
    pass
class Hawaii(StateOfTheUnion):
    pass

class California(StateOfTheUnion):
    
    def name(self):
        return "California"
    def state_tax_from_long_term_capital_gains(self, income, cap, tax_adjustment):
        return 0
    def state_tax_from_income(self, income, long_cap, tax_adjustment):
        if long_cap < 0: long_cap = 0
        standard_deduction = 7682 * tax_adjustment
        income_tax_table = [[.01, 14910],
                            [.02, 35352],
                            [.04, 55794],
                            [.06, 77452],
                            [.08, 97884],
                            [.093, 500000],
                            [.103,600000],
                            [.113,1000000],
                            [.123]]        
        tax = tax_amount_from_tax_table(long_cap+income-standard_deduction,income_tax_table, tax_adjustment)
        return tax
        
STATES_OF_THE_UNION = [Texas(),
                       #Arizona(), Washington(), Hawaii(),
                       California()]

    
