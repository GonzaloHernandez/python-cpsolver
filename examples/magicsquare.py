import os,sys, time
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import *

n = 4

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

C.append( Constraint( alldifferent(V)) )

for i in range(n) :
    C.append( Constraint( sum(Vrows[i])==t  ) )
    C.append( Constraint( sum(Vcols[i])==t  ) )

C.append( Constraint( sum(Vdia1)==t  ) )
C.append( Constraint( sum(Vdia2)==t  ) )

C.append( Constraint( t == (n*n*(n*n+1)//2)//n ) ) 

S = solveModel( V+[t], C )

print(f"Sum = {S[0][n*n].toStr(IntVar.PRINT_VALUE)}\n")

for r in range(n) :
    for c in range(n) :
        v = S[0][r*n+c]
        print(f"{v.toStr(IntVar.PRINT_VALUE):>2}", end=' ')
    print()

