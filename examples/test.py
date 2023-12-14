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

V = IntVarArray(3,1,3)

S = solveModel(
    V,
    [
        AllDifferent(V)
    ], 
    tops=0
)

for s in S :
    printvars(s)
