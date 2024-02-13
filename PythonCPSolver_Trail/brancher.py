#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3 (Using a trail to undo a search)
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
#       brancher.py
#====================================================================

class Brancher :
    def __init__(self, vars) -> None:
        self.vars   = vars
        self.curv   = -1
    
    def branch(self) :
        for i,v in enumerate(self.vars) :
            if not v.isAssigned() :
                self.curv = i
                return [v,v.min,i]
        return None

