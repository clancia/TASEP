import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# N = 20
# B = 10
# p = 0.5

# nomefile = './N' + str(N) + '_B' + str(B) + '_p' + str(p) + '_e*.npy'
# nomefile = glob(nomefile) 

# epsilon = []

# nomefile.sort(key=lambda x: x.split('_')[-1][1:-4])

# for f in nomefile:
#     epsilon.append(float(f.split('_')[-1][1:-4]))


data0=np.load('SSN20_B10_p0.5_e0.1.npy')
data1=np.load('SPN20_B10_p0.5_e0.1.npy')

fig, (ax0,ax1) = plt.subplots(ncols=2)
fig.suptitle('Parallel TASEP with blockage Same Site vs Same Particle Coalescence Times', fontsize=18)


#plt.boxplot(data)
ax0.set_ylabel('Coalescence Times', fontsize=15)
ax0.set_xlabel('Same Site Same Update', fontsize=15)
ax1.set_xlabel('Same Particle Same Update', fontsize=15)

ax0.boxplot(data0)
ax1.boxplot(data1)

#plt.grid(True)
#plt.savefig('%s.png' %(nomefile))
#xtickNames = plt.setp(ax, xticklabels=epsilon)
#plt.setp(xtickNames, rotation=45, fontsize=10)
plt.show()

