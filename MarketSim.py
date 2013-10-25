from Market import *
from HistoricState import *
from Parameters import *
from Asset import *
from Strategy import *
from Environment import *
from Log import log, tack
from MultiThread import *
from printCash import *
import math


def calulate_one_round(parameters, input_key):
    env = parameters["env"]
    strategy = parameters["strat"]
    [solvency, age, ending_cash] = applyStrategyToMarket(strategy, Market(input_key), env)
    return 1 if solvency else 0

def strategyScore(strategy, env, N):
    parameters = {"strat": strategy,
                  "env": env
                  }
    
    successes = successesForRunFunctionWithParameters(calulate_one_round, parameters, N)
    

    return int((1000*successes) / N) / 10

def score(successes):
    
    return sum(successes) / float(len(successes))

def nextGuess(lower_bound, upper_bound, precision):
    #if upper_bound - lower_bound <= precision:
        #x = int(upper_bound / (precision / 2)) *  (precision / 2)
        
        #print "l = %s  u = %s  x = %s  p = %s"%(str(lower_bound), str(upper_bound), str(x), str(precision))
    #return x
    return float(lower_bound + upper_bound) / 2
    

def optimizeParameter(strategy, env, N, chance, isStrategyParameter, parameterName, range, precision):
    chance = chance / 100.0
    lower_bound = range[0]
    upper_bound = range[1]

    parameters = {"strat": strategy,
                  "env": env
                  }

    lower_successes = runFunctionWithParameters(calulate_one_round, parameters, N, parameterName = parameterName, parameterValue = lower_bound)
    upper_successes = runFunctionWithParameters(calulate_one_round, parameters, N, parameterName = parameterName, parameterValue = upper_bound)
    lower_score = score(lower_successes)
    upper_score = score(upper_successes)
    
    if lower_score < chance and upper_score < chance:
        print "%s range, too low of a chance"%(range)
        return 0
    if lower_score < chance and upper_score < chance:
        print "%s range, too high of a chance"%(range)
        return 0
    if lower_score == chance and upper_score == chance:
        print "flat"
        return nextGuess(lower_bound, upper_bound, precision)
    if lower_score == chance:
        return lower_bound
    if upper_score == chance:
        return upper_buound
    if upper_score > lower_score:
        increasing = True
    else:
        increasing = False

    marker_success = {}
    
    for i in xrange(N):
        low_s = lower_successes[i]
        high_s = upper_successes[i]
        if (low_s < high_s and not increasing) or (low_s > high_s and increasing): raise Exception()
        if increasing:
            if low_s:
                marker_success[i] = 1
            elif high_s:
                marker_success[i] = 0
            else:
                marker_success[i] = -1
        else:
            if high_s:
                marker_success[i] = 1
            elif low_s:
                marker_success[i] = 0
            else:
                marker_success[i] = -1




    while upper_bound - lower_bound >= precision/2:
        
        guess = nextGuess(lower_bound, upper_bound, precision)
        guess_successes = runFunctionWithParameters(calulate_one_round, parameters, N, parameterName = parameterName, parameterValue = guess, marker_success = marker_success)
        
        guess_score = score(guess_successes)

        if (guess_score >= chance and increasing) or (guess_score <= chance and not increasing):
            upper_bound = guess
        else:
            lower_bound = guess

        if increasing:
            if guess_score >= chance:
                chuck = [0,-1]
            else:
                chuck = [1, 1]
        else:

            if guess_score <= chance:
                chuck = [1, 1]
            else:
                
                chuck = [0,-1]
            

        for i in xrange(N):
            if guess_successes[i] == chuck[0]:
                marker_success[i] = chuck[-1]
        
            
    
    
    return round((lower_bound+upper_bound)/2.0 / precision) * precision




def initialCashRequired(strategy, env, N, chance):
    return optimizeParameter(strategy, env, N, chance, False, "STARTING_CASH_IN_THOUSANDS", [0,10000], 1) * 1000

def spending_allowed(strategy, env, N, chance):
    return optimizeParameter(strategy, env, N, chance, False, "COST_OF_LIVING_IN_THOUSANDS", [0,500], 0.1) * 1000
        
    

