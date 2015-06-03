import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from scipy import stats

#p = 0.5
e = 0.1
qth = [25,50,75,90]

nomefile = './N*' + '_B*' + '_p=1su2L_e0.0.npy'
nomefile = glob(nomefile) 

data = []
N = []
medie = []
mediane = []
massimi = []
perc = []

nomefile.sort(key=lambda x:int(x.split('_')[1][1:])) 
'''
questo sort e' la ostia, Carlo tu avevi dimenticato l'int() e non
funzionava!
'''
for f in nomefile:
	N.append(2*int(f.split('_')[1][1:]))
	data.append(np.load(f))
	medie.append(np.mean(data[-1]))
	massimi.append(max(data[-1]))
	mediane.append(np.median(data[-1]))
	perc.append(np.percentile(data[-1], qth))

perc = np.array(perc)
perc= perc.T

xi = np.zeros(len(N))
for i in range(len(N)):
	xi[i] = N[i] - 10

Eslope, Eintercept, Er_value, Ep_value, Estd_err = stats.linregress(xi, medie)
Mslope, Mintercept, Mr_value, Mp_value, Mstd_err = stats.linregress(xi, massimi)
MEDslope, MEDintercept, MEDr_value, MEDp_value, Mstd_err = stats.linregress(xi, mediane)

fig, (ax, bx, cx) = plt.subplots(ncols=3)

fig.suptitle('Coalescence Times for Parallel TASEP p=1/2L e=0.0', fontsize=18)

Eline = Eslope*xi + Eintercept
MEDline = MEDslope*xi + MEDintercept
Mline = Mslope*xi + Mintercept

ax.plot(N,Eline,'r-',N,medie,'o')
ax.set_ylabel('Mean of Coalescence Times', fontsize=15)
ax.set_xlabel('Number of Sites of the Ring')
ax.text(15,35, 'Slope = %f \nIntercept = %f' %(Eslope, Eintercept), fontsize=16)

bx.plot(N,MEDline,'r-',N,mediane,'x')
bx.set_ylabel('Median of Coalescence Times', fontsize=15)
bx.set_xlabel('Number of Sites of the Ring')
bx.text(15, 15, 'Slope = %f \nIntercept = %f' %(MEDslope, MEDintercept), fontsize=16)

cx.plot(N,Mline,'r-',N,massimi,'g^')
cx.text(15, 1000, 'Slope = %f \nIntercept = %f' %(Mslope, Mintercept), fontsize=16)
cx.set_ylabel('Max of Coalescence Times', fontsize=15)
cx.set_xlabel('Number of Sites of the Ring')

plt.show()

fig = plt.figure()

# for row, lab in zip(perc[::-1],qth[::-1]): 
# 	plt.plot(N,row, label=lab)
# '''
# ho usato la extended slice syntax solo per avere la legenda in ordine decrescente
# '''
# plt.legend(loc=2, title= 'Percentiles')
# plt.ylabel('Values of Percentiles of Coalescence Times')
# plt.xlabel('Number of Sites of the Ring')
# plt.title('Percentiles of Coealescence Times of Parallel TASEP p0.5 e0.1')

# plt.show(fig)