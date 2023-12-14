#====================================================================
# Simple Constraint (Satisfaction/Optimization) Programming Solver 
# Current version 1.? In construction
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2023
#
# Modules:
#   PythonCPSolver
#       engine-trail.py
#       propagators.py
#       variables.py
#====================================================================

from PythonCPSolverT.propagators import *
from PythonCPSolverT.brancher import *
import copy

class Engine :
    def __init__(self, vars, cons, func, tops) -> None:
        self.vars   = vars  # Variables and domains
        self.cons   = cons  # Constraints
        self.func   = func  # Optimization function [type, expression] 
        self.tops   = tops  # Amount of solutions required
        self.optv   = 0     # Current optimization value
        self.optc   = None  # Optimization (new) constraint
        self.sols   = []    # Solutions found
        self.trail  = []    # Trail to UnDo purspose
        self.vi     = 0
        self.done   = False
        self.bran   = Brancher(vars)

        for v in vars : v.setEngine(self)

    #--------------------------------------------------------------
    def isOptimizing(self) :
        return True if self.func[0] > 0 else False

    def isMinimizing(self) :
        return True if self.func[0] == 1 else False
    
    def isMaximizing(self) :
        return True if self.func[0] == 2 else False

    def getFunValue(self) :
        return self.optv

    def evaluateFun(self) :
        localfun = self.func[1].match(self.vars, self.vars)
        return localfun.evaluate()[0]
    
    def setFunValue(self,v) :
        self.optv = v
    
    def getFun(self) :
        return self.func[1]

    #--------------------------------------------------------------
    def propagate(self) :
        t1 = 0
        for v in self.vars : t1 += v.card()

        self.q = []
        for c in self.cons :
            self.q.append(c)
        
        if not self.optc is None :
            self.q.append(self.optc)

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
        while True :
            if self.done : return

            self.propagate()

            allAssigned = True
            for v in self.vars :
                if v.isFailed() :
                    pass
                if not v.isAssigned() :
                    allAssigned = False
                    break
            
            if allAssigned :
                if self.isOptimizing() : 
                    val = self.evaluateFun()
                    if self.sols == [] :
                        if self.isMaximizing() :
                            self.optc = Equation(
                                self.func[1] > IntVar(val, IntVar.INFINITE) )
                        else :
                            self.optc = Equation(
                                self.func[1] < IntVar(-IntVar.INFINITE, val) )
                    else :
                        if self.isMaximizing() :
                            self.optc.exp.exp2.setge( val )
                        else :
                            self.optc.exp.exp2.setle( val )

                    self.sols = [ self.vars ]
                    self.setFunValue( val )
                else : # Is satisfying
                    s = []
                    for v in self.vars :
                        s.append( IntVar(v.min, v.max, v.name) )

                    self.sols.append( s )
                    if len(self.sols)==self.tops : self.done = True
            
            dec = self.bran.branch()
            if not self.makeDecision(dec) : return

    #--------------------------------------------------------------
    def makeDecision(self, dec) :
        if dec is None :
            if self.trail != [] :
                step = self.trail.pop()
                var,sid,val = step[0],step[1],step[2]
                match(sid) :
                    case Brancher.LEFT :
                        var.min = val
                        var = self.undo()
                        if var is None : return False
                    case Brancher.RIGHT :
                        var.max = val

                step = [var, Brancher.LEFT, var.min, False]
                self.trail.append( step )
                var.min += 1

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

def solveModel(vars, cons, func=[0,None], tops=1) :
    e = Engine(vars, cons, func, tops)
    e.search()
    return e.sols

#--------------------------------------------------------------

def minimize(exp) :
    return [1,exp]

#--------------------------------------------------------------

def maximize(exp) :
    return [2,exp]

#====================================================================
