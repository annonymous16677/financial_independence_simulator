
import os
from optparse import OptionParser


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--dir", dest="directory")
    (options, args) = parser.parse_args()


   
    
    directory = options.directory
    
    if directory:
        os.chdir(directory)

    from MarketSim import run_simulation
    run_simulation()