#!/usr/bin/env python

import numpy as np
import numpy.random as npr
import logging
import logging.config
import sys
import os.path
import time
#import pdb

PATH_TO_NPY = './npys/'

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def coalescence(b, n=None, p=0.5, e=0.05):
    """
    Simulate an instance of Coupling until coalescence is reached
    Return the coalescence time
    """
    c = Coupling(b, n, p, e)
    counter = 0
    flag = 1
    while flag:
        flag = c.update()
        counter += 1
    return counter

def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

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
    """
    Parallel TASEP on a 1D-ring of length 2*particles with update probability and blockage intensity epsilon
    """
    def __init__(self, particles, size=None, p=.5, epsilon=.05):
        self.b = particles
        # how many particles in the tasep
        if size is not None:
            self.n = size
        else:
            self.n = 2*self.b
            # the size of the ring defaults to twice the number of particles
        self.p = p
        self.e = epsilon
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        npr.seed()
        self.npy = PATH_TO_NPY + 'N' + str(self.n) \
            + '_B' + str(self.b)\
            + '_p' + str(self.p)\
            + '_e' + str(self.e) + '.npy'
        self._sigma = self.initSigma()
        # The configuration of the tasep is represented by a vector of positions
        # sigma[i] = where is located the ith particle
        self.current = []
        self.logger.debug('Instance created.')

    def __repr__(self):
        return 'Parallel TASEP :: %d particles, ring length %d, p=%.3f, e=%.3f' % (self.b, self.n, self.p, self.e)

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        self._sigma = value

    def dumper(self):
        self.logger.info('Trying to save current configuration to .npy file...')
        try:
            np.save(self.npy, self.sigma)
        except IOError as e:
            self.logger.error('Failed to save .npy file. I/O error({0}): {1}'.format(e.errno, e.strerror))
        else:
            self.logger.info('Configuration saved successfully.')


    def loader(self):
        self.logger.info('Trying to load current configuration to .npy file...')
        try:
            loaded = np.load(self.npy)
        except IOError as e:
            self.logger.error('Failed to load .npy file. I/O error({0}): {1}'.format(e.errno, e.strerror))
        else:
            self.logger.info('Configuration loaded successfully.')
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
        Return an initial configuration sigma (either a previously-dumped or a new random configuration)
        """
        answer = False
        if os.path.isfile(self.npy):
            last_modified = time.ctime(os.path.getmtime(self.npy))
            created = time.ctime(os.path.getctime(self.npy))
            print 'There exists a save of the configuration sigma:'
            print '- created on', created
            print '- last modified', last_modified
            print ''
            self.logger.debug('Previously saved configuration exists. Waiting for user...')
            answer = query_yes_no('Do you want to load it?')
        if answer:
            self.logger.debug('Positive answer.')
            return self.loader()
        else:
            # sigma is initialized to a sorted vector of random numbers in [0, n-1]
            # each entry of the vector is the spatial position of a particle on the ring
            self.logger.debug('Negative answer.')
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
        # THIS WILL RAISE AN ERROR IF self.n == self.b BUT THIS IS SOMETHING VERY STUPID
            # if there's a particle at site n-1 about to move, then we move it with probability 1-epsilon
            # all in all, that particle is moved with probability p*(1-epsilon) (blockage)
            blockupdate = 0 if npr.random() < self.e else 1
            updates[-1] = blockupdate
        self.sigma[freN10_B5_p0.5_e0.05.npyetomove] += updates
        # the particles selected to be moved go to the next position
        self.sigma[-1] = self.sigma[-1] % self.n
        # the last particle may go to site n, so we apply the periodic boundary conditions
        if not self.sigma[-1]:
            self.sigma = np.roll(self.sigma, 1)
            # if the last particle has completed one loop (i.e. it is in position 0)
            # then we apply the periodic boundary condition by rolling the configuration

    def density(self, graining):
        """
        Return the particles density using a coarse-graining of the ring
        INPUT: graining is a 1D vector that indicates where to split the ring
        """
        sections = np.split(self.fullsigma, graining)
        # the ring is split into subarrays according to graining,
        # then np.mean is applied to each subarray
        return map(np.mean, sections)

class Coupling(object):
    """
    Parallel TASEP on a 1D-ring of length 2*particles with update probability and blockage intensity epsilon
    """
    def __init__(self, particles, size=None, p=.5, epsilon=.05):
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
        ################################################################
        # considerare di rendere inizializzazione sigma/tau piu' dinamica
        self._sigma = np.arange(self.b) + self.n - self.b
        self._tau = np.arange(self.b)
        ################################################################

    def __repr__(self):
        return 'Coupling of two parallel TASEPs :: %d particles, ring length %d, p=%.3f, e=%.3f' % (self.b, self.n, self.p, self.e)

    @property
    def sigma(self):
        return self._sigma
    @sigma.setter
    def sigma(self, value):
        self._sigma = value

    @property
    def tau(self):
        return self._tau
    @tau.setter
    def tau(self, value):
        self._tau = value
    
    def update(self):
        """
        Jointly update the coupled configurations sigma and tau
        Free particles occupying the same site in both configurations take the same update
        The remaining free particles are updated indipendently
        """
        s_freetomove = np.nonzero( np.roll(self.sigma, -1) - (self.sigma + 1)%self.n )[0]
        t_freetomove = np.nonzero( np.roll(self.tau, -1) - (self.tau + 1)%self.n )[0]
        # find sites occupied by particles that are free to move in sigma or tau, respectively
        bothfree = np.intersect1d(self.sigma[s_freetomove], self.tau[t_freetomove], assume_unique=True)
        s_bothfree = np.nonzero(np.in1d(self.sigma, bothfree, assume_unique=True))[0]
        t_bothfree = np.nonzero(np.in1d(self.tau, bothfree, assume_unique=True))[0]
        # find sites that are occupied by particles that are simultaneously free to move in both sigma and tau
        s_free_only = np.setdiff1d(s_freetomove, s_bothfree)
        t_free_only = np.setdiff1d(t_freetomove, t_bothfree)
        # find sites ocupied by particles that are free to move in sigma only or in tau only, respectively 
        b_updates = npr.choice(np.arange(2), size=len(bothfree), replace=True, p=np.array([1.-self.p, self.p]))
        # select for updates particles free to move both in sigma and tau
        s_updates = npr.choice(np.arange(2), size=len(s_free_only), replace=True, p=np.array([1.-self.p, self.p]))
        t_updates = npr.choice(np.arange(2), size=len(t_free_only), replace=True, p=np.array([1.-self.p, self.p]))
        # select for updates particles free to move in sigma only or in tau only, respectively
        try:
            common_particle_before_blockage = (bothfree[-1] == self.n-1 and b_updates[-1] == 1)
        except IndexError:
            common_particle_before_blockage = False
        
        try:
            sigma_particle_before_blockage = (self.sigma[s_freetomove[-1]] == self.n-1 and s_updates[-1] == 1)
        except IndexError:
            sigma_particle_before_blockage = False
        
        try:
            tau_particle_before_blockage = (self.tau[t_freetomove[-1]] == self.n-1 and t_updates[-1] == 1)
        except IndexError:
            tau_particle_before_blockage = False

        if common_particle_before_blockage:
            # if there's a particle at site n-1 about to move, then we move it with probability 1-epsilon
            # all in all, that particle is moved with probability p*(1-epsilon) (blockage)
            blockupdate = 0 if npr.random() < self.e else 1
            b_updates[-1] = blockupdate

        if sigma_particle_before_blockage:
            # if there's a particle at site n-1 about to move, then we move it with probability 1-epsilon
            # all in all, that particle is moved with probability p*(1-epsilon) (blockage)
            blockupdate = 0 if npr.random() < self.e else 1
            s_updates[-1] = blockupdate

        if tau_particle_before_blockage:
            # if there's a particle at site n-1 about to move, then we move it with probability 1-epsilon
            # all in all, that particle is moved with probability p*(1-epsilon) (blockage)
            blockupdate = 0 if npr.random() < self.e else 1
            t_updates[-1] = blockupdate
        
        self.sigma[s_bothfree] += b_updates
        self.tau[t_bothfree] += b_updates
        self.sigma[s_free_only] += s_updates
        self.tau[t_free_only] += t_updates
        # update sigma and tau
        self.sigma[-1] = self.sigma[-1] % self.n
        self.tau[-1] = self.tau[-1] % self.n
        # apply periodic boundary conditions to the last particle
        if not self.sigma[-1]:
            self.sigma = np.roll(self.sigma, 1)
        if not self.tau[-1]:
            self.tau = np.roll(self.tau, 1)
        # if the last particle has completed one loop (i.e. it is in position 0)
        # then we apply the periodic boundary condition by rolling the configuration
        return np.sum(np.absolute(self.sigma - self.tau))
        # if the function returns 0 then coalescence was reached
