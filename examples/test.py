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
from PythonCPSolverL.engine import *

x = IntVar(0,2,'x')
y = IntVar(0,2,'y')

# xs = IntVarArray( x.card(), 0,1, 'x')
# ys = IntVarArray( y.card(), 0,1, 'y')

# CL = []
# for i,xi in enumerate(xs) :
#     CL.append( Equation( xi == (x == i+x.min) ) )

# for i,yi in enumerate(ys) :
#     CL.append( Equation( yi == (y == i+y.min) ) )

e = Engine(
    [x,y],
    [ 
        # Lazzy( [x,y] ) 
    ]
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s) )
