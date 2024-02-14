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

import copy

from PythonCPSolver_Trail.propagators import *
from PythonCPSolver_Trail.brancher import *

#====================================================================

class Engine :
    def __init__(self, vars, cons, func=[0,None]) -> None:
        model = copy.deepcopy([vars,cons,func])
        self.vars   = model[0]  # Variables and domains
        self.cons   = model[1]  # Constraints
        self.func   = model[2]  # Optimization function [type, expression] 
        self.optc   = None      # Optimization (new) constraint
        self.sols   = []        # Solutions found
        self.trail  = []        # Trail to UnDo purspose
        self.bran   = Brancher(self.vars)

        for v in self.vars : v.setEngine(self)
        for c in self.cons : c.setEngine(self)

    #--------------------------------------------------------------
    def isOptimizing(self) :
        return True if self.func[TYPE]  > NONEOPTI else False

    def isMinimizing(self) :
        return True if self.func[TYPE] == MINIMIZE else False
    
    def isMaximizing(self) :
        return True if self.func[TYPE] == MAXIMIZE else False

    def getFun(self) :
        return self.optc

    #--------------------------------------------------------------
    def propagate(self) :
        t1 = t2 = 0

        for v in self.vars : t1 += v.card() # Domain size precount

        for c in self.cons :
            if not c.prune() : return False
        if self.optc != None :
            if not self.optc.prune() : return False

        for v in self.vars : t2 += v.card() # Domain size postcount

        if t2 < t1 :
            return self.propagate()
        else :
            return True

    #--------------------------------------------------------------
    def search(self, tops=1) :
        while True :
            if self.propagate() : 

                allAssigned = True
                for v in self.vars :
                    if not v.isAssigned() :
                        allAssigned = False
                        break
                
                if allAssigned :
                    if self.isOptimizing() : 
                        result = self.func[EXPR].evaluate()
                        if self.sols == [] :
                            if self.isMaximizing() :
                                var = IntVar( result[MIN], IntVar.INFINITE, engine=self)
                                self.optc = Equation( self.func[1] > var )
                            else :
                                var = IntVar(-IntVar.INFINITE, result[MAX], engine=self)
                                self.optc = Equation( self.func[1] < var )
                        else :
                            if self.isMaximizing() :
                                self.optc.exp.exp2.setge( result[MIN] )
                            else :
                                self.optc.exp.exp2.setle( result[MAX] )

                        s = []
                        for v in self.vars :
                            s.append( IntVar(v.min, v.max, v.name) )
                        self.sols = [ s ]
                    else : # Is satisfying
                        s = []
                        for v in self.vars :
                            s.append( IntVar(v.min, v.max, v.name) )

                        self.sols.append( s )
                        if len(self.sols)==tops : 
                            break
                
                dec = self.bran.branch()
            else :
                dec = None

            if not self.makeDecision(dec) : break
        return self.sols

    #--------------------------------------------------------------
    def makeDecision(self, dec) :
        if dec is None :
            if self.trail != [] :
                var = self.undo()
                if var is None : return False
                step = [var, LEFT, var.min, False]
                self.trail.append( step )
                var.min += 1

                return True
            else :
                return False
            
        var,val = dec[0],dec[1]
        step = [var, RIGHT, var.max, True]
        self.trail.append( step )
        var.max = val

        return True

    #--------------------------------------------------------------
    def undo(self) :
        while self.trail != [] :
            [var,sid,val,key] = self.trail.pop()

            if   sid == LEFT :  var.min = val
            elif sid == RIGHT : var.max = val

            if   key :          return var
        return None

#====================================================================

def stepToStr(step) -> str:
    text  = step[0].name
    text += ' L ' if step[1]==1 else ' R '
    text += str(step[2])
    
    return '{' + text + '}'