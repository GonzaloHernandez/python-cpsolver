#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testes with version 1.2
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
from PythonCPSolverT.engine import *

V = s,e,n,d,m,o,r,y = IntVarArray(8,0,9)

C = [
    Equation( (s>=1) & (m>=1) ),

    AllDifferent(V),

    Equation(   s*1000 + e*100 + n*10 + d*1 +
                m*1000 + o*100 + r*10 + e*1 ==
      m*10000 + o*1000 + n*100 + e*10 + y*1 )
]

t1 = time.time()
S = solveModel(V, C)
t2 = time.time()

for _ in S :
    printvars(_)

print(f"total time {t2-t1}")