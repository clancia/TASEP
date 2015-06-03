import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from scipy import stats
#import statistics as st

#p = 0.5
e = 0.1
qth = [25,50,75,90]

#insert the probability to load
p = 0.5

nomefile = './p=%.1f/N*' %(p) + '_B*' + 'p*' + '.npy' 
nomefile = glob(nomefile) 

data = []
N = []
medie = []
mediane = []
massimi = []
perc = []
var = []

nomefile.sort(key=lambda x:int(x.split('_')[1][1:])) 
'''
questo sort e' la ostia, Carlo tu avevi dimenticato l'int() e non
funzionava!
'''
for f in nomefile:
	N.append(2*int(f.split('_')[1][1:]))
	data.append(np.load(f))
	var.append(np.log(np.var(data[-1])))
	medie.append(np.mean(np.log(data[-1])))
	massimi.append(max(np.log(data[-1])))
	mediane.append(np.median(np.log(data[-1])))
	perc.append(np.percentile(data[-1], qth))

perc = np.array(perc)
perc= perc.T

xi = np.zeros(len(N))
for i in range(len(N)):
	xi[i] = np.log(N[i])# - 10)

Vslope, Vintercept, Vr_value, Vp_value, Vstd_err = stats.linregress(xi, var)
Eslope, Eintercept, Er_value, Ep_value, Estd_err = stats.linregress(xi, medie)
Mslope, Mintercept, Mr_value, Mp_value, Mstd_err = stats.linregress(xi, massimi)
MEDslope, MEDintercept, MEDr_value, MEDp_value, Mstd_err = stats.linregress(xi, mediane)

fig, (ax, bx, cx, dx) = plt.subplots(ncols=4)

fig.suptitle('LogLog of Coalescence Times of $\sigma^{o|x}$ and $\sigma^{x|o}$ for Sequential TASEP with p=%.3f e=0.0' %(p), fontsize=18)

Vline = Vslope*xi + Vintercept
Eline = Eslope*xi + Eintercept
MEDline = MEDslope*xi + MEDintercept
Mline = Mslope*xi + Mintercept

ax.plot(xi,Eline,'r-',xi,medie,'o')
ax.set_ylabel('Mean of Coalescence Times', fontsize=15)
ax.set_xlabel('Number of Sites of the Ring')
ax.text(xi[0],medie[-7], 'Slope = %f \nIntercept = %f' %(Eslope, Eintercept), fontsize=16)

bx.plot(xi,MEDline,'r-',xi,mediane,'x')
bx.set_ylabel('Median of Coalescence Times', fontsize=15)
bx.set_xlabel('Number of Sites of the Ring')
bx.text(xi[0], mediane[-2], 'Slope = %f \nIntercept = %f' %(MEDslope, MEDintercept), fontsize=16)

cx.plot(xi,Mline,'r-',xi,massimi,'g^')
cx.text(xi[0], massimi[-2], 'Slope = %f \nIntercept = %f' %(Mslope, Mintercept), fontsize=16)
cx.set_ylabel('Max of Coalescence Times', fontsize=15)
cx.set_xlabel('Number of Sites of the Ring')

dx.plot(xi,Vline,'r-',xi,var,'x')
dx.set_ylabel('Variance of Coalescence Times', fontsize=15)
dx.set_xlabel('Number of Sites of the Ring')
dx.text(xi[0], var[-5], 'Slope = %f \nIntercept = %f' %(Vslope, Vintercept), fontsize=16)


plt.show()

fig = plt.figure()