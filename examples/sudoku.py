import os,sys, time
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver import *

V = IntVarArray(9*9, 1, 9)

Vrows = []
Vcols = []
Varea = []

# Creating view for rows and columns
for r in range(9) :
    row = []
    col = []
    for c in range(9) :
        row.append(V[r*9+c])
        col.append(V[c*9+r])
    Vrows.append(row)
    Vcols.append(col)

# Creating view for areas
for r1 in range(3) :
    for c1 in range(3) :
        area = []
        for r2 in range(3) :
            for c2 in range(3) :
                area.append(V[r1*27 + c1*3 + r2*9 + c2])
        Varea.append(area)

C = []

for i in range(9) :
    C.append( AllDifferent(Vrows[i]) )
    C.append( AllDifferent(Vcols[i]) )
    C.append( AllDifferent(Varea[i]) )

# Custom constraints / Values of game
C.append( Equation( V[ 4]==7) )
C.append( Equation( V[10]==2) )
C.append( Equation( V[75]==8) )

t1 = time.time()
S = solveModel( V, C )
t2 = time.time()

for r in range(9) :
    for c in range(9) :
        v = S[0][r*9+c]
        print(v.toStr(IntVar.PRINT_VALUE), end=' ')
    print()

print(f"Total time: {t2-t1}")
