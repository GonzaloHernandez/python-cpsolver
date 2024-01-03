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
from constraintgames.ConstraintCPSolver import *

nPlayers    = 5
nStrategies = 5

V = IntVarArray(nPlayers,0,nStrategies-1)
U = IntVarArray(nPlayers,1,nStrategies)

G = []

for i in range(nPlayers) :
    G.append(
        Equation( U[i] == count(V,V[i]) )
    )

C = [
    # Equation( V[i]>0 )
]

e = EngineGame(V,U,C,G)

S = e.search(0)

for s in S :
    print(intVarArrayToStr(s))