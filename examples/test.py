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

x = IntVar(-1,1)
y = IntVar(-5,5)


e = Engine(
    [x,y],
    [ Constraint(y == (x*2)) ]
)

S = e.search(ALL)

for s in S :
    print( intVarArrayToStr(s) )
