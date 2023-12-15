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

s = IntVar(0,9,'s')
e = IntVar(0,9,'e')
n = IntVar(0,9,'n')
d = IntVar(0,9,'n')
m = IntVar(0,9,'m')
o = IntVar(0,9,'o')
r = IntVar(0,9,'r')
y = IntVar(0,9,'y')

k0 = IntVar(1,1)
k1 = IntVar(10,10)
k2 = IntVar(100,100)
k3 = IntVar(1000,1000)
k4 = IntVar(10000,10000)

V = [s,e,n,d,m,o,r,y]
# A = [k0,k1,k2,k3,k4]

C = [
    # Equation( (s==9) & (e==4) & (n==5) & (d==7) & (m==1)),

    Equation( (s>=1) & (m>=1) ),

    AllDifferent(V),

    # Equation(   s*k3 + e*k2 + n*k1 + d*k0 +
    #             m*k3 + o*k2 + r*k1 + e*k0 ==
    #      m*k4 + o*k3 + n*k2 + e*k1 + y*k0 ),

    Equation(   s*1000 + e*100 + n*10 + d*1 +
                m*1000 + o*100 + r*10 + e*1 ==
      m*10000 + o*1000 + n*100 + e*10 + y*1 ),

]

t1 = time.time()
S = solveModel(V, C, tops=0)
t2 = time.time()

for _ in S :
    printvars(_)

print(f"total time {t2-t1}")