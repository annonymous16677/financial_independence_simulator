from Parameters import DEBUG
import sys


def log(s):
    if DEBUG == 1:
        sys.stdout.write('\n')
        sys.stdout.write(s)

def tack(s):
    if DEBUG == 1:
        
        sys.stdout.write(s)