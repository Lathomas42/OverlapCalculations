import numpy
import catmaid
import csv
from catmaid.algorithms.population.synapses import edge_to_cylinder,cylinder_overlap

# c=catmaid.connection.Connection('http://catmaid.hms.harvard.edu','thomas.lo','asdfjkl;',9)
# src = catmaid.get_source(c)

# sk1 = 325123
# sk2 = 38321

# n1 = src.get_neuron(sk1)
# n2 = src.get_neuron(sk2)


def euclidean_dist(n1,n2):
    ax = n1.axons[n1.axons.keys()[0]]['tree'].nodes()
    den = n2.dendrites.nodes()
    sk1 = n1.skeleton['id']
    sk2 = n2.skeleton['id']
    with open('euclidian_{}_{}.csv'.format(sk1,sk2),'wb') as f_o:
        csv_writer = csv.writer(f_o)

        def dist(a_n, d_n):
            d = numpy.sqrt(sum([(n1.nodes[a_n][x]-n2.nodes[d_n][x])**2 for x in ['x','y','z']]))
            return d

        for ax_node in ax:
            d = None
            for den_node in den:
                if d is None:
                    d = dist(ax_node,den_node)
                else:
                    d = min(d,dist(ax_node,den_node))
            csv_writer.writerow([n1.nodes[ax_node]['x'], n1.nodes[ax_node]['y'], n1.nodes[ax_node]['z'], d])
        
def overlap_dist(n1,n2,resample=0.,s=1000.,sig=10000.):
    if resample != 0.:
        ax = catmaid.algorithms.morphology.resample_edges(n1,resample,labels=['axon'])
        den = catmaid.algorithms.morphology.resample_edges(n2,resample,labels=['dendrite'])
    else:
        ax = n1.axons[n1.axons.keys()[0]]['tree']
        den = n2.dendrites
    sk1 = n1.skeleton['id']
    sk2 = n2.skeleton['id']
    with open('cylinder_{}_{}.csv'.format(sk1,sk2),'wb') as f_o:
        csv_writer = csv.writer(f_o)
        for (nron,g) in ((n1,ax),(n2,den)):
            for u,v,d in g.edges_iter(data=True):
                try:
                    d['r'],d['n'],d['l'] = edge_to_cylinder(nron.skeleton['vertices'][u],nron.skeleton['vertices'][v])
                    d['valid'] = True
                except EdgeError as e:
                    logging.error("BADEDGE")
                    d['valid']=False
        total = 0.
        for _,_,a in ax.edges_iter(data=True):
            if not a['valid']:
                continue
            max_o = 0.0
            sum_o = 0.0
            for _,_,d in den.edges_iter(data=True):
                if not d['valid']:
                    continue
                o_lap = cylinder_overlap(a,d,sig=sig)
                max_o = max(o_lap,max_o)
                sum_o += o_lap 
                total += o_lap
            csv_writer.writerow([a['r'][0],a['r'][1],a['r'][2],max_o,sum_o])
    return total * 2. * s
    
def cylinders_csv(nron,resample=0.):
    if resample != 0.:
        ax = catmaid.algorithms.morphology.resample_edges(nron,resample,labels=['axon'])
        den = catmaid.algorithms.morphology.resample_edges(nron,resample,labels=['dendrite'])
    else:
        ax = nron.axons[nron.axons.keys()[0]]['tree']
        den = nron.dendrites
    sk1 = nron.skeleton['id']
    with open('cylinders_{}_ax.csv'.format(sk1),'wb') as f_ax:
        ax_writer = csv.writer(f_ax)
        for u,v,d in ax.edges_iter(data=True):
            r,n,l = edge_to_cylinder(nron.skeleton['vertices'][u],nron.skeleton['vertices'][v])
            ax_writer.writerow(numpy.concatenate((r,n,[l])))
    with open('cylinders_{}_den.csv'.format(sk1),'wb') as f_d:
        d_writer = csv.writer(f_d)
        for u,v,d in den.edges_iter(data=True):
            r,n,l = edge_to_cylinder(nron.skeleton['vertices'][u],nron.skeleton['vertices'][v])
            d_writer.writerow(numpy.concatenate((r,n,[l])))
            
def overlap_numpy(s1,s2,s=1000.,sig=10000.):
    full_ax = numpy.genfromtxt('cylinders_{}_ax.csv'.format(s1),delimiter=',')
    full_den = numpy.genfromtxt('cylinders_{}_den.csv'.format(s2),delimiter=',')
    r_ax = full_ax[:,0:3]
    n_ax = full_ax[:,3:6]
    l_ax = full_ax[:,6]
    r_den = full_den[:,0:3]
    n_den = full_den[:,3:6]
    l_den = full_den[:,6]
    tot = 0.0
    for i in numpy.arange(len(l_ax)):
        r = r_ax[i,:]
        n = n_ax[i,:]
        l = l_ax[i]
        n_d = n_den.copy()
        r_diff = r_den - r
        for j in [0,1,2]:
            n_d[:,j] = n_d[:,j]*n[j]
            r_diff[:,j] = r_diff[:,j]*r_diff[:,j]
        dots_n = numpy.sum(n_d,1)
        dots_n[dots_n>1] = 1.0
        dots_n[dots_n<-1] = -1.0
        dots_r = numpy.sum(r_diff,1)
        angs = numpy.arccos(dots_n)
        v_full = l *l_den * numpy.abs(numpy.sin(angs))*numpy.exp(
                 -(dots_r)/(4*sig**2))/((4*numpy.pi*sig**2)**1.5)
        tot += numpy.sum(v_full)
    return tot * 2. * s
    
def angle(a,d):
    dp = numpy.dot(a,d)
    if dp > 1.0:
        dp = 1.0
    if dp < -1.0:
        dp = -1.0
    v = nump.arccos(dp)
    return v