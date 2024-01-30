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

x,y,z,w,t = IntVarArray(5, 1, 711)

c0 = Equation( t == 711 )
c1 = Equation( x + y + z + w == t )
c2 = Equation( x * y * z * w == t*100*100*100 )

e = Engine( [x,y,z,w,t], [c0,c1,c2] )

for _ in e.search() :
    print(intVarArrayToStr(_))