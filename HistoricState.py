




import sys
import math
from tax_rates import *
from StateOfTheUnion import StateOfTheUnion
from Tally import Tally
from Parameters import *
from Asset import *
from Action import *
from MortgageCalc import *
from printCash import printCash, roundCash
from Log import log, tack
from Utility import *


def monthly_payment(principle, percentage_interest_rate, years):
    n = years * 12
    if percentage_interest_rate == 0:
        return float(principle) / float(n)
    f = 1200.0 / (1200.0 + percentage_interest_rate)
    m = principle * (1 - f) / ( f - f ** (n+1))
    return m



class MarketState:
    def __init__(self):
        self.assets = {
            
            
            AssetType.cash: 1.0,
            AssetType.bond: 1.0,
            AssetType.stock: 1.0,
            
                
          
            AssetType.ira_stock : 1.0,
            AssetType.qtp_cash : 1.0,
            AssetType.ira_cash : 1.0,
            AssetType.ira_bond : 1.0,
            AssetType.qtp_stock : 1.0,
            AssetType.qtp_bond : 1.0,
            
            AssetType.index_cost_of_living:1.0,
            AssetType.index_college_tuition: 1.0
        }
        
    def share_price(self, asset_type):
        return self.assets[asset_type]
        

class HistoricState:
    def __init__(self, init_cash, init_market_state,  strategy, env):
        self.total_expenditures_spent_this_quarter = {}
        if strategy.HAVE_MORTGAGE:
            self.INITIAL_HOUSE_PAYMENT = env.COST_OF_HOUSE * float(strategy.PERCENT_DOWN ) / 100.0
            
            self.quarters_to_pay_mortgage = strategy.YEARS_OF_MORTGAGE * 4
            if strategy.YEARS_OF_MORTGAGE <= 15:
                mortgage_interest_rate = env.FIFTEEN_YEAR_MORTGAGE_INTEREST_RATE
            elif strategy.YEARS_OF_MORTGAGE <= 30:
                mortgage_interest_rate = env.THIRTY_YEAR_MORTGAGE_INTEREST_RATE
            else:
                raise Exception("Mortgages cannot last more than 30 years")
            
            self.quarterly_mortgage_payment = 3 * monthly_payment(env.COST_OF_HOUSE * float(100.0 - strategy.PERCENT_DOWN ) / 100.0, mortgage_interest_rate, strategy.YEARS_OF_MORTGAGE)
            
        
        else:
            self.INITIAL_HOUSE_PAYMENT = env.COST_OF_HOUSE
            self.quarters_to_pay_mortgage = 0
            self.quarterly_mortgage_payment = 0
    #print "%s"%([self.INITIAL_HOUSE_PAYMENT,self.quarters_to_pay_mortgage , self.quarterly_mortgage_payment])
        
        self.SOCIAL_SECURITY_ENABLED =     env.SOCIAL_SECURITY_ENABLED
        self.SOCIAL_SECURITY_INCOME_QUARTERLY =  roundCash(env.SOCIAL_SECURITY_INCOME / 4)
        self.AGE_SOCIAL_SECUIRTY_STARTS =  env.AGE_SOCIAL_SECUIRTY_STARTS
        self.qtp_cost_basis = 0
        self.inflation_multiplier = 1
        self.mortgage_interest_deduction = env.mortgage_interest_deduction
        
        self.needed_spend_by_quarter = {}
        self.actual_spend_by_quarter = {}
            
            
        self.env = env
        self.state_of_the_union = env.STATE_OF_THE_UNION
        self.reinvest_dividends = strategy.reinvest_dividends()
        self.federal_tax_from_income = federal_tax_from_income
        self.federal_tax_from_long_term_capital_gains = federal_tax_from_long_term_capital_gains
        
        self.state_tax_from_income = self.state_of_the_union.state_tax_from_income
        self.state_tax_from_long_term_capital_gains = self.state_of_the_union.state_tax_from_long_term_capital_gains
        
        self.asset_shares = {}
        self.asset_shares_by_quarter_purchased = {}
        
        self.share_price_on_date = {}
        self.share_price = {}
        self.relative_prices ={}
        self.historic_relative_prices = {}
        
        self.tax_adjustment = 1        
        
        for at in LIST_OF_ASSET_TYPES:
            self.asset_shares[at] = 0
            
            self.asset_shares_by_quarter_purchased[at] = [0]
            
            self.share_price[at] = init_market_state.share_price(at)
            self.share_price_on_date[at] = [self.share_price[at]]
            
            self.relative_prices[at] = 1
            self.historic_relative_prices[at] = [1]
            
        self.asset_shares[AssetType.cash] = init_cash
        self.asset_shares_by_quarter_purchased[AssetType.cash] = [init_cash]
        self.asset_shares[AssetType.ira_cash] = env.INITIAL_IRA
        
        TARGET_YEARLY_INCOME_IN_REAL_DOLLARS = roundCash(self.env.COST_OF_LIVING_IN_THOUSANDS * 1000)
        self.cost_of_living = roundCash(TARGET_YEARLY_INCOME_IN_REAL_DOLLARS / 4)
        
    
        self.kids_expenses = roundCash(self.env.COST_OF_KID_IN_THOUSANDS * self.env.NUMBER_OF_KIDS * 1000 / 4)
        
        
        self.qtp_yearly_contribution_limit = 13000 * self.env.NUMBER_OF_KIDS * 2
        self.qtp_maximum_investment = 377000 * self.env.NUMBER_OF_KIDS
        self.qtp_contributions_per_year = Tally()
                
        self.kids_college_tuition = roundCash(self.env.COST_OF_KID_COLLEGE_IN_THOUSANDS_TUITION * self.env.NUMBER_OF_KIDS * 1000 / 4)
        
    
        self.kids_college_living_edu = roundCash(self.env.COST_OF_KID_COLLEGE_IN_THOUSANDS_LIVING_QUALIFIED * self.env.NUMBER_OF_KIDS * 1000 / 4)
        
    
        self.kids_college_living_misc = roundCash(self.env.COST_OF_KID_COLLEGE_IN_THOUSANDS_LIVING_NON_QUALIFIED * self.env.NUMBER_OF_KIDS * 1000 / 4)
        
    
    
        self.estimated_taxes_paid_per_quarter = Tally()
        self.taxes_paid_per_year = Tally()
        
        self.estimated_state_taxes_owed_per_quarter = Tally()
        self.estimated_federal_taxes_owed_per_quarter = Tally()
        self.estimated_penalty_taxes_owed_per_quarter = Tally()
        self.taxes_owed_per_year = Tally()
        self.spend_per_quarter = Tally()
        

        self.totalLongTermCapitalLossState = 0
        self.totalLongTermCapitalLossFederal = 0
        self.capitalLossYearlyMaxState = 3000
        self.capitalLossYearlyMaxFederal = 3000
        
        self.short_term_capital_gain_per_quarter = Tally()
        self.short_term_capital_gain_per_year = Tally()
        
        self.long_term_capital_gain_per_quarter = Tally()
        self.long_term_capital_gain_per_year = Tally()
            
        self.dividends_per_quarter = Tally()
        self.dividends_per_year = Tally()
        
            
        self.quarter = 0
        self.quarter_of_year = INITIAL_QUARTER
        self.year = INITIAL_YEAR
        self.age_years = INITIAL_AGE_YEARS
        self.age_quarters = INITIAL_AGE_QUARTERS
        
        self.total_amount_contributed_to_qtp = 0
    
    def currentStateString(self):
        year_s = str(self.year)
        quarter_s = str(self.quarter_of_year % 4 + 1)
        return "%s Q%s  %s: %s (%s total)"%(year_s, quarter_s ,
        "Age %s %s/4"%(str(self.age_years), str(self.age_quarters) ),
        ", ".join(["%s in %s"%(printCash( self.asset_shares[t] * self.share_price[t]), assetTypeToString(t)) for t in  LIST_OF_ASSET_TYPES if self.asset_shares[t] > 0.001]),
        printCash(self.total_assets())
        )
    
            
            
    def amount_allowed_to_contribute_to_qtp(self):
        
        if self.age_years >= self.env.AGE_OF_KIDS and self.age_years < self.env.AGE_OF_KIDS + 22:
            return max(
                       min(self.qtp_yearly_contribution_limit * 5 - sum([self.qtp_contributions_per_year.get(self.year - y) for y in range(5)]),
                           self.qtp_maximum_investment - self.assetValue(AssetType.qtp_stock) - self.assetValue(AssetType.qtp_bond))
                       
                       , 0)
        else:
            return 0

            

        
            
    def tax_treatment_of_transfer(self, source, destination):
        ira = [AssetType.ira_stock, AssetType.ira_bond, AssetType.ira_cash]
        qtp = [AssetType.qtp_stock, AssetType.qtp_bond, AssetType.qtp_cash]
        qualified_educational_expenses = [AssetType.spend_kids_college_tuition, AssetType.spend_kids_college_edu]
        if source in ira:
            if destination in ira:
                capital_gains_and_income_tax_charged = False
                counts_totally_as_income = False
                penalty_percentage = 0
                non_qualified_qtp = False
            elif self.age_years >= 60 or (self.age_years == 59 and self.age_quarters >= 2):
                capital_gains_and_income_tax_charged = False
                counts_totally_as_income = True
                penalty_percentage = 0
                non_qualified_qtp = False
            else:
                capital_gains_and_income_tax_charged = False
                counts_totally_as_income = True
                penalty_percentage = .10
                non_qualified_qtp = False
        elif source in qtp:
            if destination in qtp or destination in qualified_educational_expenses: 
                capital_gains_and_income_tax_charged = False
                counts_totally_as_income = False
                penalty_percentage = 0
                non_qualified_qtp = False
            else:
                capital_gains_and_income_tax_charged = False
                counts_totally_as_income = True
                penalty_percentage = 0
                non_qualified_qtp = True
        else:
            capital_gains_and_income_tax_charged = True
            counts_totally_as_income = False
            penalty_percentage = 0
            non_qualified_qtp = False
            

        return [capital_gains_and_income_tax_charged, counts_totally_as_income, penalty_percentage, non_qualified_qtp]
    def applySale(self, source, amount, destination):
        self.allow_borrowing = True
        quarter = self.quarter
        year = self.year
        
        if (source in LIST_OF_SINK_TYPES):
            spend = -amount
            if spend < 0:
                raise Exception("Cannot spend negative money %s %s"%(assetTypeToString(source), printCash(spend) ))
            spend_dict = self.total_expenditures_spent_this_quarter
            if source in self.total_expenditures_spent_this_quarter:
                self.total_expenditures_spent_this_quarter[source] = self.total_expenditures_spent_this_quarter[source]+spend
            else:
                self.total_expenditures_spent_this_quarter[source] = spend
            
        
            
        else:
            number_of_shares_to_sell = amount / self.share_price_on_date[source][quarter]
            number_of_owned_shares = self.asset_shares[source]
            if (number_of_shares_to_sell > 0 and number_of_shares_to_sell >  number_of_owned_shares+1):
                
                raise Exception("Trying to sell %s shares of %s when only %s exist"%(number_of_shares_to_sell,assetTypeToString(source) ,number_of_owned_shares))
    
            if amount > 0:
                self.asset_shares[source] = self.asset_shares[source] - number_of_shares_to_sell
                [capital_gains_and_income_tax_charged, counts_totally_as_income, penalty_percentage, non_qualified_qtp] = self.tax_treatment_of_transfer(source, destination)
                
                if capital_gains_and_income_tax_charged:
                    short_term_capital_gain = 0
                    long_term_capital_gain = 0
                    number_of_shares_left_to_find = number_of_shares_to_sell
                    looking_at_quarter = quarter - 4
                    while looking_at_quarter >= 0 and number_of_shares_left_to_find > 0:
                        shares_to_sell_from_this_quarter = min(number_of_shares_left_to_find,
                                                               self.asset_shares_by_quarter_purchased[source][looking_at_quarter])
                        if shares_to_sell_from_this_quarter > 0:
                            number_of_shares_left_to_find = number_of_shares_left_to_find - shares_to_sell_from_this_quarter
                            this_capital_gain =  shares_to_sell_from_this_quarter * (self.share_price_on_date[source][quarter] -
                                                                               self.share_price_on_date[source][looking_at_quarter])
                            long_term_capital_gain = long_term_capital_gain + this_capital_gain
                        looking_at_quarter = looking_at_quarter -1
                    looking_at_quarter = quarter
                    while looking_at_quarter >= 0 and looking_at_quarter > quarter - 4 and number_of_shares_left_to_find > 0:
                        shares_to_sell_from_this_quarter = min(number_of_shares_left_to_find,
                                                               self.asset_shares_by_quarter_purchased[source][looking_at_quarter])
                        if shares_to_sell_from_this_quarter > 0:
                            number_of_shares_left_to_find = number_of_shares_left_to_find - shares_to_sell_from_this_quarter
                            this_capital_gain = shares_to_sell_from_this_quarter * (self.share_price_on_date[source][quarter] -
                                                                               self.share_price_on_date[source][looking_at_quarter])
                            short_term_capital_gain = short_term_capital_gain + this_capital_gain
                        looking_at_quarter = looking_at_quarter - 1
                    if number_of_shares_left_to_find > 0.1:
                        raise Exception("%s shares of %s left to find to sell"%(number_of_shares_left_to_find, assetTypeToString(source)))
                
                    if (short_term_capital_gain > 0):
                        self.short_term_capital_gain_per_quarter.inc(quarter, short_term_capital_gain)
                        self.short_term_capital_gain_per_year.inc(year, short_term_capital_gain)

                    if (long_term_capital_gain > 0) :
                        self.long_term_capital_gain_per_quarter.inc(quarter, long_term_capital_gain)
                        self.long_term_capital_gain_per_year.inc(year, long_term_capital_gain)
                    elif long_term_capital_gain < 0:
                        self.totalLongTermCapitalLossState = self.totalLongTermCapitalLossState - long_term_capital_gain
                        self.totalLongTermCapitalLossFederal = self.totalLongTermCapitalLossFederal - long_term_capital_gain
                        tack(" (-%s long-term cap loss) "%(printCash(-long_term_capital_gain)))
                
                    if short_term_capital_gain > 0 and long_term_capital_gain > 0:
                        tack( " (%s short-term cap gain and %s long-term cap gain)"%(printCash(short_term_capital_gain),
                                                                                           printCash(long_term_capital_gain)))
                    elif short_term_capital_gain > 0:
                        tack( " (%s short-term cap gain)"%(printCash(short_term_capital_gain)))
                    elif long_term_capital_gain > 0:
                        tack( " (%s long-term cap gain)"%(printCash(long_term_capital_gain)))
                elif counts_totally_as_income:
                    self.dividends_per_quarter.inc(quarter, amount)
                    self.dividends_per_year.inc(year, amount)
                    if penalty_percentage > 0:
                        self.estimated_penalty_taxes_owed_per_quarter.inc(self.quarter + 1, amount * penalty_percentage)
                elif non_qualified_qtp:
                    
                    portion_taken_out = amount / (self.assetValue[AssetType.qtp_bond] + self.assetValue[AssetType.qtp_stock])
                    cost_basis_to_use = self.qtp_cost_basis * portion_taken_out
                    taxable_increase = max(amount - cost_basis_to_use, 0)
                    self.estimated_penalty_taxes_owed_per_quarter.inc(self.quarter + 1, taxable_increase * .1)
                    
                    self.dividends_per_quarter.inc(quarter, taxable_increase)
                    self.dividends_per_year.inc(year, taxable_increase)
                        
                    self.qtp_cost_basis = self.qtp_cost_basis - cost_basis_to_use
                        
                    
            
            
            else:
                
                qtp = [AssetType.qtp_stock, AssetType.qtp_bond]
                        
                if source in qtp and destination not in qtp:
                    self.qtp_cost_basis = self.qtp_cost_basis + amount
                    if -amount > self.amount_allowed_to_contribute_to_qtp()+0.5:
                        raise Exception("Trying to add %s to qtp when %s is allowed"%(-amount, self.amount_allowed_to_contribute_to_qtp()))
                    self.asset_shares[source] = self.asset_shares[source] - number_of_shares_to_sell
                    self.qtp_contributions_per_year.inc(self.year, -amount)
                    self.total_amount_contributed_to_qtp = self.total_amount_contributed_to_qtp + -amount
                else:
                    self.asset_shares[source] = self.asset_shares[source] - number_of_shares_to_sell
                    self.asset_shares_by_quarter_purchased[source][quarter] = self.asset_shares_by_quarter_purchased[source][quarter] - number_of_shares_to_sell
                
                
                        
                        
                
            
            
        
    def assetValue(self, assetType):
        return self.asset_shares[assetType] * self.share_price[assetType]
    def assets(self):
        return {assetType : self.assetValue(assetType) for assetType in self.asset_shares}
    
        
    def applyTransfer(self,action):
        #print "Applying transfer: %s [%s]"%(str(action), action.amount)
        if action.destination in LIST_OF_IRA_TYPES and action.source not in LIST_OF_IRA_TYPES:
            raise Exception("Cannot move unearned income into IRA")
        if self.assetValue(action.source)+1 < action.amount:
            raise Exception("Attempting to transfer %s %s, which is more than the available amount (%s)"%(printCash(action.amount),
                                                                                                          assetTypeToString(action.source),
                                                                                                          printCash(self.assetValue(action.source))))
        self.applySale(action.source, action.amount, action.destination)
        self.applySale(action.destination, -action.amount, action.source)
        
            
    def applyMultiplier(self,action):
        if action.source == AssetType.index_cost_of_living:
            self.qtp_yearly_contribution_limit = self.qtp_yearly_contribution_limit * action.multiplier
            self.inflation_multiplier = self.inflation_multiplier * action.multiplier
            self.qtp_maximum_investment = self.qtp_maximum_investment * action.multiplier
            self.cost_of_living = roundCash(self.cost_of_living * action.multiplier)
            self.kids_college_tuition = roundCash( self.kids_college_tuition * action.multiplier * action.multiplier)
            self.kids_college_living_edu = roundCash( self.kids_college_living_edu * action.multiplier)
            self.kids_college_living_misc = roundCash( self.kids_college_living_misc * action.multiplier)
            
            self.kids_expenses = roundCash(self.kids_expenses * action.multiplier)
            self.tax_adjustment = self.tax_adjustment *  action.multiplier
            self.SOCIAL_SECURITY_INCOME_QUARTERLY = roundCash(self.SOCIAL_SECURITY_INCOME_QUARTERLY* action.multiplier)
            self.capitalLossYearlyMaxState = roundCash(self.capitalLossYearlyMaxState * action.multiplier)
            self.capitalLossYearlyMaxFederal = roundCash(self.capitalLossYearlyMaxFederal * action.multiplier)

        elif action.source == AssetType.bond:
            self.share_price[AssetType.bond] = self.share_price[AssetType.bond] * action.multiplier
            self.share_price[AssetType.ira_bond] = self.share_price[AssetType.ira_bond] * action.multiplier
            self.share_price[AssetType.qtp_bond] = self.share_price[AssetType.qtp_bond] * action.multiplier
        elif action.source == AssetType.stock:
            self.share_price[AssetType.stock] = self.share_price[AssetType.stock] * action.multiplier
            self.share_price[AssetType.ira_stock] = self.share_price[AssetType.ira_stock] * action.multiplier
            self.share_price[AssetType.qtp_stock] = self.share_price[AssetType.stock] * action.multiplier 
        else:
            self.share_price[action.source] = self.share_price[action.source] * action.multiplier
            
    
        
    
    def estimate_of_state_taxes_so_far_this_year(self, fraction_of_year, long_term_capital_gains, short_term_capital_gains, dividends):
        long_term_capital_gains = max(long_term_capital_gains, 0)
        short_term_capital_gains = max(short_term_capital_gains, 0)
        dividends = max(dividends, 0)
        income_estimate = (short_term_capital_gains + dividends) / fraction_of_year
        long_term_capital_gains_estimate = long_term_capital_gains / fraction_of_year
        state_income_tax = (self.state_tax_from_income)(income_estimate, long_term_capital_gains_estimate, self.tax_adjustment)
        
        state_long_term_capital_gains_tax = (self.state_tax_from_long_term_capital_gains)(income_estimate, long_term_capital_gains_estimate, self.tax_adjustment)
        total_income = (short_term_capital_gains + dividends) + long_term_capital_gains
        total_tax = (state_income_tax + state_long_term_capital_gains_tax )*fraction_of_year
        
        return roundCash(total_tax)

    def estimate_of_federal_taxes_so_far_this_year(self, fraction_of_year, long_term_capital_gains, short_term_capital_gains, dividends):
        long_term_capital_gains = max(long_term_capital_gains, 0)
        short_term_capital_gains = max(short_term_capital_gains, 0)
        dividends = max(dividends, 0)
        income_estimate = (short_term_capital_gains + dividends) / fraction_of_year
        long_term_capital_gains_estimate = long_term_capital_gains / fraction_of_year
        
        federal_income_tax = (self.federal_tax_from_income)(income_estimate, self.tax_adjustment)
        federal_long_term_capital_gains_tax = (self.federal_tax_from_long_term_capital_gains)(income_estimate, long_term_capital_gains_estimate, self.tax_adjustment)
        total_income = (short_term_capital_gains + dividends) + long_term_capital_gains
        
        
        total_tax = (federal_income_tax  + federal_long_term_capital_gains_tax)*fraction_of_year
        
        return roundCash(total_tax)
    
    def estimate_state_taxes(self):
        number_of_quarters_in_consideration = (self.quarter_of_year % 4) + 1
        fraction_of_year = (float(number_of_quarters_in_consideration)) / 4.0
        long_term_capital_gains = self.long_term_capital_gain_per_year.get(self.year)
        long_term_capital_gains_before_capital_loss_application = long_term_capital_gains
        long_term_capital_loss_application = min(long_term_capital_gains, self.capitalLossYearlyMaxState, self.totalLongTermCapitalLossState)
        short_term_capital_gains = self.short_term_capital_gain_per_year.get(self.year)
        dividends = self.dividends_per_year.get(self.year)
        
        long_term_capital_gains = long_term_capital_gains - long_term_capital_loss_application
                
        estimate_of_taxes = self.estimate_of_state_taxes_so_far_this_year(fraction_of_year, long_term_capital_gains, short_term_capital_gains, dividends)
        if number_of_quarters_in_consideration == 4:
            total_tax = (short_term_capital_gains+dividends+long_term_capital_gains_before_capital_loss_application- long_term_capital_loss_application)
            if total_tax == 0:
                effectiveTaxRate = "N/A"
            else:
                effectiveTaxRate = "%s%%"%(int(100*estimate_of_taxes/total_tax ))
            self.totalLongTermCapitalLossState = self.totalLongTermCapitalLossState - long_term_capital_loss_application
            log("%s Year State   Tax Summary: Long-Term Cap Gain: %s - %s   Income:  %s   Yearly State Tax: %s  (%s)   Carry For. Cap. Loss:%s"%(self.year, printCash(long_term_capital_gains_before_capital_loss_application),printCash(long_term_capital_loss_application), printCash(dividends + short_term_capital_gains ) , printCash(estimate_of_taxes),effectiveTaxRate,printCash(self.totalLongTermCapitalLossState)))
        
        if estimate_of_taxes < 0:
            estimate_of_taxes = 0
        previous_quarter_to_subtract = self.quarter 
        previous_quarter_of_year_to_subtract = self.quarter_of_year 
        while previous_quarter_of_year_to_subtract >= 0 and previous_quarter_to_subtract >= 0 :
            prev_paid = self.estimated_taxes_paid_per_quarter.get(previous_quarter_to_subtract)
            #log("subtracting %s from estimated taxes (paid Q%s (quarter %s))"%(prev_paid, previous_quarter_of_year_to_subtract + 1, previous_quarter_to_subtract))
            estimate_of_taxes = estimate_of_taxes - prev_paid
            previous_quarter_to_subtract = previous_quarter_to_subtract - 1
            previous_quarter_of_year_to_subtract = previous_quarter_of_year_to_subtract - 1
        estimate_of_taxes = max(estimate_of_taxes, 0)
        return roundCash(estimate_of_taxes)

    def estimate_federal_taxes(self):
        number_of_quarters_in_consideration = (self.quarter_of_year % 4) + 1
        fraction_of_year = (float(number_of_quarters_in_consideration)) / 4.0
        long_term_capital_gains = self.long_term_capital_gain_per_year.get(self.year)
        long_term_capital_gains_before_capital_loss_application = long_term_capital_gains
        long_term_capital_loss_application = min(long_term_capital_gains, self.capitalLossYearlyMaxFederal, self.totalLongTermCapitalLossFederal)
        short_term_capital_gains = self.short_term_capital_gain_per_year.get(self.year)
        dividends = self.dividends_per_year.get(self.year)
        
        long_term_capital_gains = long_term_capital_gains - long_term_capital_loss_application
        
        estimate_of_taxes = self.estimate_of_federal_taxes_so_far_this_year(fraction_of_year, long_term_capital_gains, short_term_capital_gains, dividends)
        if number_of_quarters_in_consideration == 4:
            total_income = (short_term_capital_gains+dividends+long_term_capital_gains_before_capital_loss_application- long_term_capital_loss_application)
            if total_income == 0:
                effectiveTaxRate = "N/A"
            else:
                effectiveTaxRate = "%s%%"%(int(100*estimate_of_taxes/total_income ))
            self.totalLongTermCapitalLossFederal = self.totalLongTermCapitalLossFederal - long_term_capital_loss_application
            log("%s Year Federal Tax Summary: Long-Term Cap Gain: %s - %s   Income:  %s   Yearly Federal Tax: %s  (%s)   Carry For. Cap. Loss:%s"%(self.year, printCash(long_term_capital_gains_before_capital_loss_application),printCash(long_term_capital_loss_application), printCash(dividends + short_term_capital_gains ) , printCash(estimate_of_taxes),effectiveTaxRate ,printCash(self.totalLongTermCapitalLossFederal)))
        
        if estimate_of_taxes < 0:
            estimate_of_taxes = 0
        previous_quarter_to_subtract = self.quarter
        previous_quarter_of_year_to_subtract = self.quarter_of_year
        while previous_quarter_of_year_to_subtract >= 0 and previous_quarter_to_subtract >= 0 :
            prev_paid = self.estimated_taxes_paid_per_quarter.get(previous_quarter_to_subtract)
            #log("subtracting %s from estimated taxes (paid Q%s (quarter %s))"%(prev_paid, previous_quarter_of_year_to_subtract + 1, previous_quarter_to_subtract))
            estimate_of_taxes = estimate_of_taxes - prev_paid
            previous_quarter_to_subtract = previous_quarter_to_subtract - 1
            previous_quarter_of_year_to_subtract = previous_quarter_of_year_to_subtract - 1
        estimate_of_taxes = max(estimate_of_taxes, 0)
        return roundCash(estimate_of_taxes)
            
    def applyDividend(self, action):
        def _internalApplyDividend(self, source, dividend):
            number_of_shares = self.asset_shares[source]
            dividend_amount = number_of_shares * dividend * self.share_price[source]
            if source not in TAX_ADVANTAGED_ASSET_TYPES:
                self.dividends_per_year.inc(self.year, dividend_amount)
                self.dividends_per_quarter.inc(self.quarter, dividend_amount)
                if dividend_amount  > 0:
                    tack(" (%s of taxable income)"%( printCash(dividend_amount)))
            if self.reinvest_dividends:
                dest = source
            else:
                if source in LIST_OF_IRA_TYPES:
                    dest = AssetType.ira_cash
                elif source in LIST_OF_QTP_TYPES:
                    dest = AssetType.qtp_cash
                else:
                    dest = AssetType.cash
            self.applySale(dest, -dividend_amount, dest)
        if action.source == AssetType.bond:
            ts = [AssetType.bond, AssetType.ira_bond, AssetType.qtp_bond]
        elif action.source == AssetType.stock:
            ts = [AssetType.stock, AssetType.ira_stock, AssetType.qtp_stock]
        else:
            ts = [action.source]
        for t in ts:
            _internalApplyDividend(self, t, action.relative_dividend)
        
        
   
    
    
    def years_of_living_expenses(self, years):

        qtp_expenses = 0
        other_expenses = 0
        fake_age_years = self.age_years
        fake_age_quarters = self.age_quarters
        fake_quarter = self.quarter
        cost_of_living_multiplier = 1.0
        cost_of_college_multiplier = 1.0
        for i in range(years * 4):
            fake_quarter = fake_quarter + 1
            fake_age_quarters = fake_age_quarters + 1
            if fake_age_quarters == 4:
                fake_age_quarters = 0
                fake_age_years = fake_age_years + 1
            cost_of_living_multiplier = cost_of_living_multiplier * 1.008374761
            cost_of_college_multiplier = cost_of_college_multiplier * 1.008374761 * 1.008374761
            
            other_expenses = other_expenses + self.cost_of_living * cost_of_living_multiplier
            
            if fake_quarter == 0:
                other_expenses  = other_expenses + self.INITIAL_HOUSE_PAYMENT
            if fake_quarter < self.quarters_to_pay_mortgage:
                other_expenses = other_expenses + self.quarterly_mortgage_payment
            
            if fake_age_years >= self.env.AGE_OF_KIDS and fake_age_years < self.env.AGE_OF_KIDS + 18:
                other_expenses = other_expenses + self.kids_expenses * cost_of_living_multiplier
            elif fake_age_years >= self.env.AGE_OF_KIDS + 18 and fake_age_years < self.env.AGE_OF_KIDS + 22:
                qtp_expenses = qtp_expenses +  self.kids_college_tuition * cost_of_college_multiplier
                qtp_expenses = qtp_expenses + self.kids_college_living_edu * cost_of_living_multiplier
                other_expenses = other_expenses + self.kids_college_living_misc * cost_of_living_multiplier
        retval = [other_expenses, qtp_expenses]
                    #print "Returnning %s"%(retval)
        return retval
    
    
    def total_expenditures_required_this_quarter(self):
        if self.quarter in self.needed_spend_by_quarter:
            return self.needed_spend_by_quarter[self.quarter]
        expenses = {}
        expenses[AssetType.spend_taxes_state] = self.estimated_state_taxes_owed_per_quarter.get(self.quarter)
        expenses[AssetType.spend_taxes_federal] = self.estimated_federal_taxes_owed_per_quarter.get(self.quarter)
        expenses[AssetType.spend_taxes_penalty] = self.estimated_penalty_taxes_owed_per_quarter.get(self.quarter)
    
        if self.quarter >= self.env.YEARS_TO_WAIT * 4:
            expenses[AssetType.spend_living_expenses] = self.cost_of_living
    
        if self.quarter == self.env.YEARS_TO_WAIT * 4:
            expenses[AssetType.spend_down_payment_on_house]  = self.INITIAL_HOUSE_PAYMENT
        if self.quarter < self.quarters_to_pay_mortgage + self.env.YEARS_TO_WAIT * 4:
            expenses[AssetType.spend_mortgage_payment_on_house] = self.quarterly_mortgage_payment
    
        if self.age_years >= self.env.AGE_OF_KIDS and self.age_years < self.env.AGE_OF_KIDS + 18:
            expenses[AssetType.spend_kids_expenses] = self.kids_expenses
        elif self.age_years >= self.env.AGE_OF_KIDS + 18 and self.age_years < self.env.AGE_OF_KIDS + 22:
            expenses[AssetType.spend_kids_college_tuition] = self.kids_college_tuition
            expenses[AssetType.spend_kids_college_edu] = self.kids_college_living_edu
            expenses[AssetType.spend_kids_college_misc] = self.kids_college_living_misc


        self.needed_spend_by_quarter[self.quarter] = expenses
        return expenses
    def kids_are_done_with_college(self):
        return self.age_years >= self.env.AGE_OF_KIDS + 22
    def dollar_amount_of_total_expenditures_required_this_quarter(self):
        return sum(self.total_expenditures_required_this_quarter().values())
                
    
    def total_assets(self):
        return roundCash(sum([self.asset_shares[t] * self.share_price[t] for t in  LIST_OF_ASSET_TYPES]))
        
        
    def applyAdvanceQuarter(self,action):
        if self.SOCIAL_SECURITY_ENABLED == 1:
            if self.age_years >= self.AGE_SOCIAL_SECUIRTY_STARTS:
                self.asset_shares[AssetType.cash] = self.asset_shares[AssetType.cash] + self.SOCIAL_SECURITY_INCOME_QUARTERLY
                log("Recieved %s in SS benefits"% printCash(self.SOCIAL_SECURITY_INCOME_QUARTERLY))
        log("  ")
        
        quarter = self.quarter
        
        for expense_type, amount_required in self.total_expenditures_required_this_quarter().iteritems():
            if expense_type  in self.total_expenditures_spent_this_quarter:
                amount_paid = self.total_expenditures_spent_this_quarter[expense_type]
            else:
                amount_paid = 0
            
            if not close_enough(amount_paid, amount_required):
                raise Exception("Incorrect %s. (Need %s, paid %s)"%(assetTypeToString(expense_type), printCash(amount_required), printCash(amount_paid)))

        self.estimated_state_taxes_owed_per_quarter.set(quarter+1, self.estimate_state_taxes())
        self.estimated_federal_taxes_owed_per_quarter.set(quarter+1, self.estimate_federal_taxes())
                
        self.age_quarters = self.age_quarters + 1
        if self.age_quarters == 4:
            self.age_quarters = 0
            self.age_years = self.age_years + 1
            
            
            
        for at in LIST_OF_ASSET_TYPES:
            self.asset_shares_by_quarter_purchased[at].append(0)
            self.share_price_on_date[at].append(self.share_price[at])
            
        self.quarter = self.quarter + 1
        self.quarter_of_year = self.quarter_of_year + 1
        if self.quarter_of_year % 4 == 0:
            self.year = self.year + 1
            self.quarter_of_year = 0
        self.total_expenditures_spent_this_quarter = {}
            
            
        
    ApplyActionCaseStatement = {ActionType.transfer : applyTransfer,
                                ActionType.multiplier : applyMultiplier,
                                ActionType.dividend : applyDividend,
                                ActionType.advanceQuarter : applyAdvanceQuarter}
    
    def applyActions(self, actions):
        for action in actions:
            (self.ApplyActionCaseStatement[action.action_type])(self, action)
                
        
        
    


    
