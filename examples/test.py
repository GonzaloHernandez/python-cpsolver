#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testing version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   examples
#====================================================================

import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolverT.engine import *

V = x,y,z = IntVarArray(3,1,9)

e = Engine(
    V,
    [
        Equation( x*20+y < y*z )
    ],
    minimize( sum(V) )
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s) )

print(e.getFun())