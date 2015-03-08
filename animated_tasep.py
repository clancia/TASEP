#!/usr/bin/env python

import parall_tasep as pt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import gridspec
import argparse

parser = argparse.ArgumentParser(description='Totally Asymmetric Simple Exclusion Process with blockage')
parser.add_argument('balls', type=int, help='Number of particles in the system')
#parser.add_argument('-n', '--nsites', default=0, type=int, help='Number of sites in the system; defaults to twice the particles')
parser.add_argument('-p', '--prob', default=.5, type=float, help='Probability of each particle taking a move if free; defaults to 0.5')
parser.add_argument('-e', '--epsilon', default=.05, type=float, help='Blockage intensity; defaults to 0.05')

args = parser.parse_args()

b = args.balls
#n = args.nsites if args.nsites else 2*b
n = 2*b
p = args.prob
e = args.epsilon

BUFFERSIZE = 500

CIRCLE_RADIUS = 1
PLOT_RADIUS = 3 * CIRCLE_RADIUS * n / np.pi

tsp = pt.Tasep(b, size=n, p=p, epsilon=e, loadcheck=False)

nx = 10.
ny = 10.

rx, ry = 1., 5.

fig = plt.figure()
#ax1 = fig.add_subplot(1, 2, 1)
#ax2 = fig.add_subplot(1, 2, 2)
gs = gridspec.GridSpec(2, 1, width_ratios=[2,1], height_ratios=[4,1])
gs.update(left=0.3)
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

if e:
    ax1.axis([-PLOT_RADIUS -nx, PLOT_RADIUS +nx, -PLOT_RADIUS -ny/2, PLOT_RADIUS +1.5*ny])
else:
    ax1.axis([-PLOT_RADIUS -nx, PLOT_RADIUS +nx, -PLOT_RADIUS -ny, PLOT_RADIUS +ny])

ax1.set_aspect('equal')
ax2.axis([1, BUFFERSIZE, 0, .55])

def equallySpacedPointsOnACircle(howmany, rho):
    thetas = np.linspace(0, -2*np.pi, 2*howmany, endpoint=False)
    xx = rho*np.cos(thetas + np.pi/2 - np.pi/b)
    yy = rho*np.sin(thetas + np.pi/2 - np.pi/b)
    return zip(xx, yy)

def init():
    global patches, current, line
    positions = equallySpacedPointsOnACircle(b, PLOT_RADIUS)
    # initialize an empty list of cirlces
    ax1.add_patch( plt.Circle((0,0), radius=PLOT_RADIUS, fc='none', ec='k', ls='dotted') )
    ax1.set_title('Parallel TASEP on a ring of size {0}'.format(n))
    if e > 0:
        ax1.add_patch( plt.Rectangle((-rx/2, PLOT_RADIUS - ry/2), rx, ry, fc='k', alpha=0.75 ) )
        ax1.text(0, PLOT_RADIUS + 1.5*ry, r'Blockage intensity e={0}'.format(e), horizontalalignment='center')
    patches = [ ax1.add_patch( plt.Circle(p, radius=CIRCLE_RADIUS, fc='none', ec='k', ls='dotted') ) for p in positions ]
    current = np.zeros(BUFFERSIZE, dtype=np.float64)
    ax2.set_title('Empirical current (avg number of engines)')
    ax2.set_xlabel('Last {0} steps'.format(BUFFERSIZE))
    line, = ax2.plot([], 'g-', lw=2)
    return patches, line

def animate(i):
    global patches, current, line
    for p, s in zip(patches, tsp.fullsigma):
        if s:
            p.set_facecolor('r')
            p.set_edgecolor('none')
            p.set_linestyle('solid')
        else:
            p.set_facecolor('w')
            p.set_edgecolor('none')
            #p.set_linestyle('solid')
    current = np.roll(current, 1)
    a = tsp.fullsigma
    current[0] = np.sum( np.logical_and( a, np.logical_xor( a, np.roll(a, -1) ) ) )/float(n)
    #line1.set_data(np.arange(100), current1)
    line.set_data(np.arange(BUFFERSIZE), current)
    tsp.update()
    return patches, line

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=100)
#anim.save('live_tasep.mp4', fps=5)#, extra_args=['-vcodec', 'libx264'])
plt.show()