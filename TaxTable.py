import math

def tax_amount_from_tax_table(income, table, tax_adjustment):
    if income < 0:
        return 0
    previous_bracket = [0, 0]
    index = 0
    total_tax = 0
    while True:
        bracket = table[index]
        if len(bracket) > 1:
            bracket = [bracket[0], bracket[1] * tax_adjustment]
        if len(bracket) == 1:
            total_tax = total_tax + (bracket[0] * (income - (previous_bracket[1])))
            return total_tax
        else:
            total_tax = total_tax + bracket[0] * (min(income, bracket[1]) - previous_bracket[1])
        if bracket[1] >= income:
            return total_tax
        previous_bracket = bracket
        index = index + 1