import numpy as np
import parall_tasep as pt
from glob import glob 

def carica(balls):
  d = []
  for i in range(100):
    d.append(np.load('./SSparts/B%d_%d.npy' %(balls, i)))
  TM = np.concatenate(np.array(d))
  ofile = 'N%d_B%d_p0.5_e0.1.npy' %(2*balls, balls) 
  np.save(ofile, TM)

def foo(balls,p):
   N=10000
   TM = np.zeros(N)
   part = []
   print 'Inizio simulazione balls = %d, p=%.3f, e=0.0' %(balls,p) 
   for i in xrange(N):
       TM[i] = pt.seqHIT(balls, p)
       part.append(TM[i])
       if not (i+1)%100:
           print str((i+1)/100.0) + ' %'
           #np.save('./SSparts/B%d_%d.npy' %(balls, i/100.0), part)
           part = []
   ofile = './hit/Nhit%d_B%d_p=%.3f_e0.0.npy' %(2*balls, balls,p) 
   np.save(ofile, TM)

def esistenti():   #legge se gia' esistono file con N siti
  nomefile = './hit/N*' + '_B*'  
  nomefile = glob(nomefile) 
  N = []
  nomefile.sort(key=lambda x:int(x.split('_')[1][1:]))
  for f in nomefile:
	N.append(2*int(f.split('_')[1][1:]))
  return N

p = float(0.5)
N = np.arange(10,1000,10)
for i in N:
	if not i in esistenti():
		print foo(i/2, p)

  