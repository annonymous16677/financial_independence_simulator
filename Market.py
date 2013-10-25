from PRNG import PRNG
from Parameters import *
from Action import *
import csv
from Asset import *
from LifeExpectancy import *

LENGTH_OF_REGIMES_IN_QUARTERS_LOWER = 0
LENGTH_OF_REGIMES_IN_QUARTERS_UPPER = 0


def setYears(years):
    setQuarters(years*4)
def setQuarters(quarters):
    global LENGTH_OF_REGIMES_IN_QUARTERS_LOWER
    global LENGTH_OF_REGIMES_IN_QUARTERS_UPPER
    LENGTH_OF_REGIMES_IN_QUARTERS_LOWER = quarters
    LENGTH_OF_REGIMES_IN_QUARTERS_UPPER = quarters

    

class HistoricData:
    def __init__(self):
        self.quarters = {}
        self.min_quarter = None
        self.max_quarter = None
    def addData(self, quarter, key, value):
        if quarter not in self.quarters:
            self.quarters[quarter] = {}
        quarter_dict = self.quarters[quarter]
        quarter_dict[key] = value
        if (not self.min_quarter) or quarter < self.min_quarter:
            self.min_quarter = quarter
        if (not self.max_quarter) or quarter > self.max_quarter:
            self.max_quarter = quarter
    def getData(self,quarter, key):
        if quarter not in self.quarters:
            return None
        if key not in self.quarters[quarter]:
            return None
        return self.quarters[quarter][key]
    def quarterData(self, quarter):
        if quarter not in self.quarters:
            return None
        return self.quarters[quarter]
    
historicData = HistoricData()

    
        
   
    
SP500_RELATIVE_DIVIDEND_KEY = "SPRD"
SP500_RELATIVE_MULTIPLE_KEY = "SPRM"
BOND_RELATIVE_MULTIPLE_KEY = "BRM"
BOND_RELATIVE_DIVIDEND_KEY= "BRD"
INFLATION_KEY = "I"

keys = [SP500_RELATIVE_DIVIDEND_KEY, SP500_RELATIVE_MULTIPLE_KEY, INFLATION_KEY, BOND_RELATIVE_DIVIDEND_KEY, BOND_RELATIVE_MULTIPLE_KEY]

def doWeHaveAllKeysFor(quarter):
    
    for k in keys:
        if historicData.getData(quarter,k) == None:
            return False
    return True


    



def readSP500fromFile():
    sp500filename = "SP500.csv"
    csv_reader = csv.reader(open(sp500filename, 'rU'))
    first = True
    for row in csv_reader:
        if first:
            first = False
        else:
            [year_str, price_multiplier, relative_dividend] = [row[0], float(row[1]), float(row[2])]
            [year, quarter_str] = year_str.split('-')
            
            year_int = int(year)
            quarter_int = int(quarter_str[1])-1
            historicData.addData(year_int * 4 + quarter_int, SP500_RELATIVE_DIVIDEND_KEY, relative_dividend)
            historicData.addData(year_int * 4 + quarter_int, SP500_RELATIVE_MULTIPLE_KEY, price_multiplier)
readSP500fromFile()

def readInflationFromFile():
    inflation_filename = "Inflation.csv"
    for row in csv.reader(open(inflation_filename, 'rU')):
        year = int(row[0])
        for quarter in range(0,4):
            index = quarter+1
            if len(row) > index and len(row[index]) > 0:
                
                inflation = float(row[index])
                historicData.addData(year * 4 + quarter, INFLATION_KEY, inflation)
readInflationFromFile()

def readBondFromFile():
    bond_filename = "Bond.csv"
    for row in csv.reader(open(bond_filename, 'rU')):
        year = int(row[0])
        for quarter in range(0,4):
            index = quarter+1
            if len(row) > index and len(row[index]) > 0:
                bond_return_multiplier = float(row[index])
                if (bond_return_multiplier > 1):
                    bond_dividend = (bond_return_multiplier - 1) / 2
                    bond_multiplier = bond_return_multiplier - bond_dividend

                else:
                    bond_multiplier = bond_return_multiplier
                    bond_dividend = 0

                historicData.addData(year * 4 + quarter, BOND_RELATIVE_MULTIPLE_KEY, bond_multiplier)
                historicData.addData(year * 4 + quarter, BOND_RELATIVE_DIVIDEND_KEY, bond_dividend)
                
