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

os.system('clear')

sys.path.insert(1,'.')
from PythonCPSolver_Trail.engine import *

x = IntVar(0,1,'x')
y = IntVar(0,1,'y')

ux = IntVar(0,3,'ux')
uy = IntVar(0,3,'uy')

gx = Constraint( ux == ( (y*2)-x+1 ) )
gy = Constraint( uy == ( (x*2)-y+1 ) )

e = Engine( 
    [ x, y] + [ux,uy], 
    [gx,gy] 
)

S = e.search(ALL)

for s in S :
    print( intVarArrayToStr(s) )

# -------------------------------------------------------
# Pendant to review the multiplication in Constraint