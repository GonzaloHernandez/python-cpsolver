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

from .variables import *

#====================================================================

class Propagator :
    def __init__(self) -> None:
        pass

    #--------------------------------------------------------------
    def __str__(self) -> str:
        return self.toStr()

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        pass

#====================================================================

class AllDifferent(Propagator) :
    def __init__(self, vars:list) -> None:
        Propagator.__init__(self, )
        self.vars = vars

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'alldifferent('+toStrs(self.vars ,printview)+')'

    #--------------------------------------------------------------
    def prune(self) :
        for v1 in self.vars :
            if v1.isAssigned() :
                for v2 in self.vars :
                    if id(v1) != id(v2) :
                        if v1.min == v2.min :
                            if not v2.project(
                                v2.min+1, 
                                v2.max ) : return False
                        if v1.max == v2.max :
                            if not v2.project(
                                v2.min, 
                                v2.max-1 ) : return False
        return True

#====================================================================

class Linear(Propagator) :
    def __init__(self, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for v in self.vars :
            maxs += v.max
            mins += v.min
        if not self.vart.project( mins, maxs ) : return False

        for v1 in self.vars :
            maxs, mins = 0, 0
            for v2 in self.vars :
                if id(v1) != id(v2) :
                    maxs += v2.max
                    mins += v2.min
            if not v1.project(
                self.vart.min-maxs, 
                self.vart.max-mins ) : return False
        return True

#====================================================================

class LinearArgs(Propagator) :
    def __init__(self, args, vars, vart) -> None:
        if isinstance(vart, int) : vart = IntVar(vart,vart)
        self.args   = args
        self.vars   = vars
        self.vart   = vart

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return str(self.vars)+' = '+str(self.valt)
    
    #--------------------------------------------------------------
    def prune(self) :
        maxs, mins = 0, 0
        for i,v in enumerate(self.vars) :
            if self.args[i] >= 0 :
                maxs += v.max * self.args[i]
                mins += v.min * self.args[i]
            else :
                maxs += v.min * self.args[i]
                mins += v.max * self.args[i]

        if not self.vart.project( mins, maxs ) : return False

        for i1,v1 in enumerate(self.vars) :
            maxs, mins = 0, 0
            for i2,v2 in enumerate(self.vars) :
                if id(v1) != id(v2) :
                    if (self.args[i1] >= 0 and self.args[i2] >= 0) or \
                       (self.args[i1]  < 0 and self.args[i2] < 0):                        
                        maxs += v2.max * self.args[i2]
                        mins += v2.min * self.args[i2]
                    else :
                        maxs += v2.min * self.args[i2]
                        mins += v2.max * self.args[i2]
            if self.args[i1] >= 0 :
                if not v1.project(
                    math.floor((self.vart.min - maxs)/self.args[i1]), 
                    math.ceil ((self.vart.max - mins)/self.args[i1])) : return False
            else :
                if not v1.project(
                    math.floor((mins - self.vart.max)/(self.args[i1]*-1)), 
                    math.ceil ((maxs - self.vart.min)/(self.args[i1]*-1))) : return False

        return True

#====================================================================
    
class Constraint(Propagator) :
    def __init__(self, exp:Expression) -> None:
        self.exp = exp

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return self.exp.toStr(printview)
    
    #--------------------------------------------------------------
    def prune(self) :
        self.exp.evaluate()
        return self.exp.project(1,1)
    
    #--------------------------------------------------------------
    def match(self, localvars:list, globalvars:list) :
        return Constraint( self.exp.match(localvars, globalvars) )

    #--------------------------------------------------------------
    def setEngine(self, engine) :
        self.exp.setEngine(engine)

#====================================================================

def count(vars:list, cond:Expression) -> Expression:
    exp = vars[0]==cond
    for i in range(1,len(vars)):
        exp = exp + (vars[i]==cond)
    return exp

#--------------------------------------------------------------

def alldifferent(vars:list) -> Expression:
    exp = vars[0] if len(vars)==1 else None
    for i in range(len(vars)-1):
        for j in range(i+1,len(vars)):
            if exp is None :
                exp = (vars[i] != vars[j])
            else :
                exp = exp & (vars[i] != vars[j])

    return exp

#--------------------------------------------------------------
def clause(vars:list, vals:list) -> Expression:
    exp = (vars[0] != vals[0]) if len(vars)==1 else None
    for i in range(len(vars)):
        if exp is None :
            exp = (vars[i] != vals[i])
        else :
            exp = exp | (vars[i] != vals[i])

    return exp

#--------------------------------------------------------------

def sum(vars:list) -> Expression:
    exp = vars[0]
    for i in range(1,len(vars)):
        exp = exp + vars[i]
    return exp

#====================================================================

class NegativeClause(Propagator) :
    def __init__(self, vars:list, vals:list) -> None:
        self.vars = vars
        self.vals = vals

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        text = ""
        for vr,vl in zip(self.vars,self.vals) :
            text += "(" + str(vr.toStr()) + "!=" + str(vl) + ") | "
        
        text = text[:-2]
        return "(" + text + ")"
    
    #--------------------------------------------------------------
    def prune(self) :
        varfree = None
        valfree = None
        for vr,vl in zip(self.vars,self.vals) :
            if not vr.isAssigned() :
                if not varfree is None : return True
                varfree = vr
                valfree = vl
            else :
                if vr.getVal() != vl : return True

        if varfree is None :
            return False
        
        if varfree.min == valfree :
            if not varfree.setMin(valfree+1) : return False
        elif varfree.max == valfree :
            if not varfree.setMax(valfree-1) : return False

        return True

#====================================================================

class Clause(Propagator) :
    def __init__(self, exps:list) -> None:
        self.exps = exps

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        text = ""
        for exp in self.exps :
            text += exp.toStr(printview) + " | "
        
        text = text[:-2]
        return "[" + text + "]"

    #--------------------------------------------------------------
    def prune(self) :
        expfree = None
        for exp in self.exps :
            sat = exp.evaluateSAT()
            if sat is None :
                if not expfree is None : return True
                expfree = exp
            else :
                if sat is True : return True

        if expfree is None : return False   # All are "False"
        
        r = exp.project(1,1)

        return r

#====================================================================

import importlib, copy

engine = importlib.import_module('PythonCPSolver.engine')

#====================================================================

class PNE_Eager(Propagator) :
    def __init__(self, V,U,G,C=[],F=[]) -> None:
        self.V,     \
        self.U,     \
        self.G,     \
        self.C,     \
        self.F      = copy.deepcopy( [V,U,G,C,F] )
        
        self.vars   = V
        self.cons   = []

        self.Nash   = []
        self.BR     = []
        self.cnt    = []
        self.n      = len(V)

        for i in range(self.n) : 
            self.BR.append([])
            self.cnt.append(1)
            for m in range(self.n) :
                if i !=m :
                    self.cnt[i] *= V[m].card()
        
        pass

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'NashConstraint propagator'
    
    #--------------------------------------------------------------
    def prune(self) :

        for i,v in enumerate(self.V) :
            if self.cnt[i] <= 0 :
                self.checkEndOfTable(i)
                # self.cons.append( Equation( self.vars[i] <= t[i]) )
                pass

        allAssigned = True
        for v in self.vars :
            if not v.isAssigned() :
                allAssigned = False
                break

        if allAssigned :
            s = []
            for v in self.vars :
                s.append( IntVar(v.min, v.max, v.name) )

            t = toInts(s)
            self.checkNash(t, self.n-1)

        for c in self.cons :
            if not c.prune() : return False

        return True

    #--------------------------------------------------------------
    def checkNash(self,t,i) :
        if i<0 :
            if t not in self.Nash :
                self.Nash.append(t)
                print('PNE: ',end='')
                print(t)
        else :
            d = self.search_table(t,i)
            if d == [] :
                d = self.findBestResponse(t,i)
                
                if d == [] :
                    
                    C = []
                    for j in range(len(self.V)) :
                        if j != i :
                            C.append( Constraint( self.V[j] == t[j] ) )
                    
                    S = engine.Engine(self.V + self.U , self.C + self.G + C ).search(ALL)

                    for s in S :
                        dt = toInts(s,self.n)
                        d.append(dt)

                self.insert_table(i,d)
                self.cnt[i] -= 1

            if t in d :
                self.checkNash(t,i-1)

    #--------------------------------------------------------------
    def findBestResponse(self,t,i) :
        C = []
        for j in range(len(self.V)) :
            if j != i :
                C.append( Constraint( self.V[j] == t[j] ) )

        S = []
        if self.F == [] :
            C.append( Constraint( self.U[i] == 1))
            S = engine.Engine( self.V + self.U , self.C + self.G + C).search(ALL)
        else :
            F = self.F[i]
            E = engine.Engine( self.V + self.U , self.C + self.G + C, F )
            S = E.search()

            if S != [] :
                if F[TYPE]==MAXIMIZE :  val = E.optc.exp.exp2.min
                else :                  val = E.optc.exp.exp2.max

                C.append( Constraint( self.U[i] == val ) )
                S = engine.Engine( self.V + self.U , self.C + self.G + C).search(ALL)

        d = []
        for s in S :
            dt = []
            for j in range(self.n) :
                dt.append(s[j].min)
            d.append(dt)

        return d

    #--------------------------------------------------------------
    def checkEndOfTable(self,i) :
        for t in self.BR[i] :
            self.checkNash(t,self.n-1)

    #--------------------------------------------------------------
    def search_table(self,t,i) :
        if len(self.BR[i]) <= 0 : return []

        br = []

        for b in range(len(self.BR[i])) :
            if self.BR[i][b][0:i]+self.BR[i][b][i+1:self.n] == t[0:i]+t[i+1:self.n] :
                br.append( self.BR[i][b] )
        return br

    #--------------------------------------------------------------
    def insert_table(self,i,d) :
        for t in d :
            if t not in self.BR[i] :
                self.BR[i].append(t)

#====================================================================

class BestResponsesEager(Propagator) :
    def __init__(self, V,p,u,g,f=unoptimize()) -> None:
        self.V  = V
        self.p  = p
        self.u  = u
        self.g  = g
        self.f  = maximize(u) if f==unoptimize() else f
        self.o  = copy.deepcopy(p)
        self.C  = []

        self.BR = []

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'BestResponses propagator'
    
    #--------------------------------------------------------------
    def prune(self) :

        vars    = [self.u]
        others  = []
        values  = []
        for v in self.V :
            if id(v) != id(self.p) :
                if not v.isAssigned(): return True
                vars.append(v)
                others.append(v)
                values.append(v.getVal())
            else :
                vars.append( self.p )

        min, max                = [self.p.min, self.p.max]
        self.p.min, self.p.max  = [self.o.min, self.o.max]

        e = engine.Engine(vars, self.C + [self.g], self.f)
        S = e.search()
        if S != [] :
            val = e.optc.exp.exp2.getVal()
            e = engine.Engine(vars,self.C+[ self.g, Constraint( self.u == val) ])
            S = e.search(ALL)

        if S != [] :
            self.BR += S

            self.C.append( Constraint( clause(others,values) ) )

            for r in S :
                print(toStrs(r[1:]))

        self.p.min, self.p.max  = [min, max]

        return True

#====================================================================

class EquilibriumDB(Propagator) :
    def __init__(self, V, U, G, F=[], C=[]) -> None:
        model  = copy.deepcopy([V,U,G,F,C])
        self.oV = model[0]  # Original Variables
        self.oU = model[1]  # Original Utilities
        self.oG = model[2]  # Original Goals
        self.oF = model[3]  # Original Functions
        self.oC = model[4]  # Original Hard Constraints

        self.vars  = V  # Variables on current searching

        self.subspace   = []

        self.brs = []
        self.cnt = []
        for i in range(len(self.vars)) :
            self.brs.append([])
            self.cnt.append(-999)

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'Equilibrium DB propagator'
    
    #--------------------------------------------------------------
    def prune(self) :
        n = len(self.vars)
        
        allAssigned = True
        newsubspace = []
        for v in self.vars :
            if v.isAssigned() :
                newsubspace.append(v.getVal())
            else :
                allAssigned = False

        self.analyseSubscape(newsubspace)

        if allAssigned :
            t = toInts(self.vars)
            isNash = self.checkNash(t)
            return isNash

        return True
    
    #--------------------------------------------------------------
    def analyseSubscape(self, newsubspace) :
        n = len(self.vars)

        i = 0
        while i < min(len(newsubspace),len(self.subspace)) :
            if newsubspace[i] != self.subspace[i] :
                break
            i += 1
        
        if i == len(newsubspace) or i == n :  return

        if self.cnt[i] == -999 :

            self.brs[i] = []
            self.cnt[i] = 1
            for j in range(i+1, n) :
                self.cnt[i] *= self.oV[j].card()
                self.brs[j] = []
                self.cnt[j] = -999
        else :
 
            for j in range(i+1, n) :
                self.brs[j] = []
                self.cnt[j] = -999
        
        self.subspace = newsubspace

    #--------------------------------------------------------------
    def checkNash(self,t) -> bool :
        for i,v in reversed(list(enumerate(self.vars))) :
            if not self.isBestResponseInTable(t,i) :
                if self.cnt[i] <= 0 :
                    return False
                if not self.isBestResponseNew(t,i) :
                    return False
        return True

    #--------------------------------------------------------------
    def isBestResponseNew(self,t,i) :
        C = [] + self.oC
        for j in range(len(self.oV)) :
            if j != i :
                C.append( Constraint( self.oV[j] == t[j] ) )

        S = []
        if self.oF == [] :
            S = engine.Engine( 
                [self.oU[i]] + self.oV,
                [self.oG[i]] + C + [Constraint( self.oU[i] == 1)]
            ).search(ALL)

            if S==[] :
                S = engine.Engine( 
                    [self.oU[i]] + self.oV,
                    [self.oG[i]] + C + [Constraint( self.oU[i] == 0)]
                ).search(ALL)
        else :
            F = self.oF[i]
            e = engine.Engine( [self.oU[i]] + self.oV, [self.oG[i]] + C, self.oF[i] )
            S = e.search()

            if S != [] :
                if F[TYPE]==MAXIMIZE :  val = e.optc.exp.exp2.min
                else :                  val = e.optc.exp.exp2.max

                C.append( Constraint( self.oU[i] == val ) )
                S = engine.Engine( [self.oU[i]] + self.oV, self.oC + [self.oG[i]] + C).search(ALL)

        isBestResponse = False
        d = []
        for s in S :
            r = toInts(s[1:])
            d.append(r)
            if r == t :
                isBestResponse = True

        self.cnt[i] -= 1

        if d != [] :
            self.saveResponsesInTable(i,d)
            return isBestResponse
        
        return False

    #--------------------------------------------------------------
    def isBestResponseInTable(self,t,i) -> bool :
        if len(self.brs[i]) <= 0 : return False

        for r in self.brs[i] :
            if r == t :
                return True
        
        return False
    
    #--------------------------------------------------------------
    def saveResponsesInTable(self,i,d) :
        for t in d :
            if t not in self.brs[i] :
                self.brs[i].append(t)

    #--------------------------------------------------------------
    def checkEndOfTable(self,i) :
        for t in self.brs[i] :
            if self.checkNash(t) :
                print(f'PNE* {t}')

#====================================================================

class Equilibrium(Propagator) :
    def __init__(self, V, U, G, F=[], C=[]) -> None:
        model  = copy.deepcopy([V,U,G,F,C])
        self.oV = model[0]
        self.oU = model[1]
        self.oG = model[2]
        self.oF = model[3]
        self.oC = model[4]

        self.vars  = V

    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'Equilibrium propagator'
    
    #--------------------------------------------------------------
    def prune(self) :
        for v in self.vars :
            if not v.isAssigned() :
                return True

        t = toInts(self.vars)
        
        for i,v in enumerate(self.vars) :
            if self.isThereABetterResponse(t,i) :
                return False
        return True

    #--------------------------------------------------------------
    def isThereABetterResponse(self,t,i) :
        C = [] + self.oC
        T = [] + self.oC
        for j in range(len(self.oV)) :
            if j != i :
                C.append( Constraint( self.oV[j] == t[j] ) )
            T.append( Constraint( self.oV[j] == t[j] ) )

        # Utility calculation
        e = engine.Engine([self.oU[i]] + self.oV, [self.oG[i]] + T )
        e.propagate()               # S = e.search()
        val = e.vars[0].getVal()    # val = S[0][0].getVal()

        # Looking for a best response
        if self.oF != [] and self.oF[i][TYPE]==MINIMIZE :
            C.append( Constraint( self.oU[i] < val) )
        else :
            C.append( Constraint( self.oU[i] > val) )

        e = engine.Engine( self.oV + [self.oU[i]] , [self.oG[i]] + C )
        S = e.search()

        return ( S != [] )

#====================================================================
# Storing never best responses using cluses
#====================================================================
class EquilibriumClauses(Propagator) :
    def __init__(self, V, U, G, F=[], C=[]) -> None:
        model  = copy.deepcopy([V,U,G,F,C])
        self.oV = model[0]
        self.oU = model[1]
        self.oG = model[2]
        self.oF = model[3]
        self.oC = model[4]

        self.vars = V
        self.util = U
        self.cons = C

    #--------------------------------------------------------------
    def setEngine(self, engine):
        self.engine = engine
    
    #--------------------------------------------------------------
    def toStr(self, printview=IntVar.PRINT_MIX) -> str :
        return 'Equilibrium propagator'
    
    #--------------------------------------------------------------
    def prune(self) :

        for v in self.vars :
            if not v.isAssigned() :
                return True

        t = toInts(self.vars)
        
        for i,v in enumerate(self.vars) :
            if self.isThereABetterResponse(t,i) :
                return False
        return True

    #--------------------------------------------------------------
    def isThereABetterResponse(self,t,i) :
        C1 = [] + self.oC   # by utility calculation
        C2 = [] + self.oC   # by searching the best response
        exps = []           # by creating a new clause
        for j in range(len(self.oV)) :
            if j != i :
                C1.append( Constraint( self.oV[j] == t[j] ) )
                exps.append( self.vars[j] != t[j] )
            C2.append( Constraint( self.oV[j] == t[j] ) )

        # Utility calculation
        e = engine.Engine([self.oU[i]] + self.oV, [self.oG[i]] + C2 )
        e.propagate()               # S = e.search()
        util = e.vars[0].getVal()   # val = S[0][0].getVal()

        # Looking for a best response
        f = None
        if self.oF != [] and self.oF[i][TYPE]==MINIMIZE :
            C1.append( Constraint( self.oU[i] < util) )
            f = minimize( self.oU[i] )
        else :
            C1.append( Constraint( self.oU[i] > util) )
            f = maximize( self.oU[i] )

        e = engine.Engine( [self.oU[i]] + self.oV, [self.oG[i]] + C1, f )
        S = e.search()

        thereIsBetterResponse = False

        if S != [] :
            util = S[0][0].getVal()
            thereIsBetterResponse = True

        # # Looking for never best responses
        # if self.oF != [] and self.oF[i][TYPE]==MINIMIZE :
        #     exps.append( self.util[i] <= util )
        # else :
        #     exps.append( self.util[i] >= util )

        # self.engine.cons.append( Clause(exps) )

        return thereIsBetterResponse