readBondFromFile()


def nextQuarter(currentQuarter):
    return currentQuarter + 1
        
def prevQuarter(currentQuarter):
    return currentQuarter -1

def rangeOfFullData():
    min_q = historicData.min_quarter
    max_q = historicData.max_quarter
    current_q = max_q
    while True:
        if doWeHaveAllKeysFor(current_q):
            break
        current_q = prevQuarter(current_q)
    maxFullData = current_q
    while True:
        if not doWeHaveAllKeysFor(current_q):
            break
        current_q = prevQuarter(current_q)
    doWeHaveAllKeysFor(current_q)
    minFullData = nextQuarter(current_q)
    return [minFullData, maxFullData]
range_of_full_data = rangeOfFullData()    

    
                
                
        



class Market:
    def __init__(self, seed):
        self.seed = seed
        self.prng = PRNG(seed)
        self.quarter = 0
        self.quarter_data = []
        self.life_expectancy = lifeExpectancy(seed + 1000000)
        while len(self.quarter_data) < (self.life_expectancy * 4 - INITIAL_AGE_YEARS * 4 - INITIAL_AGE_QUARTERS):
            self.extend_regime()
    
        
    def quarterlyActions(self):
        self.actions_for_current_quarter()
        
    def advance_quarter(self):
        self.quarter = self.quarter + 1
    
    def __str__(self):
        return "Market #%s"%(str(self.seed))
        
    def extend_regime(self):
        ran = self.range_of_new_regime()
        for quarter in ran:
            x = historicData.quarterData(quarter)
            self.quarter_data.append(x)
        
                
    def range_of_new_regime(self):
        
        
        max_quarter = range_of_full_data[1]
        min_quarter = range_of_full_data[0]
            
        
        
        l = self.length_of_new_regime()
        start = self.prng.random_in_range(min_quarter, max_quarter-l)
        r = range(start, start+l)
        
        #years = (float(start)/4, float(start+l)/4)
        #print "years = %s"%(str(years))
        
        return r
    def length_of_new_regime(self):
        min_quarter = range_of_full_data[0]
        max_quarter = range_of_full_data[1]
        number_of_quarters = max_quarter - min_quarter + 1
        totalPool = 0
        for i in range(LENGTH_OF_REGIMES_IN_QUARTERS_LOWER, LENGTH_OF_REGIMES_IN_QUARTERS_UPPER+1):
            totalPool = totalPool + (1+number_of_quarters - i)
        index = self.prng.random_in_range(0,totalPool-1)
        original_index = index
        for i in range(LENGTH_OF_REGIMES_IN_QUARTERS_LOWER, LENGTH_OF_REGIMES_IN_QUARTERS_UPPER+1):
            index = index - (1+number_of_quarters - i)
            if index < 0:
                return i
        pass
        
        
        
    def actions_for_current_quarter(self):
        data = self.quarter_data[self.quarter]
        actions = []
        actions.append(Action(ActionType.multiplier, source = AssetType.index_cost_of_living, multiplier = data[INFLATION_KEY]))
        actions.append(Action(ActionType.multiplier, source = AssetType.stock, multiplier = data[SP500_RELATIVE_MULTIPLE_KEY]))
        actions.append(Action(ActionType.dividend, source = AssetType.stock, relative_dividend = data[SP500_RELATIVE_DIVIDEND_KEY]))
        
        actions.append(Action(ActionType.multiplier, source = AssetType.bond, multiplier = data[BOND_RELATIVE_MULTIPLE_KEY]))
        actions.append(Action(ActionType.dividend, source = AssetType.bond, relative_dividend = data[BOND_RELATIVE_DIVIDEND_KEY]))
        
        
        actions.append(Action(ActionType.advanceQuarter))
        return actions
               

