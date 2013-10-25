from PRNG import *
from Parameters import *

chance_of_man_dying_at_age_dict = {}
chance_of_woman_dying_at_age_dict = {}

yearly_percentage_improvement_at_age = {}


max_age_seen = 0

def chance_of_man_dying_at_age(age, years_into_the_future):
    return chance_of_man_dying_at_age_dict[min(age, max_age_seen)] * (( 1 - yearly_percentage_improvement_at_age[min(age, max_age_seen)]) ** years_into_the_future )

def chance_of_woman_dying_at_age(age, years_into_the_future):
    return chance_of_woman_dying_at_age_dict[min(age, max_age_seen)] * (( 1 - yearly_percentage_improvement_at_age[min(age, max_age_seen)]) ** years_into_the_future )




        

with open("actuarial_life_expectancy_tables.txt") as f:
    content = f.readlines()

    for line in content:
        
        tokens = line.split()
        age = int(tokens[0])
        chance_of_man_dying = float(tokens[1])
        chance_of_woman_dying = float(tokens[4])
        chance_of_man_dying_at_age_dict[age] = chance_of_man_dying
        chance_of_woman_dying_at_age_dict[age] = chance_of_woman_dying
        max_age_seen = max(max_age_seen, age)

with open("yearly_improvement_in_mortality_by_age.csv") as f:
    content = f.readlines()

    for all in content:
      lines = all.split("\r")
      for line in lines:
        tokens = line.split(",")

        percentage_improvement = float(tokens[0])
        begin_age = int(tokens[1])
        while begin_age > len(yearly_percentage_improvement_at_age):
            age_to_consider = len(yearly_percentage_improvement_at_age)

            yearly_percentage_improvement_at_age[age_to_consider] =previous_percentage_improvement
        
        previous_percentage_improvement = percentage_improvement

    while max_age_seen > len(yearly_percentage_improvement_at_age):
        age_to_consider = len(yearly_percentage_improvement_at_age)
        yearly_percentage_improvement_at_age[age_to_consider] =previous_percentage_improvement


def lifeExpectancy(seed):
    prng = PRNG(seed)
    man_alive = True
    woman_alive = True
    age = INITIAL_AGE_YEARS
    years_into_the_future = 0
    while man_alive or woman_alive:
        if man_alive and prng.rand_unit() < chance_of_man_dying_at_age(age, years_into_the_future):
            man_alive = False
        if woman_alive and prng.rand_unit() < chance_of_woman_dying_at_age(age, years_into_the_future):
            woman_alive = False
        age = age + 1
        years_into_the_future = years_into_the_future + 1

    
    return age 







