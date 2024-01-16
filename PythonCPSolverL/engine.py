#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.3
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

import copy

from PythonCPSolverL.conflictdriven import *
from PythonCPSolverL.brancher import *

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

        self.cdcl  = ConflictDriven(self.vars, self)

        self.cons.append( self.cdcl )

    #--------------------------------------------------------------
    def isOptimizing(self) :
        return True if self.func[0] > 0 else False

    def isMinimizing(self) :
        return True if self.func[0] == 1 else False
    
    def isMaximizing(self) :
        return True if self.func[0] == 2 else False

    def evaluateFun(self) :
        localfun = self.func[1].match(self.vars, self.vars)
        return localfun.evaluate()[0]
    
    def getFun(self) :
        return self.optc

    #--------------------------------------------------------------
    def propagate(self) :
        t1 = 0
        for v in self.vars : t1 += v.card()
        for lv in self.cdcl.bvars : 
            for v in lv : t1 += v.card()

        self.q = []
        for c in self.cons :
            self.q.append(c)
        
        if not self.optc is None :
            self.q.append(self.optc)

        while self.q != [] :
            c = self.q.pop(0)
            if not c.prune() : return False

        t2 = 0
        for v in self.vars : t2 += v.card()
        for lv in self.cdcl.bvars : 
            for v in lv : t2 += v.card()

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
                        val = self.evaluateFun()
                        if self.sols == [] :
                            if self.isMaximizing() :
                                self.optc = Equation(
                                    self.func[1] > IntVar( val, IntVar.INFINITE, engine=self) )
                            else :
                                self.optc = Equation(
                                    self.func[1] < IntVar(-IntVar.INFINITE, val, engine=self) )
                        else :
                            if self.isMaximizing() :
                                self.optc.exp.exp2.setge( val )
                            else :
                                self.optc.exp.exp2.setle( val )

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
                self.cdcl.createClause(self.vars,[False for i in self.vars])
                var = self.undo()
                if var is None : return False
                
                return True
            else :
                return False
            
        var,val = dec[0],dec[1]
        step = [var, Brancher.RIGHT, var.max, True]
        self.trail.append( step )
        var.max = val

        return True

    #--------------------------------------------------------------
    def undo(self) :
        while self.trail != [] :
            [var,sid,val,key] = self.trail.pop()
            match(sid) :
                case Brancher.LEFT :
                    var.min = val
                case Brancher.RIGHT :
                    var.max = val
            if key : 
                return var
        return None

#====================================================================

def minimize(exp) -> Expression:
    return [1,exp]

#--------------------------------------------------------------

def maximize(exp) -> Expression:
    return [2,exp]

#====================================================================
