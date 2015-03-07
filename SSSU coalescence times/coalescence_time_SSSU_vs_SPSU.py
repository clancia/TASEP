import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# N = 20
# B = 10
# p = 0.5

# nomefile = './N' + str(N) + '_B' + str(B) + '_p' + str(p) + '_e*.npy'
# nomefile = glob(nomefile) 

data = []
# epsilon = []

# nomefile.sort(key=lambda x: x.split('_')[-1][1:-4])

# for f in nomefile:
#     epsilon.append(float(f.split('_')[-1][1:-4]))


data.append(np.load('N20_B10_p0.5_e0.10.npy'))
data.append(np.load('./SPSU/ryN20_B10_p0.5_e0.1.npy'))

fig, ax = plt.subplots()

plt.boxplot(data)

ax.set_ylabel('Coalescence Times')
ax.set_xlabel('SSSU vs SPSU')
#plt.title('Parallel TASEP with blockage ({particles} particles and update probability {prob})'.format(particles=B, prob=p))
#plt.grid(True)
#plt.savefig('%s.png' %(nomefile))
#xtickNames = plt.setp(ax, xticklabels=epsilon)
#plt.setp(xtickNames, rotation=45, fontsize=10)
plt.show()

