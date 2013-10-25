from TaxTable import *
from printCash import *
standard_federal_deduction = 12200
def federal_tax_from_income(income, tax_adjustment):
    deduction_used = standard_federal_deduction * tax_adjustment
    income_tax_table = [
                      [.10, 17850],
                         [.15, 72500],
                         [.25, 146400],
                         [.28, 223050],
                         [.33, 398350],
                         [.35, 450000],
                        [.396]]
    tax = tax_amount_from_tax_table(income-deduction_used, income_tax_table, tax_adjustment)
    #print "income = %s    tax_adjustment = %s  income tax = %s"%(printCash(income),  (tax_adjustment), printCash(tax))
    return tax
    

def federal_tax_from_long_term_capital_gains(income, long_term_capital_gains, tax_adjustment):
    deduction_used = standard_federal_deduction * tax_adjustment
    long_term_cap_gain_tax_table = [
                        [0, 17850],
                        [0, 72500],
                        [.15, 146400],
                        [.15, 223050],
                        [.15+.038, 250000],#+3.8%  Thanks Obama
                        [.15+.038, 398350],
                        [.15+.038, 450000],
                        [.20+.038]]
    income_before_cap_gain = income-deduction_used
    income_after_cap_gain = income_before_cap_gain + long_term_capital_gains
    base = tax_amount_from_tax_table(income_after_cap_gain,  long_term_cap_gain_tax_table, tax_adjustment) 
    subbend = tax_amount_from_tax_table(income_before_cap_gain, long_term_cap_gain_tax_table, tax_adjustment)
    tax =base - subbend
    #print "income = %s  long_term_capital_gains = %s  tax_adjustment = %s  base = %s  subbend = %s cap.gain. tax = %s"%(printCash(income), printCash(long_term_capital_gains), (tax_adjustment),printCash( base), printCash(subbend), printCash(tax))

    return tax
    
        

