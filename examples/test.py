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
from PythonCPSolver_CDCL.engine import *

x = IntVar(0,1,'x')
y = IntVar(0,1,'y')

e = Engine(
    [x,y],
    []
)

S = e.search(0)

for s in S :
    print( intVarArrayToStr(s) )
