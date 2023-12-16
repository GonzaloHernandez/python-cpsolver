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
from PythonCPSolverT.engine import *

s = IntVar(1,9,'s')
e = IntVar(0,9,'e')
n = IntVar(0,9,'n')
d = IntVar(0,9,'n')
m = IntVar(1,9,'m')
o = IntVar(0,9,'o')
r = IntVar(0,9,'r')
y = IntVar(0,9,'y')

V = [s,e,n,d,m,o,r,y]

C = [
    AllDifferent(V),

    Equation(   s*1000 + e*100 + n*10 + d*1 +
                m*1000 + o*100 + r*10 + e*1 ==
      m*10000 + o*1000 + n*100 + e*10 + y*1 ),
]

e = Engine(V, C)

t1 = time.time()
S = e.search(0)
t2 = time.time()

for _ in S :
    print( intVarArrayToStr(_) )

print(f"total time {t2-t1}")