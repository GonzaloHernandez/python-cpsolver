#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   PythonCPSolver
#       engine.py
#       propagators.py
#       variables.py
#       brancer.py
#====================================================================

from PythonCPSolverT.variables import *

#====================================================================

class Brancher :
    LEFT    = 1
    RIGHT   = 2
    def __init__(self, vars) -> None:
        self.vars   = vars
        self.curv   = -1
    
    def branch(self) :
        if self.curv == len(self.vars) :
            self.curv = -1
            return None
        for i,v in enumerate(self.vars) :
            if not v.isAssigned() :
                self.curv = i
                return [v,v.min,i]
        return None
