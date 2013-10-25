from random import *

class PRNG:
     	
    
    
    def __init__(self, s):
        self.prng  = Random()
        self.prng.seed(s)
        self.prng.jumpahead(s)
    
   
    def random_in_range(self,a,b):
        return self.prng.randint(a,b)
        
    def random_selection(self, array):
        return array[self.random_in_range(0,len(array)-1)]

    def rand_unit(self):
        N = 1000000000
        return float(self.random_in_range(0, N-1)) / float(N)
    
        