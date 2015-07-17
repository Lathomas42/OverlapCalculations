import catmaid
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import csv

csv_w = csv.writer(open('ax.csv','wb'))
csv_2 = csv.writer(open('den.csv','wb'))
c=catmaid.connection.Connection('http://catmaid.hms.harvard.edu','thomas.lo','asdfjkl;',9)
src = catmaid.get_source(c)

n1 = src.get_neuron(325123)
n2 = src.get_neuron(38321)
g1 = catmaid.algorithms.morphology.resample_edges_2(n1,400.,['axon'])
g2 = catmaid.algorithms.morphology.resample_edges_2(n2,400.,['dendrite'])
t_s = catmaid.algorithms.population.synapses.skeleton_overlap_v_verbose_ids(n1,n2,1000.,10000.,g1,g2)

fig = plt.figure()
ax = fig.gca(projection='3d')
min_r = float(t_s[0][2])
max_r = min_r
sum_r = 0.0
for (_,_,r) in t_s:
    min_r = min(min_r,float(r))
    max_r = max(max_r,float(r))
    sum_r += float(r)
print("With Resampling: SUM:{} MIN:{} MAX:{}".format(sum_r,min_r,max_r))
for (a,b,r) in t_s:
    [x1,y1,z1] = [n1.nodes[a][i] for i in ['x','y','z']]
    [x2,y2,z2] = [n1.nodes[b][i] for i in ['x','y','z']]
    ax.plot([x1,x2],[-y1,-y2],[z1,z2],c=plt.cm.YlOrRd((float(r)-min_r)/(max_r-min_r)))
    # csv_w.writerow([x1,y1,z1,(float(r)-min_r)/(max_r-min_r)])
    # csv_2.writerow([x2,y2,z2,(float(r)-min_r)/(max_r-min_r)])
    
for (a,b) in g2.edges():
    [x1,y1,z1] = [n2.nodes[a][i] for i in ['x','y','z']]
    [x2,y2,z2] = [n2.nodes[b][i] for i in ['x','y','z']]
    ax.plot([x1,x2],[-y1,-y2],[z1,z2],c=plt.cm.cool((float(max(z1,z2))-4000)/(31000)))

fig = plt.figure()
ax = fig.gca()
fig2 = plt.figure()
ax2 = fig2.gca()
for (a,b,r) in t_s:
    [x1,y1,z1] = [n1.nodes[a][i] for i in ['x','y','z']]
    [x2,y2,z2] = [n1.nodes[b][i] for i in ['x','y','z']]
    ax.plot([x1,x2],[-y1,-y2],c=plt.cm.YlOrRd((float(r)-min_r)/(max_r-min_r)))
    ax2.plot([x1,x2],[z1,z2],c=plt.cm.YlOrRd((float(r)-min_r)/(max_r-min_r)))
    
for (a,b) in g2.edges():
    [x1,y1,z1] = [n2.nodes[a][i] for i in ['x','y','z']]
    [x2,y2,z2] = [n2.nodes[b][i] for i in ['x','y','z']]
    ax.plot([x1,x2],[-y1,-y2],c=plt.cm.cool((float(max(z1,z2))-4000)/(31000)))
    ax2.plot([x1,x2],[z1,z2],c=plt.cm.cool((float(max(z1,z2))-4000)/(31000)))
plt.show()

# t_s = catmaid.algorithms.population.synapses.skeleton_overlap_v_verbose_ids(n1,n2,1000.,10000.)
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# min_r = float(t_s[0][2])
# sum_r = 0.0
# for (_,_,r) in t_s:
    # min_r = min(min_r,float(r))
    # max_r = max(max_r,float(r))
    # sum_r += float(r)
# print("With out Resampling: SUM:{} MIN:{} MAX:{}".format(sum_r,min_r,max_r))
# for (a,b,r) in t_s:
    # [x1,y1,z1] = [n1.nodes[a][i] for i in ['x','y','z']]
    # [x2,y2,z2] = [n1.nodes[b][i] for i in ['x','y','z']]
    # ax.plot([x1,x2],[y1,y2],[z1,z2],c=plt.cm.YlOrRd((float(r)-min_r)/(max_r-min_r)))
    
# for (a,b) in g2.edges():
    # [x1,y1,z1] = [n2.nodes[a][i] for i in ['x','y','z']]
    # [x2,y2,z2] = [n2.nodes[b][i] for i in ['x','y','z']]
    # ax.plot([x1,x2],[y1,y2],[z1,z2],c='b')
# plt.show()