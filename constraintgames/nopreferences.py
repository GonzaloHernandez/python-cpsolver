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
from ConstraintCPSolver import *

n = 3

V = IntVarArray(n,1,n)
U = IntVarArray(n,0,n)

G = []
for i in range(n):
    G.append( Equation( U[i] == 0 ) )

# G.append( Equation( U[0] == 0) )
# G.append( Equation( U[1] == 0) )
# G.append( Equation( U[2] == V[2]) )

# F = []
# F.append( maximize(U[0]) )
# F.append( maximize(U[1]) )
# F.append( maximize(U[2]) )

S = EngineGame(V,U,[],G,[]) .search(ALL)
for s in S :
    print(s)

# S = Engine(V+U,G) .search(ALL)
# for s in S :
#     print(intVarArrayToStr(s,IntVar.PRINT_VALUE))
