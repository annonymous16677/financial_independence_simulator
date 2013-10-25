import locale
import math

import os

if os.name == "posix":
    loc ='en_US'
else:
    loc ='English_United States' 
locale.setlocale(locale.LC_ALL, loc)


def roundCash(x):
    return round(x)

def printCash(x):
    r = roundCash( x )
    return "$%s"%(locale.format("%d", r, grouping=True))



