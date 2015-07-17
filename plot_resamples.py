import catmaid
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

c=catmaid.connection.Connection('http://catmaid.hms.harvard.edu','thomas.lo','asdfjkl;',9)
src = catmaid.get_source(c)

n1 = src.get_neuron(325123)
o_g = n1.dgraph
n_g = catmaid.algorithms.morphology.resample_edges(n1,400)

def plot_g(g,nron,fig_name):
    fig = plt.figure()
    plt.title(fig_name)
    ax = fig.gca(projection='3d')
    for (a,b) in g.edges():
        [x1,y1,z1] = [nron.nodes[a][i] for i in ['x','y','z']]
        [x2,y2,z2] = [nron.nodes[b][i] for i in ['x','y','z']]
        ax.plot([x1,x2],[y1,y2],[z1,z2])
plot_g(o_g,n1,'orig')
plot_g(n_g,n1,'new')
plt.show()