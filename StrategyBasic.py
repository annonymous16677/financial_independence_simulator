from Action import *
from StateOfTheUnion import *
from HistoricState import *
import math

CASH_PERCENT = "CASH_PERCENT"
BOND_PERCENT = "BOND_PERCENT"
STOCK_PERCENT = "STOCK_PERCENT"
IRA_CASH_PERCENT = "IRA_CASH_PERCENT"
IRA_BOND_PERCENT = "IRA_BOND_PERCENT"
IRA_STOCK_PERCENT = "IRA_STOCK_PERCENT"
QTP_CASH_PERCENT = "QTP_CASH_PERCENT"
QTP_BOND_PERCENT = "QTP_BOND_PERCENT"
QTP_STOCK_PERCENT = "QTP_STOCK_PERCENT"

CASH_AMOUNT = "CASH_AMOUNT"
BOND_AMOUNT = "BOND_AMOUNT"
STOCK_AMOUNT = "STOCK_AMOUNT"
IRA_CASH_AMOUNT = "IRA_CASH_AMOUNT"
IRA_BOND_AMOUNT = "IRA_BOND_AMOUNT"
IRA_STOCK_AMOUNT = "IRA_STOCK_AMOUNT"
QTP_CASH_AMOUNT = "QTP_CASH_AMOUNT"
QTP_BOND_AMOUNT = "QTP_BOND_AMOUNT"
QTP_STOCK_AMOUNT = "QTP_STOCK_AMOUNT"


class Namespace:
    pass

def actionsToGoFromTo(begin, end):
    [cash,bond,stock,ira_stock,ira_bond, ira_cash ,qtp_stock,qtp_bond,qtp_cash, spend_taxes_state,spend_taxes_federal, spend_taxes_penalty,spend_living_expenses,spend_down_payment_on_house,spend_mortgage_payment_on_house ,  spend_kids_college_tuition ,spend_kids_college_edu,spend_kids_college_misc,spend_kids_expenses] = [AssetType.cash,AssetType.bond,AssetType.stock,AssetType.ira_stock,AssetType.ira_bond , AssetType.ira_cash,  AssetType.qtp_stock,AssetType.qtp_bond,AssetType.qtp_cash,AssetType.spend_taxes_state,AssetType.spend_taxes_federal,AssetType.spend_taxes_penalty, AssetType.spend_living_expenses,AssetType.spend_down_payment_on_house,AssetType.spend_mortgage_payment_on_house ,  AssetType.spend_kids_college_tuition ,AssetType.spend_kids_college_edu,AssetType.spend_kids_college_misc,AssetType.spend_kids_expenses]
    
    
    actions = []
    c = begin.copy()
    d = end.copy()
    
    
    for x in LIST_OF_ALL_ASSET_TYPES:
        if x not in c:
            c[x] = 0.0
        if x not in d:
            d[x] = 0.0
    if abs(sum([c[x] - d[x] for x in LIST_OF_ALL_ASSET_TYPES])) > 1 :
        print "\nbegin = %s (total = %s)"%(str(begin),  (sum([c[x]  for x in LIST_OF_ALL_ASSET_TYPES])) )
        print "\nend = %s (total = %s)\n"%(str(end),  (sum([ d[x] for x in LIST_OF_ALL_ASSET_TYPES])) )
        print "off by %s"%(abs(sum([c[x] - d[x] for x in LIST_OF_ALL_ASSET_TYPES])))
        raise Exception("Off!")
    
    
    def mv(amount, src, dest):
        if amount < 0.01:
            return
        actions.append(Action(ActionType.transfer, source = src, destination = dest, amount = amount))
        if src not in c: c[src] = 0
        c[src] = c[src] - amount
        if dest not in c: c[dest] = 0
        c[dest] = c[dest] + amount
    def equalize(a, b):
        
        
        
        if (c[a] < d[a]) and (c[b] > d[b]) and b not in LIST_OF_SINK_TYPES:
            mv(min(d[a]-c[a], c[b] - d[b]), b, a)
        elif (c[b] < d[b]) and (c[a] > d[a]) and a not in LIST_OF_SINK_TYPES:
            mv(min(d[b]-c[b], c[a] - d[a]), a, b)
        else:
            pass
    def eq(list):
        for a in list:
            for b in list:
                if a < b:
                    equalize(a,b)
    
    
    eq([qtp_stock, qtp_bond, qtp_cash])
    eq([qtp_stock, qtp_bond, spend_kids_college_edu, spend_kids_college_tuition])
    eq([ira_stock, ira_bond, ira_cash])
    
    eq(LIST_OF_ALL_ASSET_TYPES)
    
    return actions


