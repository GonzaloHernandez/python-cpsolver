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
from PythonCPSolver import *

t = 711

x,y,z,w = IntVarArray(4, 1, t)

c1 = Constraint( x + y + z + w == t )
c2 = Constraint( x * y * z * w == t*100*100*100 )

e = Engine( [x,y,z,w], [c1,c2,Constraint(x==150)] )

for _ in e.search() :
    for v in toInts(_) :
        print (f"${v/100:.2f}")
