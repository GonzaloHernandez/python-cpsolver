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

nPlayers    = 3
nStrategies = 3

V = IntVarArray(nPlayers,0,nStrategies-1,'v')
U = IntVarArray(nPlayers,1,nStrategies,'u')

G = []
F = []
for i in range(nPlayers) :
    G.append(
        Equation( U[i] == count(V,V[i]) )
    )
    F.append(
        maximize( U[i] )
    )

C = [
    # Equation( V[i]>0 )
]



e = EngineGame(V,U,C,G,F)

S = e.search(0)

for s in S :
    print(s)