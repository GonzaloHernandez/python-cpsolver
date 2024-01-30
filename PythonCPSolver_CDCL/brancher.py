#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.4 (Conflict-Driven Clause Learning)
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   PythonCPSolver
#       engine.py
#       propagators.py
#       variables.py
#       brancher.py
#       conflictdriven.py
#====================================================================

from PythonCPSolver_CDCL.variables import *

#====================================================================

class Brancher :
    LEFT    = 1
    RIGHT   = 2
    def __init__(self, vars) -> None:
        self.vars   = vars
        self.curv   = -1
    
    def branch(self) :
        for i,v in enumerate(self.vars) :
            if not v.isAssigned() :
                self.curv = i
                return [v,v.min,i]
        return None

