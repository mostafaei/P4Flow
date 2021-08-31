# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:04:41 2021

@author: inet
"""

import os
import networkx as nx
import random
from random import shuffle


# Select all 'graphml' files in current directory
#myl=sorted(glob.glob('*graphml'))
#print (myl)


#Topo= sys.argv[1]+'.graphml'
#Topo= 'AS1755.graphml'
Topo= 'AS3967.graphml'

#Topo = str(name_arg.replace(".graphml", ""))

g = nx.read_graphml(Topo)
g= nx.Graph(g)

##nodes=list(g.nodes)
nodes=[]
for n in g.nodes:
    nodes.append(int(n))

flowSet= []
#lastNode =  nodes[-1]

lastNode =  max(nodes)
controller =lastNode+1
#print(controller)
#g.add_node(controller)
#g.add_edge(controller,  (lastNode-1), latency=22, bw=9)



newFlowSet = []

# We select n random number of Flows 

for flows in range(50,60,10):
     
    
    # we call different implementations here to generate the desired output, one 
    # call per each
    os.system("python.exe P4Flow-FinalWithRunner.py  --flowSet %s --topo %s --controller %s > %s-Moon-Flows%d.txt" %( "flowSet.txt", Topo, controller, Topo.replace(".graphml", ""),flows))
    
    os.system("python.exe FlowCover-FinalWithRunner.py  --flowSet %s --topo %s --controller %s > %s-FlowCover-Flows%d.txt" %( "flowSet.txt", Topo, controller, Topo.replace(".graphml", ""),flows))
    
    os.system("python.exe OpenTM-FinalWithRunner.py  --flowSet %s --topo %s --controller %s > %s-OpenTM-Flows%d.txt" %( "flowSet.txt", Topo, controller, Topo.replace(".graphml", ""),flows))