class BasicStrategy:
    def __init__(self):
        
        
        pass
    def mortgage_str(self):
        if self.HAVE_MORTGAGE:
            return "%s-yr mortage"%(self.YEARS_OF_MORTGAGE)
        else:
            return "no mortgage"
    def init(self):
        
        
        self.HAVE_MORTGAGE = False
        self.PERCENT_DOWN = 20
        self.YEARS_OF_MORTGAGE = 30
    
    def reinvest_dividends(self):
        return True
    
    def estimated_quarterly_inflation_rate(self):
        return 1.008374761
    def __str__(self):
        return self.name()
    def should_strategy_declare_bankruptcy_this_quarter(self, historic_state):
        return historic_state.dollar_amount_of_total_expenditures_required_this_quarter() > historic_state.total_assets()






class StrategyFramework(BasicStrategy):
    def initStrategyFramework(self,  mortgage_years, amount_of_money_for_qtp):
        self.init()
        self.amount_of_money_for_qtp = amount_of_money_for_qtp

        if mortgage_years == 0:
            self.HAVE_MORTGAGE = False
        else:
            self.HAVE_MORTGAGE = True
            self.YEARS_OF_MORTGAGE = mortgage_years

    
    
    
    def actions_for_quarter(self, historic_state):
        
        actions = []
        beginning_assets = historic_state.assets()
        cash = historic_state.assetValue(AssetType.cash)
        bond = historic_state.assetValue(AssetType.bond)
        stock = historic_state.assetValue(AssetType.stock)
        ira_stock = historic_state.assetValue(AssetType.ira_stock)
        ira_cash = historic_state.assetValue(AssetType.ira_cash)
        ira_bond = historic_state.assetValue(AssetType.ira_bond)
        qtp_stock =historic_state.assetValue(AssetType.qtp_stock)
        qtp_bond =historic_state.assetValue(AssetType.qtp_bond)
        qtp_cash =historic_state.assetValue(AssetType.qtp_cash)
        
        total_ira = ira_stock + ira_bond + ira_cash
        total_qtp =qtp_stock + qtp_bond + qtp_cash
        total_stock_bond_cash = cash + stock + bond
        
        
        amount_of_money_to_add_to_qtp = min(historic_state.amount_allowed_to_contribute_to_qtp(),
                                            self.amount_of_money_for_qtp - historic_state.total_amount_contributed_to_qtp)
        
        if amount_of_money_to_add_to_qtp > 0:
            total_qtp = total_qtp + amount_of_money_to_add_to_qtp
            total_stock_bond_cash = total_stock_bond_cash - amount_of_money_to_add_to_qtp
            pass
        
        
        expenses = historic_state.total_expenditures_required_this_quarter()
        
        qtp_expenses = expenses.get(AssetType.spend_kids_college_tuition, 0) + expenses.get(AssetType.spend_kids_college_edu, 0)
        non_qtp_expenses = historic_state.dollar_amount_of_total_expenditures_required_this_quarter() - qtp_expenses
        total_expenses_left_to_pay = qtp_expenses + non_qtp_expenses
        
                
       
        
        total_amount_to_pay_from_qtp = min(total_qtp, qtp_expenses)
        total_expenses_left_to_pay = total_expenses_left_to_pay - total_amount_to_pay_from_qtp
        total_qtp = total_qtp - total_amount_to_pay_from_qtp
        
        total_amount_to_pay_from_cash_bond_stock = min(total_stock_bond_cash, total_expenses_left_to_pay)
        total_expenses_left_to_pay = total_expenses_left_to_pay - total_amount_to_pay_from_cash_bond_stock
        total_stock_bond_cash = total_stock_bond_cash - total_amount_to_pay_from_cash_bond_stock
        
        if total_expenses_left_to_pay > 0:
            if historic_state.kids_are_done_with_college():
                additional_amount_to_pay_from_qtp = min(total_expenses_left_to_pay,  total_qtp)
                total_expenses_left_to_pay = total_expenses_left_to_pay - additional_amount_to_pay_from_qtp
                total_qtp = total_qtp - additional_amount_to_pay_from_qtp
                
                additional_amount_to_pay_from_ira = min(total_expenses_left_to_pay, total_ira)
                total_expenses_left_to_pay = total_expenses_left_to_pay - additional_amount_to_pay_from_ira
                total_ira = total_ira - additional_amount_to_pay_from_ira
            else:
                additional_amount_to_pay_from_ira = min(total_expenses_left_to_pay, total_ira)
                total_expenses_left_to_pay = total_expenses_left_to_pay - additional_amount_to_pay_from_ira
                total_ira = total_ira - additional_amount_to_pay_from_ira
                
                additional_amount_to_pay_from_qtp = min(total_expenses_left_to_pay,  total_qtp)
                total_expenses_left_to_pay = total_expenses_left_to_pay - additional_amount_to_pay_from_qtp
                total_qtp = total_qtp - additional_amount_to_pay_from_qtp
        
                    
        n = Namespace()
        n.total_expenses = total_expenses_left_to_pay
        n.cash = cash
        n.bond = bond
        n.stock = stock
        n.ira_cash = ira_cash
        n.ira_bond = ira_bond
        n.ira_stock = ira_stock
        n.qtp_cash = qtp_cash
        n.qtp_bond = qtp_bond
        n.qtp_stock = qtp_stock
        n.ending_cash_bond_stock = total_stock_bond_cash
        n.ending_ira = total_ira
        n.ending_qtp = total_qtp
        n.age = float(historic_state.age_years) + (float(historic_state.age_quarters) / 4.0)
        def years_of_living_expenses(years):
            return historic_state.years_of_living_expenses(years)
        n.years_of_living_expenses =years_of_living_expenses
        
                    
        results_from_strat_function = self.strategy_function(n)
                    
        [cash_set, bond_set, stock_set, qtp_cash_set, qtp_bond_set, qtp_stock_set, ira_cash_set, ira_bond_set, ira_stock_set] = [False, False, False, False, False, False, False, False, False]
        for key, value in results_from_strat_function.iteritems():


            if key == CASH_PERCENT:
                desired_cash = total_stock_bond_cash * float(value) / 100.0
                cash_set = True
            if key == BOND_PERCENT:
                desired_bond = total_stock_bond_cash * float(value) / 100.0
                bond_set = True
            if key == STOCK_PERCENT:
                desired_stock = total_stock_bond_cash * float(value) / 100.0
                stock_set = True

            if key == IRA_CASH_PERCENT:
                desired_ira_cash = total_ira * float(value) / 100.0
                ira_cash_set = True
            if key == IRA_BOND_PERCENT:
                desired_ira_bond = total_ira * float(value) / 100.0
                ira_bond_set = True
            if key == IRA_STOCK_PERCENT:
                desired_ira_stock = total_ira * float(value) / 100.0
                ira_stock_set = True

            if key == QTP_CASH_PERCENT:
                desired_qtp_cash = total_qtp * float(value) / 100.0
                qtp_cash_set = True
            if key == QTP_BOND_PERCENT:
                desired_qtp_bond = total_qtp * float(value) / 100.0
                qtp_bond_set = True
            if key == QTP_STOCK_PERCENT:
                desired_qtp_stock = total_qtp * float(value) / 100.0
                qtp_stock_set = True
                    
            if key == CASH_AMOUNT:
                desired_cash = value
                cash_set = True
            if key == BOND_AMOUNT:
                desired_bond = value
                bond_set = True
            if key == STOCK_AMOUNT:
                desired_stock = value
                stock_set = True
            
            if key == IRA_CASH_AMOUNT:
                desired_ira_cash = value
                ira_cash_set = True
            if key == IRA_BOND_AMOUNT:
                desired_ira_bond = value
                ira_bond_set = True
            if key == IRA_STOCK_AMOUNT:
                desired_ira_stock = value
                ira_stock_set = True
            
            if key == QTP_CASH_AMOUNT:
                desired_qtp_cash = value
                qtp_cash_set = True
            if key == QTP_BOND_AMOUNT:
                desired_qtp_bond = value
                qtp_bond_set = True
            if key == QTP_STOCK_AMOUNT:
                desired_qtp_stock = value
                qtp_stock_set = True
        if not cash_set:
            desired_cash = total_stock_bond_cash - desired_bond - desired_stock
        if not bond_set:
            desired_bond = total_stock_bond_cash - desired_cash - desired_stock
        if not stock_set:
            desired_stock = total_stock_bond_cash - desired_cash - desired_bond

        if not ira_cash_set:
            desired_ira_cash = total_ira - desired_ira_bond - desired_ira_stock
        if not ira_bond_set:
            desired_ira_bond = total_ira - desired_ira_cash - desired_ira_stock
        if not ira_stock_set:
            desired_ira_stock = total_ira - desired_ira_cash - desired_ira_bond

        if not qtp_cash_set:
            desired_cash = total_qtp - desired_qtp_bond - desired_qtp_stock
        if not qtp_bond_set:
            desired_qtp_bond = total_qtp - desired_qtp_cash - desired_qtp_stock
        if not qtp_stock_set:
            desired_qtp_stock = total_qtp - desired_qtp_cash - desired_qtp_bond

    
        
        
        ending_assets = {AssetType.cash :  desired_cash,
            AssetType.bond : desired_bond,
            AssetType.stock : desired_stock,
            AssetType.ira_stock : desired_ira_stock,
            AssetType.ira_bond : desired_ira_bond,
            AssetType.ira_cash : desired_ira_cash,
            AssetType.qtp_stock : desired_qtp_stock,
            AssetType.qtp_bond : desired_qtp_bond,
            AssetType.qtp_cash : desired_qtp_cash
        }
        ending_assets.update(expenses)
        actions =  actionsToGoFromTo(beginning_assets, ending_assets)
        return actions




