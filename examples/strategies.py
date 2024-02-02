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
from PythonCPSolver_Trail.engine import *
from PythonCPSolver_Trail.propagators import *

nPlayers    = 3
nStrategies = 3

V = IntVarArray(nPlayers,0,nStrategies-1,'v')
U = IntVarArray(nPlayers,1,nStrategies,'u')

G = []
C = []

for i in range(nPlayers) :
    G.append( Equation( U[i] == count(V,V[i]) ) )
    C.append( NashConstraint( V, i, maximize(U[i]) ) )

e = Engine(V+U, G+C)

S = e.search(0)

for s in S :
    print(intVarArrayToStr(s,IntVar.PRINT_VALUE))