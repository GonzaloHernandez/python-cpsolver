#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.2
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   PythonCPSolver
#       engine.py (copy space)
#       propagators.py
#       variables.py
#====================================================================

import copy

from PythonCPSolverC.propagators import *

class Globals :
    def __init__(self, optv, vars, func, sols, tops) -> None:
        self.optv = optv    # Current optimization value
        self.vars = vars    # Original variables
        self.func = func    # Optimization function [type,expression]
        self.optc = None    # Optimization (new) constraint
        self.sols = sols    # Solutions found
        self.tops = tops    # Amount of solutions required
        self.done = False   # Flag to stop searching

#====================================================================

class SearchInstance :
    def __init__(self, vars, cons, func, tops) -> None:
        self.vars = vars
        self.cons = cons
        self.glob = Globals([0], vars, func, [], tops)
    
    def isOptimizing(self) :
        return True if self.glob.func[0] > 0 else False

    def isMinimizing(self) :
        return True if self.glob.func[0] == 1 else False
    
    def isMaximizing(self) :
        return True if self.glob.func[0] == 2 else False

    def getFunValue(self) :
        return self.glob.optv[0]

    def evaluateFun(self) :
        localfun = self.glob.func[1].match(self.vars, self.glob.vars)
        return localfun.evaluate()[0]
    
    def setFunValue(self,v) :
        self.glob.optv[0] = v
    
    def getFun(self) :
        return self.glob.func[1]
    
    #--------------------------------------------------------------
    def propagate(self) :
        t1 = 0
        for v in self.vars : t1 += v.card()

        self.q = []
        for c in self.cons :
            self.q.append(c)
        
        if not self.glob.optc is None :
            c = self.glob.optc.match(self.vars, self.glob.vars)
            self.q.append(c)

        while self.q != [] :
            c = self.q.pop(0)
            if not c.prune() : return False

        t2 = 0
        for v in self.vars : t2 += v.max - v.min + 1

        if t2 < t1 :
            return self.propagate()
        else :
            return True

    #--------------------------------------------------------------
    def search(self) :
        if self.glob.done : return

        if not self.propagate() : return []

        allAssigned = True
        for v in self.vars :
            if v.isFailed() :
                return []
            if not v.isAssigned() :
                allAssigned = False
                break

        if allAssigned :
            if self.isOptimizing() : 
                val = self.evaluateFun()
                if self.glob.sols == [] :
                    if self.isMaximizing() :
                        self.glob.optc = Equation(
                            self.glob.func[1] > IntVar(val, IntVar.INFINITE) )
                    else :
                        self.glob.optc = Equation(
                            self.glob.func[1] < IntVar(-IntVar.INFINITE, val) )
                else :
                    if self.isMaximizing() :
                        self.glob.optc.exp.exp2.setge( val )
                    else :
                        self.glob.optc.exp.exp2.setle( val )

                self.glob.sols = [ self.vars ]
                self.setFunValue( val )
            else : # Is satisfying
                self.glob.sols.append(self.vars)
                if len(self.glob.sols)==self.glob.tops : self.glob.done = True

        else :
            for i,v in enumerate(self.vars) :
                if not v.isAssigned():
                    left    = self.clone()
                    right   = self.clone()

                    left    .vars[i].setle(left .vars[i].min)
                    right   .vars[i].setge(right.vars[i].min+1)
                    
                    left.search()
                    right.search()
                    break

    #--------------------------------------------------------------
    def clone(self) :
        branch = copy.copy(self)
        branch.vars, branch.cons = copy.deepcopy([self.vars, self.cons])
        return branch

#====================================================================

def solveModel(vars, cons, func=[0,None], tops=1) :
    model = copy.deepcopy([vars,cons,func])
    s = SearchInstance(model[0],model[1],model[2],tops)
    s.search()
    return s.glob.sols

#--------------------------------------------------------------

def minimize(exp) :
    return [1,exp]

#--------------------------------------------------------------

def maximize(exp) :
    return [2,exp]

#====================================================================
