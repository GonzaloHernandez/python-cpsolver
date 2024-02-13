#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testing version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   examples
#====================================================================

import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver_Trail.engine import *

x,y = IntVarArray(2,-3,3,'v')
t = IntVar(2,5,'t')

e = Engine(
    [x,y] + [t],
    [ Equation( x == -(t+1)) ]
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s) )

print(len(S))