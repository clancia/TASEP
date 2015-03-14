import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from scipy import stats

p = 0.5
e = 0.1

nomefile = './N*' + '_B*' + '_p' + str(p) + '_e' + str(e) +'.npy'
nomefile = glob(nomefile) 

data = []
N = []
medie = []
massimi = []

nomefile = np.sort(nomefile)

for f in nomefile:
    N.append(2*int(f.split('_')[1][1:4]))
    data.append(np.load(f))
    medie.append(np.mean(data[-1]))
    massimi.append(max(data[-1]))

xi = np.zeros(len(N))
for i in range(len(N)):
	xi[i] = N[i] - 10

Eslope, Eintercept, Er_value, Ep_value, Estd_err = stats.linregress(xi, medie)
Mslope, Mintercept, Mr_value, Mp_value, Mstd_err = stats.linregress(xi, massimi)

fig, (ax, bx) = plt.subplots(ncols=2)

fig.suptitle('Parallel TASEP with blockage Same Site vs Same Particle Coalescence Times', fontsize=18)

Eline = Eslope*xi + Eintercept
Mline = Mslope*xi + Mintercept

ax.plot(N,Eline,'r-',N,medie,'o')


ax.set_ylabel('Mean of Coalescence Times')
ax.set_xlabel('Number of Sites of the Ring')
#plt.title('Parallel TASEP p0.5 e0.1 line regression of the Mean Coalescence Times')
ax.text(60, 112, 'Slope = %f \nIntercept = %f' %(Eslope, Eintercept), fontsize=16)



bx.plot(N,Mline,'r-',N,massimi,'g^')
bx.text(65, 60000, 'Slope = %f \nIntercept = %f' %(Mslope, Mintercept), fontsize=16)
bx.set_ylabel('Max of Coalescence Times')
bx.set_xlabel('Number of Sites of the Ring')
#plt.title('Parallel TASEP e0.1 p0.5 line regression of the Max Coalescence Times')
plt.show()
