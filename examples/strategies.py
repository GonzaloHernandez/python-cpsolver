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
from PythonCPSolverL.engine import *

nPlayers    = 5
nStrategies = 5

V = IntVarArray(nPlayers,0,nStrategies-1)
U = IntVarArray(nPlayers,1,nStrategies)

C = []

for i in range(nPlayers) :
    C.append(
        Equation( U[i] == count(V,V[i]) )
    )

e = Engine(V+U, C)

S = e.search(20)

for s in S :
    print(intVarArrayToStr(s))