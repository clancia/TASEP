import matplotlib.pyplot as plt
import numpy as np
from glob import glob

nomefile = glob('./N20_B10_p0.5_e*.npy') 

data = []
epsilon = []

nomefile.sort(key=lambda x: x.split('_')[-1].split('.')[1])

for f in nomefile:
    e = f.split('_')[-1].split('.')[1]
    epsilon.append(float('0.'+ e))
    data.append(np.load(f))

fig, ax = plt.subplots()

plt.boxplot(data)

ax.set_ylabel('Coalescence Times')
ax.set_xlabel('Value of blockage intensity')
#plt.set_title('Mixing times')
#plt.grid(True)
#plt.savefig('%s.png' %(nomefile))
xtickNames = plt.setp(ax, xticklabels=epsilon)
plt.setp(xtickNames, rotation=45, fontsize=8)
plt.show()

