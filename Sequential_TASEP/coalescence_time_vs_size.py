import matplotlib.pyplot as plt
import numpy as np
from glob import glob

#N = 20
B = 10
p = 0.5
e = 0.1

nomefile = './N*' + '_B*' + '_p' + str(p) + '_e' + str(e) +'.npy'
nomefile = glob(nomefile) 

data = []
N = []

nomefile.sort(key=lambda x: x.split('_')[1][1:4])

for f in nomefile:
    N.append(2*float(f.split('_')[1][1:4]))
    data.append(np.load(f))

fig, ax = plt.subplots()


plt.boxplot(data)

ax.set_ylabel('Coalescence Times')
ax.set_xlabel('Number of Sites of the Ring')
plt.title('Parallel TASEP with blockage 0.1 and update probability {prob}'.format(prob=p))
#plt.grid(True)
#plt.savefig('%s.png' %(nomefile))
xtickNames = plt.setp(ax, xticklabels=N)
plt.setp(xtickNames, rotation=45, fontsize=10)
plt.show()

