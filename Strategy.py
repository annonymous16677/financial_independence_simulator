from StrategyBasic import *




class percentage_in_bonds(StrategyFramework):
    def name(self):
        return "%s%% in Bonds, %s, %sk 529"%(self.bond_percentage ,self.mortgage_str(), printCash(self.amount_of_money_for_qtp/1000.0) )
    
    def __init__(self, bond_percentage = 0, mortgage_length = 30, qualified_tuition_plan = 0):
        self.initStrategyFramework(mortgage_length, qualified_tuition_plan)
        self.bond_percentage = bond_percentage


    def strategy_function(self, n):
        return {CASH_PERCENT : 0,
                BOND_PERCENT : self.bond_percentage,
                STOCK_PERCENT : 100-self.bond_percentage,
                    IRA_CASH_PERCENT : 0,
                    IRA_BOND_PERCENT : self.bond_percentage,
                    IRA_STOCK_PERCENT : 100 - self.bond_percentage,
                    QTP_CASH_PERCENT : 0,
                        QTP_BOND_PERCENT :self.bond_percentage ,
                        QTP_STOCK_PERCENT : 100 - self.bond_percentage }

    
class percentage_in_bonds_by_age(StrategyFramework):
    def name(self):
        return "%s%%-%s%% in Bonds, %s, %sk 529"%(self.bond_percentage_at_age_zero , self.bond_percentage_at_age_hundred , self.mortgage_str(), printCash(self.amount_of_money_for_qtp/1000.0) )
    
    def __init__(self, bond_percentage_at_age_zero = 0, bond_percentage_at_age_hundred = 0, mortgage_length = 30, qualified_tuition_plan = 0):
        self.initStrategyFramework(mortgage_length, qualified_tuition_plan)
        self.bond_percentage_at_age_zero = bond_percentage_at_age_zero
        self.bond_percentage_at_age_hundred = bond_percentage_at_age_hundred
    
    
    def strategy_function(self, n):
        percentage_to_use = max(min( self.bond_percentage_at_age_zero + float(n.age) / 100.0 * float( self.bond_percentage_at_age_hundred) , 100), 0)
        
        return {CASH_PERCENT : 0,
            BOND_PERCENT : percentage_to_use,
            STOCK_PERCENT : 100-percentage_to_use,
                IRA_CASH_PERCENT : 0,
                IRA_BOND_PERCENT : percentage_to_use,
                IRA_STOCK_PERCENT : 100 - percentage_to_use,
                QTP_CASH_PERCENT : 0,
                    QTP_BOND_PERCENT :percentage_to_use ,
                    QTP_STOCK_PERCENT : 100 - percentage_to_use }

class years_of_living_expenses_in_bonds(StrategyFramework):
    def name(self):
        return "%s years in bonds,  %s, %sk 529"%(self.years_of_living_expenses_in_bonds, self.mortgage_str(), printCash(self.amount_of_money_for_qtp/1000.0) )
    
    def __init__(self, years_of_living_expenses_in_bonds = 0, bond_percentage_at_age_zero = 0, bond_percentage_at_age_hundred = 0, mortgage_length = 30, qualified_tuition_plan = 0):
        self.initStrategyFramework(mortgage_length, qualified_tuition_plan)
        self.bond_percentage_at_age_zero = bond_percentage_at_age_zero
        self.bond_percentage_at_age_hundred = bond_percentage_at_age_hundred
        self.years_of_living_expenses_in_bonds = years_of_living_expenses_in_bonds
    
    def strategy_function(self, n):
        percentage_to_use = max(min( self.bond_percentage_at_age_zero + float(n.age) / 100.0 * float( self.bond_percentage_at_age_hundred) , 100), 0)

        [living_cost, edu_cost] = n.years_of_living_expenses(self.years_of_living_expenses_in_bonds)
       
        
        amount_in_bonds = living_cost + edu_cost
        bond_amt_from_norm = min(n.ending_cash_bond_stock, amount_in_bonds)
        amount_in_bonds = amount_in_bonds - bond_amt_from_norm
        bond_amount_from_qtp = min(n.ending_qtp, amount_in_bonds)
        amount_in_bonds = amount_in_bonds - bond_amount_from_qtp
        bond_amount_from_ira = min(n.ending_ira, amount_in_bonds)

        return {CASH_PERCENT : 0,
            BOND_AMOUNT : bond_amt_from_norm,


                IRA_BOND_AMOUNT: bond_amount_from_ira,
                IRA_CASH_PERCENT :0,

                    QTP_BOND_AMOUNT :bond_amount_from_qtp ,
                    QTP_CASH_PERCENT :0 }







LIST_OF_STRATEGIES = []

for years in range(2,7,2):
    for hist in range(2,7,2):
        for rate in [0.5,1,2,3,4]:
            pass
#LIST_OF_STRATEGIES.append( years_living_expenses_in_bonds_with_gradual_buyback(years,hist, rate))

for perc_30 in range(0,100, 10):
    for perc_100 in range(0,100, 10):
        pass
#LIST_OF_STRATEGIES.append( percentage_of_age_in_bonds_over_lifetime(perc_30,perc_100))

for m in [30]:
    for qtp in [450000]:
        for percA in range(0,101,10):
            for percB in range(0,101,10):
        
    #LIST_OF_STRATEGIES.append( percentage_in_bonds_by_age(percA, percB, m, qtp))
                pass
    pass

for m in [30]:
    for qtp in [450000]:
        for years in range(0,10,1):
            
            
            #LIST_OF_STRATEGIES.append( years_of_living_expenses_in_bonds(years_of_living_expenses_in_bonds = years))
            pass
    pass

LIST_OF_STRATEGIES.append( percentage_in_bonds(0, 30,450000))
LIST_OF_STRATEGIES.append( percentage_in_bonds(10, 30,450000))
LIST_OF_STRATEGIES.append( percentage_in_bonds(20, 30,450000))
LIST_OF_STRATEGIES.append( percentage_in_bonds(30, 30,450000))
LIST_OF_STRATEGIES.append( percentage_in_bonds(40, 30,450000))

