#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testes with version 1.2
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
from PythonCPSolver.engine import *

V = IntVarArray(5,1,10)

S = solveModel(
    V,
    [ 
        AllDifferent(V),
        Linear(V,15),
        Equation( (V[0]>=V[1]) & (V[1]>=V[2]) & (V[2]>=V[3]) & (V[3]>=V[4]))
    ], 
    tops=1
)

for s in S :
    printvars(s)
