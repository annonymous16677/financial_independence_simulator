import multiprocessing
from multiprocessing import Pool, cpu_count
import math
from Parameters import START_TRIAL, MULTI_THREAD

pool_size = multiprocessing.cpu_count()


def functionToIterate((function, parameters, iteration, marker_success)):
    if marker_success:
        if marker_success[iteration] == -1:
            return 0
        elif marker_success[iteration] == 1:
            return 1
    return  function(parameters, iteration + START_TRIAL)



def runFunctionWithParameters(function, parameters, number_of_times, parameterName = None, parameterValue = None, marker_success = None):
    if parameterName:
        env = parameters["env"]
        
        command = """env.%s = %s"""%(parameterName, parameterValue)
        exec(command)
    
    
    
    
    if MULTI_THREAD:
        pool = multiprocessing.Pool(processes=pool_size)
        result = pool.map(functionToIterate,[(function, parameters, iteration, marker_success) for iteration in list(range(number_of_times))])
        pool.close()
        pool.join()
    else:
        result = map(functionToIterate,[(function, parameters, iteration, marker_success) for iteration in list(range(number_of_times))])
    
    return result

def successesForRunFunctionWithParameters(function, parameters, number_of_times):
    
    result = runFunctionWithParameters(function, parameters, number_of_times)


    sum = 0
    for x in result:
        if x: sum = sum+1

    return sum




    
        
        