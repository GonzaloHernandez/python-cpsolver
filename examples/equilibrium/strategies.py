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
from PythonCPSolver.engine import *

nPlayers    = 5
nStrategies = 5

V = IntVarArray(nPlayers,1,nStrategies,'v')
U = IntVarArray(nPlayers,1,nStrategies,'u')

G = []
C = []
F = []

for v,u in zip(V,U) :
    G.append( Constraint( u == count(V,v) ) )
    F.append( maximize( u ) )

C.append( EquilibriumClauses(V,U,G,F) )

C.append( Clause( [V[0]!=1, V[1]!=1, U[0]>=3] ) )

e = Engine(V+U,C+G)

from datetime import datetime

t1 = datetime.now()
S = e.search(EAGER)
t2 = datetime.now()

print(f'{t2-t1}')
print('------')

for s in S :
    print(intVarArrayToStr(s,IntVar.PRINT_VALUE))