# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:29:39 2021

@author: inet
"""

import pandas as pd
import random
import networkx as nx
import re,time, os, argparse
import itertools
import numpy as np

parser = argparse.ArgumentParser(description='Moon demo')
parser.add_argument('--flowSet', help='List of flows',
                     type=str, action="store", required=True)
parser.add_argument('--topo', help='topoName',
                    type=str, action="store", required=True)
parser.add_argument('--controller', help='ID of controller',
                    type=str, action="store", required=True)

args = parser.parse_args()

name_arg= args.topo


file1 = open(args.flowSet, 'r')
Lines = file1.readlines()

flowSet=[]
for f in Lines:
    f=[int(s) for s in f.split() if s.isdigit()]
    
    flowSet.append(list(map(str,f)))
print('flowSet:',flowSet)

fdir=str(args.topo.replace(".graphml", ""))+"commandsFilesOpenTM"
if(os.path.isdir(fdir) == False):
    os.makedirs(fdir)


## Read graph from topology
Topo = str(name_arg.replace(".graphml", ""))
G= nx.read_graphml(Topo+'.graphml')

#G = nx.read_graphml('AS3967.graphml')
#nx.draw(G, with_labels=True)

# *************************************************************************

bestPaths=[]
leaderPaths=[]
#-----------------------------------------------------------------------------

##nodes=list(g.nodes)
nodes=[]
for n in G.nodes:
    nodes.append(int(n))

flowSet= []
lastNode =  nodes[-1]

lastNode =  max(nodes)
controller ='0'
#print('lastNode:',lastNode)
#controller =lastNode+1
#print(controller)
#G.add_node(controller)



#-----------------------------------------------------------------------------
aNodes=G.nodes
aEdges=G.edges
#print (aNodes)
#print (aEdges)
ed=list(G.edges(data=True))
ed.sort()
newE=[]
f11 = open('topo.txt', "w")
for e in ed:
    k=e[0]
    newE.append((int(e[0]),int(e[1])))
newE.sort()

f11.write('switches '+str(len(aNodes))+' \n')
f11.write('hosts '+str(len(aNodes))+' \n')
for i in range(len(aNodes)):
    f11.write('h'+str(i+1)+' '+ 's'+str(i+1)+' \n')
for e in newE:
    f11.write('s'+str(e[0]+1)+' '+ 's'+str(e[1]+1)+' \n')
f11.close()
#print('new---E--',newE)



#**************************portFinder**********************************
#
#**********************************************************************
Nodes=[]
infile = open('topo.txt', 'r')
firstLine = infile.readline()
#print('count:',firstLine)
count=firstLine.split(' ')[1]
#print('count:',count)
Nodes=[[] for x in range(int(count))]
for g in range(int(count)):
    fname=str(fdir)+"/s%d-commands.txt"%(int(g)+1)
    f1 = open(fname, "a")
    #ruleReg="register_write MyIngress.port_reg 0 31 \n"
    #f1.write(ruleReg)
    f1.close()
with open('topo.txt') as f:
    for line in f:
        if 'hosts' not in  line and 'switches' not in line:
            a=list(line.split(' '))[0]
            indexa=re.findall(r'\d+',a)
            #print('a',a)
            b=list(line.split(' '))[1]
            #print('b:',b)
            indexb=re.findall(r'\d+',b)
            #print('index:',indexa[0],indexb[0])
            if 'h' in a:
                Nodes[int(indexb[0])-1].append(a)
            elif 's' in a or 's' in b:
                Nodes[int(indexa[0])-1].append(b)
                Nodes[int(indexb[0])-1].append(a)

#print("****************************Nodes*************************: ",Nodes)
#*********************************************************************                
#*************************************
# NOW PARSE ELEMENT SETS TO GET THE DATA FOR THE TOPO
# GET NODE_NAME DATA
# GET LONGITUDE DATK
# GET LATITUDE DATA

for e in aEdges:
    #print "e:",aEdges[e]['LinkNote']
    #print aNodes[e[0]]['Latitude'], aNodes[e[0]]['Longitude']
    '''
    latitude_src=math.radians(float(aNodes[e[0]]['Latitude']))
    latitude_dst=math.radians(float(aNodes[e[1]]['Latitude']))
    longitude_src=math.radians(float(aNodes[e[0]]['Longitude']))
    longitude_dst=math.radians(float(aNodes[e[1]]['Longitude']))
    first_product               = math.sin(latitude_dst) * math.sin(latitude_src)
    second_product_first_part   = math.cos(latitude_dst) * math.cos(latitude_src)
    second_product_second_part  = math.cos(longitude_dst - longitude_src)

    distance = math.acos(first_product + (second_product_first_part * second_product_second_part)) * 6378.137

    # t (in ms) = ( distance in km * 1000 (for meters) ) / ( speed of light / 1000 (for ms))
    # t         = ( distance       * 1000              ) / ( 1.97 * 10**8   / 1000         )
    ''
    latency = ( distance * 1000 ) / ( 197000 )
    '''
    #print "latency:", latency
    G[e[0]][e[1]]['latency']=G[e[0]][e[1]]['latency']
    #get the numbers from BW with value like 45Mbps
    #print(aEdges[e],e[0],e[1])
    G[e[0]][e[1]]['bandwidth']=G[e[0]][e[1]]['bw']
    #G[e[0]][e[1]]['bandwidth']=map(int, re.findall(r'\d+', aEdges[e]['LinkNote'].encode('utf-8')))
    #print aNodes[e[1]['Latitude'], aNodes[e[1]['Longitude']
    # GET IDS FOR EASIER HANDLING

# *************************************************************************
# Rank the nodes based on their path to the controller
# *************************************************************************
def findNodesRank(controller):
    nodesRank=[]
    for node in G.nodes:
        if (node!= controller):
            nodes_temp_wgt = pd.DataFrame()
            path = nx.shortest_path(G, str(node), controller)
            #print("path from node: ", nodes , " to controller node: ", controller, " ", path)
            for x, y in zip(path, path[1:]):
                    bw = getPathBW(x,y,G.subgraph(path))
                    lat= getPathDelay(x,y,G.subgraph(path))
                    nodes_temp_wgt = nodes_temp_wgt.append({"node": nodes, "latency": lat, "bw": bw},ignore_index=True)

            bw_max = nodes_temp_wgt.bw.max()
            bw_min = nodes_temp_wgt.bw.min()
            bw_sum = nodes_temp_wgt.bw.sum()

            lat_min = nodes_temp_wgt.latency.min()
            lat_max = nodes_temp_wgt.latency.max()
            lat_sum = nodes_temp_wgt.latency.sum()
            #print(nodes_temp_wgt)


            if ((lat_max - lat_min) == 0 and (bw_max - bw_min) == 0):
                O = 0
                nodesRank.append(O)

            elif ((lat_max - lat_min) == 0 and (bw_max - bw_min) != 0):
                O = ((bw_sum - bw_min) / (bw_max - bw_min))
                nodesRank.append(round(O, 2))
                
            elif ((lat_max - lat_min) != 0 and (bw_max - bw_min) == 0):
                O = ((lat_sum - lat_min) / (lat_max - lat_min))
                nodesRank.append(round(O, 2))

            else:
                try:
                    O = ((lat_sum - lat_min) / (lat_max - lat_min)) + ((bw_sum - bw_min) / (bw_max - bw_min))
                    #print ( 'o: ', O)
                    nodesRank.append(round(O, 2))
                except:
                      print("An exception occurred")

            #print ('Node: ',nodes, ' rank: ', O)
    return  nodesRank

def getPathDelay(firstNode, EndNode, p_graph):
    path = nx.shortest_path(p_graph, str(firstNode), str(EndNode))
    sub_graph = G.subgraph(path)
    sum = 0
    for edge in sub_graph.edges(data=True):
        lat= edge[2]['latency']
        sum+=lat
    return (sum)

def getPathBW(firstNode, EndNode, p_graph):
    path = nx.shortest_path(p_graph, str(firstNode), str(EndNode))
    sub_graph = G.subgraph(path)
    lst =[]
    for edge in sub_graph.edges(data=True):
        lat= edge[2]['bw']
        lst.append(lat)
        #sum+=lat
    return (min(lst))
def findHop(leader, controller ,g):
        l= leader
        c= controller
        path = nx.shortest_path(g, l, c)
        hop=(len(path)-1)
        return hop
def getPath(firstNode, EndNode, p_graph):
    path = nx.shortest_path(p_graph, str(firstNode), str(EndNode))
    return (path)

# *************************************************************************
# We print all the flows using this function
# *************************************************************************
def printFinalPath():
    print(" ********************************************** ")
    print(" Final ",len(bestPaths)," paths are:")
    for i in bestPaths:
        print (bestPaths.index(i),':',i)




# ******************************************************************************
# This function updates generates rules for P4 switches
# flow bandiwth request from the available bandwidth
# ******************************************************************************
def GenerateRule():

    for i in bestPaths:
        #print ('Rule generation for path ',bestPaths.index(i),':',i)
        p=i
        src=p[0]
        dst=p[-1]
        writeHostRules(dst)
        writeHostRules(src)
        for j in range(0,len(p),1):
            if j<len(p)-1:
                neighborIndex(p[j],p[j+1],dst,src,bestPaths.index(i))
                #writeRegisterRules(p[j])
        #create the oppoiste direction rules
        reverseP = p[::-1]

        for k in range(0,len(reverseP),1):
           if k<len(reverseP)-1:
                neighborIndex(reverseP[k],reverseP[k+1],src,dst,bestPaths.index(i)+len(bestPaths))

    for i in leaderPaths:
        #print ('Rule generation for path ',bestBackupPaths.index(i),':',i)
        if len(i)>1:
            p=i
            src=p[0]
            dst=p[-1]
            nextNode=p[1]
            writeLeaderRules(src,nextNode)
            for j in range(0,len(p),1):
               if j<len(p)-1:
                    neighborIndexLeaderPath(p[j],p[j+1],dst,controller,leaderPaths.index(i))



def checkfile(fname,rule):
    flag=False
    with open(fname) as f:
        #line=f.read()
        for line in f:
            if rule in line:
                flag=True
                return flag
    return flag

def writeHostRules(dst):
    fname=str(fdir)+"/s%d-commands.txt"%(int(dst)+1)
    f1 = open(fname, "a")
    rule1="table_add tbl_setFlowID set_flowID 10.0.%s.%s => 0  \n"%(int(dst)+1 ,int(dst)+1)
    rule2="table_add ipv4_lpm ipv4_forward 0 => 00:00:00:00:%02x:%02x 1  \n"%( int(dst)+1 ,int(dst)+1)
    if not checkfile(fname,rule1):
        f1.write(rule1)
    if not checkfile(fname,rule2):
        f1.write(rule2)
    f1.close()

def writeLeaderRules(src,nextNode):
    fname=str(fdir)+"/s%d-commands.txt"%(int(src)+1)
    eport=egressPort(src,nextNode)
    f1 = open(fname, "a")
    ruleSet=[]
    rule1 = "table_set_default ipv4_lpm drop\n"
    rule2 = "mirroring_add 11 %s\n" %(str(int(eport)+1))
    rule3 = "register_write bytesRemaining 0 0\n"
    rule4 = "register_write index 0 0\n"
    rule5 = "register_write MyEgress.sink_reg 0 167772417\n"
    rule6 = "register_write MyEgress.pkt_thd_reg 0 800\n"
    rule7="table_add MyEgress.generate_clone MyEgress.do_clone_e2e 0 \n"
    ruleSet.append(rule1)
    ruleSet.append(rule2)
    ruleSet.append(rule3)
    ruleSet.append(rule4)
    ruleSet.append(rule5)
    ruleSet.append(rule6)
    ruleSet.append(rule7)
    for rule in ruleSet:
        if not checkfile(fname,rule):
            f1.write(rule)

def writeRegisterRules(h):
    fname=str(fdir)+"/s%d-commands.txt"%(int(h)+1)
    f1 = open(fname, "a")
    ruleReg="register_write MyIngress.port_reg 0 31 \n"
    if not checkfile(fname,ruleReg):
        f1.write(ruleReg)
    f1.close()

def writeControllerRule(h):
    fname=str(fdir)+"/s%d-commands.txt"%(int(h)+1)
    f1 = open(fname, "a")
    rule="table_add tbl_toController ipv4_forward_toController 10.0.%s.%s => 00:00:00:00:%02x:%02x 1 \n"%(int(h)+1 ,int(h)+1,int(h)+1 ,int(h)+1)
    if not checkfile(fname,rule):
        f1.write(rule)
    f1.close()
    
def neighborIndex(a,b,dst,src,p_i):
    fname=str(fdir)+"/s%d-commands.txt"%(int(a)+1)
    f1 = open(fname, "a")
    eport=egressPort(a,b)
    rule1="table_add tbl_setFlowID set_flowID 10.0.%s.%s => %s  \n"%(int(dst)+1 ,int(dst)+1,(int(p_i)+1))
    rule2="table_add ipv4_lpm ipv4_forward %s => 00:00:00:%02x:%02x:00 %s \n"%((int(p_i)+1),int(dst)+1 ,int(dst)+1,str(int(eport)+1))
    if not checkfile(fname,rule1):
        f1.write(rule1)
    if not checkfile(fname,rule2):
        f1.write(rule2)
    f1.close()
def egressPort(src,dst):
    #print(Nodes[int(src)])
    egress=Nodes[int(src)].index('s'+str(int(dst)+1))
    #print('------EGRESS---',egress)
    return egress

def neighborIndexLeaderPath(a,b,dst,src,p_i):
    fname=str(fdir)+"/s%d-commands.txt"%(int(a)+1)
    f1 = open(fname, "a")
    eport=egressPort(a,b)
    rule="table_add tbl_toController ipv4_forward_toController 10.0.%s.%s => 00:00:00:%02x:%02x:00 %s \n"%(int(dst)+1 ,int(dst)+1,int(dst)+1 ,int(dst)+1,str(int(eport)+1))
    if not checkfile(fname,rule):
        f1.write(rule)
    f1.close() 


leaderList = []
hopsList = []
delayList_leaderToController = []
loopDelay = []


#print(flowSet)
#G.add_node(str(controller))
#G.add_edge(str(controller),  str(lastNode), latency=22, bw=9)   
start_leader=time.time()
#Find rank of each node to use them whenever they needed in the algorithm
nodesRank=(findNodesRank(controller))
end_leader=time.time()
leader_time=end_leader-start_leader


# We add the controller to topo.txt and also add the link 
# between the controller and the last node
#f11 = open(str(fdir) +'/topo.txt', "a")
#f11.write('s'+str(lastNode)+' '+ 's'+str(int(args.controller)+1)+' \n' )  
#f11.close()


#start = time.time()
file1 = open('flowSet.txt', 'r')
Lines = file1.readlines()

flowSet=[]
for f in Lines:
    f=[int(s) for s in f.split() if s.isdigit()] 
    flowSet.append(list(map(str,f)))
    
 
start = time.time()
for k in flowSet:

    bestPaths.append(k)
    leader=k[-1]
    
    leadcont=getPath(leader, controller, G)
    leadcont_subgraph = G.subgraph(leadcont)
    leaderPathToController = list(map(int, leadcont))
    #print('leader:',leader,leaderPathToController)
    leaderPaths.append(leaderPathToController)
    hops= findHop((leader), controller ,G)
    delay= getPathDelay((leader), controller, G)
    delayList_leaderToController.append(round(delay,2))
    leaderList.append(leader)
    hopsList.append(hops)
    
end = time.time()    

writeControllerRule(controller)
printFinalPath()
GenerateRule()

exeTime = end - start

loopTime = sum (loopDelay)
#print ('loopTime: ', loopTime)
print ('OpenTM_leaderList: ', leaderList)
print ('OpenTM_hopsList: ', (hopsList))
print ('OpenTM_delayList: ', (delayList_leaderToController))
print ('OpenTM_avg_delay: ', np.mean(delayList_leaderToController))
print ('OpenTM_avg_hops: ', np.mean(hopsList))
print ('OpenTM_exeTime: ', exeTime+leader_time )

