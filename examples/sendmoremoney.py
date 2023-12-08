import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import *

V = s,e,n,d,m,o,r,y = IntVarArray(8,0,9)

C = [
    Constraint( (s>=1) & (m>=1) ),

    Constraint( alldifferent(V) ),

    Constraint( s*1000 + e*100 + n*10 + d*1 +
                m*1000 + o*100 + r*10 + e*1 ==
      m*10000 + o*1000 + n*100 + e*10 + y*1 )
]

S = solveModel(V, C)

for _ in S :
    printvars(_)
