import sys, time

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

        for i in range(self.n) : 
            self.BR.append([])
            self.cnt.append(0)
        
    #--------------------------------------------------------------
    def search(self, tops=1) :
        # i = 0
        # self.BR[i]   = []
        # self.cnt[i]  = 1
        # for j in range(i+1,self.n) :
        #     self.cnt[i] *= self.V[j].card()
    
        while True :
            # if self.cnt[i] <= 0 :
            #     self.checkEndOfTable(i)
            #     dec = None
            #     if not self.makeDecision(dec) : break

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
                    # self.sols.append( s )
                    t = intVarArrayToIntArray(s)
                    self.checkNash(t, self.n-1)

                    # if len(self.sols)==tops : 
                    #     break
                
                dec = self.bran.branch()

                # i = dec[2] + 1
                # if i < self.n :
                #     self.BR[i]   = []
                #     self.cnt[i]  = 1
                #     for j in range(i+1,self.n) :
                #         self.cnt[i] *= self.V[j].card()
                
            else :
                dec = None

            if not self.makeDecision(dec) : break
        return self.Nash

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
                            C.append( Equation( self.V[j] == t[j] ) )
                    
                    S_ = Engine(self.V + self.U , self.C + C ).search(tops=0)

                    for s in S_ :
                        dt = intVarArrayToIntArray(s,self.n)
                        d.append(dt)

                self.insert_table(i,d)
                # self.cnt[i] -= 1
            if t in d :
                self.checkNash(t,i-1)

    #--------------------------------------------------------------
    def findBestResponse(self,t,i) :
        C = []
        for j in range(len(self.V)) :
            if j != i :
                C.append( Equation( self.V[j] == t[j] ) )
    
        if self.F == [] :
            C.append( Equation( self.U[i] == 1))
            F = [0,None]
        else :
            F = self.F[i]

        S = Engine( self.V + self.U , self.C + self.G + C, F ).search(tops=0)
        # S = solveModel( self.glob.V + self.glob.U , self.glob.G + C , F, tops=0 )

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
        # if len(self.BR[i]) <= 0 : return []

        br = []

        # for b in range(len(self.BR[i])) :
        #     if self.BR[i][b][1:i]+self.BR[i][b][i+1:self.n] == t[1:i]+t[i+1:self.n] :
        #         br.append( self.BR[i][b] )
        return br

    #--------------------------------------------------------------

    def insert_table(self,i,d) :
        for t in d :
            if t not in self.BR[i] :
                self.BR[i].append(t)

#====================================================================

