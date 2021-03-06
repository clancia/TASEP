#!/usr/bin/env python

import parall_tasep as pt
import numpy as np
import logging
import matplotlib.pyplot as plt
import sys

import argparse

parser = argparse.ArgumentParser(description='Per-site average occupancy of Totally Asymmetric Simple Exclusion Process with blockage')
parser.add_argument('balls', type=int, help='Number of particles in the system')
parser.add_argument('-n', '--nsites', default=0, type=int, help='Number of sites in the system; defaults to twice the particles')
parser.add_argument('-p', '--prob', default=.5, type=float, help='Probability of each particle taking a move if free; defaults to 0.5')
parser.add_argument('-e', '--epsilon', default=.05, type=float, help='Blockage intensity; defaults to 0.05')

args = parser.parse_args()

balls = args.balls
sites = args.nsites if args.nsites else 2*balls
prob = args.prob
epsilon = args.epsilon
iterations = 1000000

logger = logging.getLogger(__name__)


def initialConfigByCoalescence():
    cpl = pt.CouplingSameSite(balls, sites, prob, epsilon)
    cpl.sigma = np.arange(cpl.b) + cpl.n - cpl.b
    cpl.tau = np.arange(cpl.b)
    logger.info('Coupling created and started. Waiting for coalescence...')
    counter = 0
    flag = 1
    while flag:
        flag = cpl.update()
        counter += 1
    logger.info('Coalescence achieved in %d steps.' % (counter))
    npy_file = pt.PATH_TO_NPY + 'N' + str(cpl.n) \
            + '_B' + str(cpl.b)\
            + '_p' + str(cpl.p)\
            + '_e' + str(cpl.e) + '.npy'
    np.save(npy_file, cpl.sigma)

tsp = pt.Tasep(balls, sites, prob, epsilon, False)
flag = None
try:
    tsp.sigma = tsp.loader()
except IOError as e:
    if e.errno == 2:
        logger.info('Initial configuration file is missing. An initial equilibrium configuration will be generated by coupling.')
        flag = 1
    else:
        sys.exit('I/O error({0}): {1}'.format(e.errno, e.strerror))

if flag:
    initialConfigByCoalescence()
    tsp.sigma = tsp.loader()

persite_avg = np.zeros(sites, dtype=np.float64)

logger.info('Simulating per-site average occupancy. This may take a while...')

divider = int(iterations/100.0)
for i in xrange(iterations):
    tsp.update()
    persite_avg += tsp.fullsigma
    if not (i+1)%divider:
        logger.info('Completed ' + str((i+1)/divider) + '%')
persite_avg /= iterations

logger.info('Simulation completed. Plotting...')

plt.figure()
plt.plot(persite_avg)
plt.xlabel('site')
plt.ylabel('average occupancy')
plt.suptitle('Parallel TASEP on a ring of size {0} with p={1} and e={2}'.format(sites, prob, epsilon))
plt.show()

logger.info('Execution completed.')

