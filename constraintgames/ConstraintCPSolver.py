#====================================================================
# Constraint Games solver using Simple CP Solver 
# Current version 1.0 (Using a PythonCPSolver_Trail)
#
# Gonzalo Hernandez
# gonzalohernandez@hotmail.com
# 2024
#
# Modules:
#   ConstraintCPSolver
#====================================================================

import sys

#--------------------------------------------------------------

sys.path.insert(1,".")
from PythonCPSolver_Trail.engine import *

#--------------------------------------------------------------

class EngineGame(Engine) :

    def __init__(self,V,U,C=[],G=[],F=[]) -> None:
        super(EngineGame,self).__init__( V ,C )
        self.Nash   = []
        self.BR     = []
        self.cnt    = []
        self.n      = len(V)
        self.V      = V
        self.U      = U
        self.C      = C
        self.G      = G
        self.F      = F
        self.count  = 0

        for _ in range(self.n) : 
            self.BR.append([])
            self.cnt.append(0)
        
    #--------------------------------------------------------------
    def search(self, tops=1) : # overwrite

        #------------------------------------
        i = 0
        self.BR[i]   = []
        self.cnt[i]  = 1
        for j in range(i+1,self.n) :
            self.cnt[i] *= self.V[j].card()
        #------------------------------------
    
        counter = 0
        while True :
            
            #------------------------------------
            if i < self.n :
                if self.cnt[i] <= 0 :
                    self.checkEndOfTable(i)
                    if not self.makeDecision(None) : break
            #------------------------------------

            if self.propagate() : 

                allAssigned = True
                for v in self.vars :
                    if not v.isAssigned() :
                        allAssigned = False
                        break
                
                if allAssigned :
                    s = []
                    for v in self.vars :
                        s.append( IntVar(v.min, v.max, v.name) )

                    #------------------------------------
                    t = intVarArrayToIntArray(s)
                    self.checkNash(t, self.n-1)
                    #------------------------------------
                
                dec = self.bran.branch()

                #------------------------------------
                if dec != None :
                    i = dec[2]
                    if i < self.n :
                        self.BR[i]   = []
                        self.cnt[i]  = 1
                        for j in range(i+1,self.n) :
                            self.cnt[i] *= self.V[j].card()
                #------------------------------------
                
            else :
                dec = None
            
            counter += 1

            if not self.makeDecision(dec) : break
    
        # print(counter) # For debugging purposes
    
        #------------------------------------
        return self.Nash
        #------------------------------------

    #--------------------------------------------------------------
    def checkNash(self,t,i) :
        if i<0 :
            if t not in self.Nash :
                self.Nash.append(t)
        else :
            d = self.search_table(t,i)
            if d == [] :
                d = self.findBestResponse(t,i)
                
                if d == [] :
                    
                    C = []
                    for j in range(len(self.V)) :
                        if j != i :
                            C.append( Constraint( self.V[j] == t[j] ) )
                    
                    S = Engine(self.V + self.U , self.C + C ).search(ALL)

                    for s in S :
                        dt = intVarArrayToIntArray(s,self.n)
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
            S = Engine( self.V + self.U , self.C + self.G + C).search(ALL)
        else :
            F = self.F[i]
            E = Engine( self.V + self.U , self.C + self.G + C, F )
            S = E.search()

            if S != [] :
                if F[TYPE]==MAXIMIZE :  val = E.optc.exp.exp2.min
                else :                  val = E.optc.exp.exp2.max

                C.append( Constraint( self.U[i] == val ) )
                S = Engine( self.V + self.U , self.C + self.G + C).search(ALL)

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

