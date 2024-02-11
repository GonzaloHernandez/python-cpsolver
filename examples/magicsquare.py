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

import os,sys, time
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver_Trail.engine import *

n = 5

V = IntVarArray(n*n,1,n*n)
t = IntVar()

Vrows = []
Vcols = []
Vdia1 = []
Vdia2 = []

for r in range(n) :
    row = []
    col = [] 
    for c in range(n) :
        row.append(V[r*n+c])
        col.append(V[c*n+r])
    Vrows.append(row)
    Vcols.append(col)
    Vdia1.append(V[r*n+r])
    Vdia2.append(V[r*n+(n-1-r)])

C = []


C.append( Linear(Vdia1, t) )
C.append( Linear(Vdia2, t) )

for i in range(n) :
    C.append( Linear(Vrows[i], t) )
    C.append( Linear(Vcols[i], t) )

# C.append( Equation( sum(Vdia1)==t ) )
# C.append( Equation( sum(Vdia2)==t ) )

C.append( AllDifferent(V) )

C.append( Equation( t == (n*n*(n*n+1)//2)//n ) ) 

t1 = time.time()
S = Engine( V+[t], C ).search()
t2 = time.time()

print(f"Sum = {S[0][n*n].toStr(IntVar.PRINT_VALUE)}\n")

for r in range(n) :
    for c in range(n) :
        v = S[0][r*n+c]
        print(f"{v.toStr(IntVar.PRINT_VALUE):>2}", end=' ')
    print()

print(f"Total solutions: {len(S)}\nTotal time: {t2-t1}   ")

#====================================================================
# Benchmarks:
# n=6 in 100.79sg (MacBoock Pro 14, 2023)