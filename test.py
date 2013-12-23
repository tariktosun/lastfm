# SVD testing:

# Perform SVD
#U, s, V = np.linalg.svd(binary, full_matrices=True)

# Project onto PC's 2 and 3:
#v = V[:,1:3]
import pickle
import matplotlib.pyplot as plt
from process import *

full_data = load_data('json/scrobbles')
(sid_timeseries, time_timeseries, sid_to_mbid, mbid_to_meta) = get_timeseries(full_data)
(sid_bundles, time_bundles) = get_bundles(time_timeseries, sid_timeseries)
binary = get_binary(sid_bundles, len(sid_to_mbid))

usv = pickle.load( open("usv.p", "rb"))
U = usv['U']
V = usv['V']
s = usv['s']

v = V
proj = np.dot( v.transpose(), binary.transpose() )

# find largest:
norms = np.sum(np.abs(proj)**2,axis=0)**(1./2)
idx = np.argsort(norms)
idx = idx[::-1] # put in ascending order
top = proj[:,idx[0:30]]
names = [ mbid_to_meta[sid_to_mbid[sid]]['artist']['name'] for sid in idx[0:30] ]

pc2 = proj[0,:]
pc3 = proj[1,:]
idx2 = np.argsort(pc2)
idx2 = idx2[::-1]
idx3 = np.argsort(pc3)
idx3 = idx3[::-1]

top_2 = proj[:,idx2[0:10]]
top_3 = proj[:,idx3[0:10]]

names3 = [ mbid_to_meta[sid_to_mbid[sid]]['name'] for sid in idx3[0:10] ]
names2 = [ mbid_to_meta[sid_to_mbid[sid]]['name'] for sid in idx2[0:10] ]

plt.ion()
plt.figure()
for i in xrange(len(names)):
    x = top[0,i]
    y = top[1,i]
    s = names[i]
    plt.text(x,y,s)

plt.xlim((-2,2))
plt.ylim((-2,2))
