#!/usr/bin/env python

import numpy as np
import numpy.random as npr
import time
import datetime
import pdb

def densityReduction(v):
    return sum(v)/float(len(v))

class Tasep(object):
    def __init__(self, particles, p, epsilon):
        """
        Parallel TASEP on a 1D-ring of length 2*particles with update probability and blockage intensity epsilon
        """
        self.b = particles
        self.n = 2*self.b
        self.p = p
        self.e = epsilon
        npr.seed()
        self.sigma = self.initSigma()
        self.current = []

    def __repr__(self):
        return 'Parallel TASEP on a ring of size %d (p=%.3f, e=%.3f)' % (self.n, self.p, self.e)

    def initSigma(self):
        """
        Lorem ipsum
        """
        return np.sort(npr.choice(self.n, size=self.b, replace=False), kind='mergesort')

    def updateSigma(self):
        """
        Lorem ipsum
        """
        freetomove = np.nonzero( np.roll(self.sigma, -1) - (self.sigma + 1)%self.n )[0]
        self.current.append(len(freetomove)/float(self.n))
        updates = npr.choice(np.arange(2), size=len(freetomove), replace=True, p=np.array([1.-self.p, self.p]))
        if self.sigma[freetomove[-1]] == self.n-1 and updates[-1] == 1:
            blockupdate = 0 if npr.random() < self.e else 1
            updates[-1] = blockupdate
        self.sigma[freetomove] += updates
        self.sigma[-1] = self.sigma[-1] % self.n
        if not self.sigma[-1]:
            self.sigma = np.roll(self.sigma, 1)

    def denseSigma(self):
        """
        Export the configuration as a numpy vector of size self.n, tau
        tau[i] == 1 iff there is a particle in the ith position
        """
        tau = np.zeros(self.n)
        tau[self.sigma] = 1
        return tau

    def density(self, graining):
        """
        graining is a 1D vector that indicates where to split the ring
        """
        sections = np.split(self.denseSigma(), graining)
        return map(densityReduction, sections)



# def main():
#     n = 10			      #POSIZIONI, QUINDI N/2 PALLINE ecc ecc
#     T = n
#     d = 0.5
#     camp = 5					    #estensione del campione di posizioni

#     P = np.arange(0.0, 1+d, d)        #array contente le 11 probabilita' usate da 0.0 a 1.0
#     E = np.arange(0.0, 1+d, d)        #array contente le 11 epsilon usate da 0.0 a 1.0
#     P[0]= 1/float(n/2)		      #in questo modo la prima probabilita' non e' 0.0 ma 1/numero palline

#     X = np.arange(0.0, 1+d, d)        #mi serve solo per preparare una matrice pxe
#     Y = np.arange(0.0, 1+d, d)
#     X, Y = np.meshgrid(X, Y)
#     ZETA = X    

#     print '\nTASEP termic simulation \n','posizioni n =',n,', T = (n/p) * log(n), d =',d,', campione =',camp
#     print 'tempo inizio simulazione: \t', datetime.datetime.now(),'\n'    
#     for y in [0]:
#         DEN = []
#         evo = []
#         for k in range(len(E)):
#             tasep_inst = Tasep(n, P[y], E[k])
#             Lt = []   

#         for i in range(int((T/P[y]))):#*np.log(n))):  #questo e il tempo di termalizzazione
#             tasep_inst.update()
#             Z = tasep_inst.corrente(Lt)/float(n)
#             print 'p =', P[y], '\t e =', E[k], '\t', datetime.datetime.now()
#             ZETA[y][k] = Z
#         DEN.append(tasep_inst.density(camp))
#         evo.append(tasep_inst.evolution(camp))

#     np.save("densita%d" %(n,y), DEN)
#     np.save('Jn%d_d=0.%d' %(n, d*10), ZETA)
#     print '\ntempo fine simulazione: \t', datetime.datetime.now(),'\n'

# if __name__ == '__main__':
#     main()