def applyStrategyToMarket(strategy, market, env):
    historic_state = HistoricState(env.STARTING_CASH_IN_THOUSANDS * 1000, MarketState(), strategy, env)
    bankrupt = False
    
    log( """Apply strategy "%s" to "%s" in environment %s."""%(strategy, market, env.name()))
    log( """=======================================""")
    log("")
    
    log( historic_state.currentStateString())
    while True:
        if strategy.should_strategy_declare_bankruptcy_this_quarter(historic_state):
            bankrupt = True
            ending_cash = 0
            expenses = historic_state.total_expenditures_required_this_quarter()
            exp_str  = " , ".join(["%s:%s"%(assetTypeToString(t), printCash(expenses[t]) ) for t in  expenses if expenses[t] > 0.01])
            
            log(" Required Expenses: %s (%s total)"%(exp_str, printCash(historic_state.dollar_amount_of_total_expenditures_required_this_quarter() )))
            log( "Declaring Bankruptcy")
            break
        if market.quarter >= (market.life_expectancy*4 - (INITIAL_AGE_YEARS * 4 + INITIAL_AGE_QUARTERS)):
            bankrupt = False
            ending_cash = historic_state.total_assets()
            log( "Died happy at %s years old with %s (equivalent to %s in %s dollars)"%(market.life_expectancy, printCash(ending_cash), printCash(ending_cash / historic_state.inflation_multiplier), INITIAL_YEAR))
            break
        
        strategy_actions = strategy.actions_for_quarter(historic_state)
        market_actions = market.actions_for_current_quarter()
        
        for action in strategy_actions:
            s = action.__str__()
            if s:
                log( s)
            historic_state.applyActions([action])
        log("")
        for action in market_actions:
            s = action.__str__()
            if s:
                log( s)
            historic_state.applyActions([action])
        market.advance_quarter()
        log("")
        log("----------")
        log( historic_state.currentStateString())
        log("")
    age = (market.quarter +  INITIAL_AGE_QUARTERS + INITIAL_AGE_YEARS * 4 ) / 4
    
    log( """===================================================================""")
    
    return [not bankrupt, age, ending_cash]
    
    
def test_all_strategies():
    LIST_OF_STRATEGIES = [all_sp500_strategy()]
    for strategy in LIST_OF_STRATEGIES:
        for env in list_of_environments:
            score = strategyScore(strategy, env, NUMBER_OF_TRIALS)
            name = strategy.name()
            env_name = env.name()
            print "%s in %s: %s%%"%(name, env_name, score)
            
def cash_required_for_all_strategies(chance):
    min_cash = None
    min_strat = None
    mapping_of_env_to_strat = {}
    for env in list_of_environments:
        min_cash = None
        for strategy in LIST_OF_STRATEGIES:
            cash = initialCashRequired(strategy, env, NUMBER_OF_TRIALS, chance)
            name = strategy.name()
            env_name = env.name()
            
            if not min_cash or cash < min_cash:
                min_cash = cash
                min_strat = strategy
                min_env = env
            print "%s in %s: %s required for %s%% solvency"%(name, env_name, printCash( cash), chance)
            
        mapping_of_env_to_strat[env] = [min_strat, min_cash]
    print "==="
    for env in list_of_environments:
        [min_strat, min_cash] = mapping_of_env_to_strat[env]
        print """In "%s", best for %s%% solvency is %s: %s required """%(env.name(), chance, min_strat.name(), printCash(min_cash))
    print "    "

def allowed_spending(chance):
    min_cash = None
    min_strat = None
    mapping_of_env_to_strat = {}
    for env in list_of_environments:
        min_cash = None
        for strategy in LIST_OF_STRATEGIES:
            cash = spending_allowed(strategy, env, NUMBER_OF_TRIALS, chance)
            cash = round(cash / 100)*100
            name = strategy.name()
            env_name = env.name()
            
            if not min_cash or cash > min_cash:
                min_cash = cash
                min_strat = strategy
                min_env = env
            print "%s in %s: %s/yr salary allowed for %s%% solvency"%(name, env_name, printCash( cash), chance)
        
        mapping_of_env_to_strat[env] = [min_strat, min_cash]
    print "==="
    for env in list_of_environments:
        [min_strat, min_cash] = mapping_of_env_to_strat[env]
        print """In "%s", best for %s%% solvency is %s: %s/yr allowed """%(env.name(), chance, min_strat.name(), printCash(min_cash))
    print "    "

def run_simulation():
    if DEBUG == 1:
        one_strat()
    else:
        best_strat()

def one_strat():
    #strategy = percentage_in_bonds( bond_percentage = 10, mortgage_length = 30, qualified_tuition_plan = 400000)

    strategy = years_of_living_expenses_in_bonds( years_of_living_expenses_in_bonds = 4, mortgage_length = 30, qualified_tuition_plan = 400000)
    applyStrategyToMarket(strategy, Market(START_TRIAL), env)

def best_strat():
#   env = list_of_environments[0]
#   strategy = percentage_in_bonds(20)
    
#score = strategyScore(strategy, env, 100)
    #print """Strategy "%s" has %s%% success probability."""%(strategy, score)
    #for p in range(5,100,5):
    #cash_required_for_all_strategies(80)
    #for years in range(10,100,10):
        
    #print "Set regime to %s years"%(years)

    #cash_required_for_all_strategies(80)
    #cash_required_for_all_strategies(90)

    #allowed_spending(80)
    allowed_spending(90)

    #allowed_spending(99)

    #cash_required_for_all_strategies(95)
    #cash_required_for_all_strategies(98)
#cash_required_for_all_strategies(99)
setQuarters(40*3)