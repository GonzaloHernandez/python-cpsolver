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

n = 3

V = IntVarArray(n,1,3)
U = IntVarArray(n,0,1)

G = []
for i in range(n):
    G.append( Equation( U[i] == 0 ) )

C = PNE(V,U,G)

S = Engine(V,[C]).search(ALL)

for s in S :
    print(intVarArrayToStr(s))