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
from PythonCPSolverT.engine import *

V = x,y,z = IntVarArray(3,1,9)

S = solveModel(
    V,
    [
        # AllDifferent(V),
        # Equation( x*2 + y*2 + z*2 == 8 )
        Linear2( [2,2,2] , V, 9)
    ], 
    tops=0
)

for s in S :
    printvars(s)

