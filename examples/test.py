#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Testing version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   examples
#====================================================================

import os,sys
os.system("clear")

sys.path.insert(1,".")
from PythonCPSolver.engine import *

x1 = IntVar(1,10,"var")
x2 = IntVar(-5,4)
x3 = IntVar(3)
x4 = IntVar()

V = IntVarArray(5,1,10,"var")
W = IntVarArray(3)

ex1 = x1*(x2-6)
ex2 = V[2] >= 4

c1 = AllDifferent( W )
c2 = AllDifferent( [ x1,x3,V[2] ] )
c3 = Linear( V, 5 )
c4 = Linear( [x2,x3,x4], W[0] )
c5 = LinearArgs( [5,4,2], [x1,x2,x3], 12 )
c6 = LinearArgs( [2,2,2], W, x4 )
c7 = Constraint( x1+x4 > ex1 )
c8 = Constraint( x4 == x3+x2 )
c9 = Constraint( count(V,3) == x2 )
c10 = Constraint( x1*3 == sum(W) )
c11 = Constraint( sum([x1,x2,x3]) > sum(V) )

e = Engine(
    [x1,x2,x3,x4]+V+W,
    [c11]
)

S = e.search()

for s in S :
    print( intVarArrayToStr(s) )
