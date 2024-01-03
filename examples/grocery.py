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
from PythonCPSolverT.engine import *

x,y,z,w,t = IntVarArray(5, 1, 900)

# c1 = Linear( [x,y,z,w], t) # Pending double check
c1 = Equation( x + y + z + w == t)
c2 = Equation( x * y * z * w == t*100*100*100)
c3 = Equation( (x >= y) & (y >= z) & (z >= w) )
c4 = Equation( t == 711 )

e = Engine( [x,y,z,w,t], [c1,c2,c3,c4] )

for _ in e.search() :
    print(intVarArrayToStr(_))