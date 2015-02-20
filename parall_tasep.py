#!/usr/bin/env python

import numpy as np
import numpy.random as npr
import logging
import logging.config
import sys
import os.path
import time
#import datetime
#import pdb

PATH_TO_NPY = './npys/'

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " (y/n) "
    elif default == "yes":
        prompt = " ([y]/n) "
    elif default == "no":
        prompt = " (y/[n]) "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class Tasep(object):
    def __init__(self, particles, size=None, p=.5, epsilon=.05):
        """
        Parallel TASEP on a 1D-ring of length 2*particles with update probability and blockage intensity epsilon
        """
        self.b = particles
        # how many particles in the tasep
        if size is not None:
            self.n = size
        else:
            self.n = 2*self.b
            # the size of the ring defaults to twice the number of particles
        self.p = p
        self.e = epsilon
        npr.seed()
        self.npy = PATH_TO_NPY + 'N' + str(self.n) \
            + '_B' + str(self.b)\
            + '_p' + str(self.p)\
            + '_e' + str(self.e) + '.npy'
        self._sigma = self.initSigma()
        # The configuration of the tasep is represented by a vector of positions
        # sigma[i] = where is located the ith particle
        self.current = []
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        self.logger.debug('Instance created.')

    def __repr__(self):
        return 'Parallel TASEP on a ring of size %d (p=%.3f, e=%.3f)' % (self.n, self.p, self.e)

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        self._sigma = value

    def dumper(self):
        np.save(self.npy, self.sigma)

    def loader(self):
    	try:
    		loaded = np.load(self.npy)
    	except IOError as e:
    		self.logger.error("Failed to load .npy file. I/O error({0}): {1}".format(e.errno, e.strerror))
        return loaded
    
    @property
    def fullsigma(self):
        """
        Return the configuration as a numpy vector of size self.n, tau,
        where tau[i] == 1 iff there is a particle in the ith position
        """
        return self._fullsigma()

    def _fullsigma(self):
        tau = np.zeros(self.n)
        tau[self.sigma] = 1
        return tau

    def initSigma(self):
        """
        Initialize sigma either to a previously-dumped or to a new configuration
        """
        answer = False
        if os.path.isfile(self.npy):
            last_modified = time.ctime(os.path.getmtime(self.npy))
            created = time.ctime(os.path.getctime(self.npy))
            print 'There exists a save of the configuration sigma:'
            print '- created on', created
            print '- last modified', last_modified
            print ''
            answer = query_yes_no('Do you want to load it?')
        if answer:
            return self.loader()
        else:
            # sigma is initialized to a sorted vector of random numbers in [0, n-1]
            # each entry of the vector is the spatial position of a particle on the ring
            return np.sort(npr.choice(self.n, size=self.b, replace=False), kind='mergesort')

    def update(self):
        """
        Update the configuration sigma applying one step of the TASEP dynamics
        """
        freetomove = np.nonzero( np.roll(self.sigma, -1) - (self.sigma + 1)%self.n )[0]
        # Particle at site i is not free to move if there is another particle at site i+1 (mod n),
        # i.e. if sigma[i+1] == sigma[i]+1
        self.current.append(len(freetomove)/float(self.n)) 
        # Append the latest value of the current
        updates = npr.choice(np.arange(2), size=len(freetomove), replace=True, p=np.array([1.-self.p, self.p]))
        # We choose which particles to move one step ahead among those free-to-move independently with probability p
        if self.sigma[freetomove[-1]] == self.n-1 and updates[-1] == 1:
            # if there's a particle at site n-1 about to move, then we move it with probability 1-epsilon
            # all in all, that particle is moved with probability p*(1-epsilon) (blockage)
            blockupdate = 0 if npr.random() < self.e else 1
            updates[-1] = blockupdate
        self.sigma[freetomove] += updates
        # the particles selected to be moved go to the next position
        self.sigma[-1] = self.sigma[-1] % self.n
        # the last particle may go to site n, so we apply the periodic boundary conditions
        if not self.sigma[-1]:
            self.sigma = np.roll(self.sigma, 1)

    def density(self, graining):
        """
        Return the particles density using a coarse-graining of the ring
        INPUT: graining is a 1D vector that indicates where to split the ring
        """
        sections = np.split(self.fullsigma, graining)
        # the ring is split into subarrays according to graining,
        # then np.mean is applied to each subarray
        return map(np.mean, sections)
