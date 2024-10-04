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

ex1 = x1*(x2-6)

c7 = Constraint( x1+x4 > ex1 )
c8 = Constraint( x4 == x3+x2 )

e1 = Engine( [x1,x2,x3,x4], [c7,c8], minimize(x3+x4) )

for s in e1.search(5) : print( toInts(s) )