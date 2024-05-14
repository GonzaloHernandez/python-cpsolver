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

import os,sys,time
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver_Trail.engine import *

V = [s,e,n,d,m,o,r,y] = IntVarArray(8,0,9)

C = [
    AllDifferent(V),
    Constraint( s > 0),
    Constraint( m > 0),
    Constraint( s*1000 + e*100 + n*10 + d*1 +
                m*1000 + o*100 + r*10 + e*1 ==
      m*10000 + o*1000 + n*100 + e*10 + y*1 ),
]

e = Engine(V, C)

S = e.search(ALL)

for _ in S :
    print( intVarArrayToStr(_) )
