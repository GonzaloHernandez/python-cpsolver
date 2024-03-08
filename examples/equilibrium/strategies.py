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

nPlayers    = 3
nStrategies = 3

V = IntVarArray(nPlayers,0,nStrategies-1,'v')
U = IntVarArray(nPlayers,1,nStrategies,'u')

G = []
C = []
F = []
for i in range(nPlayers) :
    G.append(
        Constraint( U[i] == count(V,V[i]) )
    )
    F.append(
        maximize( U[i] )
    )

C.append( Equilibrium(V,U,G,F) )

e = Engine(V,C)

from datetime import datetime

t1 = datetime.now()
S = e.search(ALL)
t2 = datetime.now()

print(f'{t2-t1}')
print('------')

for s in S :
    print(intVarArrayToStr(s,IntVar.PRINT_VALUE))