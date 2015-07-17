import networkx as nx



def trace_graph(g,node=None,master_list=None,sub_list = None):
    if node is None:
        node = get_root(g)
    if master_list is None:
        master_list = []
    if sub_list is None:
        sub_list = []
    next = g.neighbors(node)
    sub_list.append(node)
    if(len(next)==1):
        trace_graph(g,next[0],master_list,sub_list)
    elif(len(next)==0):
        master_list.append(sub_list)
    else:
        master_list.append(sub_list)
        for n in next:
            trace_graph(g,n,master_list,[node])
    return master_list
    
def get_root(g):
    for (n,d) in g.in_degree_iter():
        if d == 0:
            return n
            
            
def trace_graph_2(g,node=None,master_list=None,sub_list=None):
    if node is None:
        node = get_root(g)
    if master_list is None:
        master_list = []
    if sub_list is None:
        sub_list = []
    next = g.neighbors(node)
    sub_list.append(node)
    while len(next)==1:
        node = next[0]
        next = g.neighbors(node)
        sub_list.append(node)
    if len(next) == 0:
        master_list.append(sub_list)
    elif len(next) > 1:
        master_list.append(sub_list)
        for n in next:
            trace_graph_2(g,n,master_list,[node])
    return master_list
        
        