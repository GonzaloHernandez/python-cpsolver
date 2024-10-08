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

n = 3

V = IntVarArray(n,1,3)
U = IntVarArray(n,1,3)

G = []
for i in range(n): 
    G.append( Constraint( U[i] == 1 ) )

c = Equilibrium(V,U,G,[],[])

S = Engine(V,[c]).search(ALL)

for s in S :
    print( toInts(s))