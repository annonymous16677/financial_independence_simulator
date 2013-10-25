def principle_remaining_after(principle, interest, months_paid, monthly_payment):
    for i in range(months_paid):
        principle = principle * (1 + interest / 1200.0)
        principle = principle - monthly_payment
    return principle

def quarterly_interest_payment(principle, interest, months_paid, monthly_payment):
    principle_remaining_1 = principle_remaining_after(principle, interest, months_paid, monthly_payment)
    monthly_interest_payment_1 = principle_remaining_1 * (interest / 1200.0)
    principle_remaining_2 = principle_remaining_after(principle, interest, months_paid+1, monthly_payment)
    monthly_interest_payment_2 = principle_remaining_1 * (interest / 1200.0)
    principle_remaining_3 = principle_remaining_after(principle, interest, months_paid+2, monthly_payment)
    monthly_interest_payment_3 = principle_remaining_1 * (interest / 1200.0)
    return monthly_interest_payment_1 + monthly_interest_payment_2 + monthly_interest_payment_3