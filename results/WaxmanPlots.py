# Import the libraries
import matplotlib


import os,  re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
#from itertools import izip
from utils import *
import matplotlib.font_manager
matplotlib.font_manager._rebuild()
filePath="Waxman/"
def avgDelay(template,name):
    tempList=0
    os.chdir(".")
    fname=filePath+template+".txt"
    with open(fname, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            cond=name+"_avg_delay:"
            if cond in line: 
                x= re.findall(r'\d+\.\d+',line)
                #print (x[0])
                tempList=round(float(x[0]),2)
            #print sorted(tempList)
    return (tempList)

def avgHops(template,name):
    tempList=0
    os.chdir(".")
    fname=filePath+template+".txt"
    with open(fname, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            cond=name+"_avg_hops:"
            if cond in line: 
                x= re.findall(r'\d+\.\d+',line)
                tempList=round(float(x[0]),2)
    return (tempList)

def avgTime(template):
    tempList=0
    os.chdir(".")
    fname=filePath+template+".txt"
    with open(fname, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            cond="exeTime:"
            if cond in line: 
                x= re.findall(r'\d+\.\d+',line)
                tempList=round(float(x[0]),2)
    return (tempList)
            

smallColor='black'
set_paper_rcs_habib2()


P4Flow_Delay=[]
FlowCover_Delay=[]
OpenTM_Delay=[]

P4Flow_Hops=[]
FlowCover_Hops=[]
OpenTM_Hops=[]

P4Flow_Time=[]
FlowCover_Time=[]
OpenTM_Time=[]

for flows in range(100,1100,100):
    P4Flow_Delay.append(avgDelay("flowMonWaxman3-P4Flow-Flows%d"%(flows),'P4Flow'))
    FlowCover_Delay.append(avgDelay("flowMonWaxman3-FlowCover-Flows%d"%(flows),'FlowCover'))
    OpenTM_Delay.append(avgDelay("flowMonWaxman3-OpenTM-Flows%d"%(flows),'OpenTM'))
    P4Flow_Hops.append(avgHops("flowMonWaxman3-P4Flow-Flows%d"%(flows),'P4Flow'))
    FlowCover_Hops.append(avgHops("flowMonWaxman3-FlowCover-Flows%d"%(flows),'FlowCover'))
    OpenTM_Hops.append(avgHops("flowMonWaxman3-OpenTM-Flows%d"%(flows),'OpenTM'))
    P4Flow_Time.append(avgTime("flowMonWaxman3-P4Flow-Flows%d"%(flows)))
    FlowCover_Time.append(avgTime("flowMonWaxman3-FlowCover-Flows%d"%(flows)))
    OpenTM_Time.append(avgTime("flowMonWaxman3-OpenTM-Flows%d"%(flows)))


#----------------------------Delay-----------------------------------------
set_paper_rcs_Erdos()
fig, axes = plt.subplots(nrows=1, ncols=1)
axes.plot( (P4Flow_Delay),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (FlowCover_Delay),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (OpenTM_Delay),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)

axes.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
plt.xlabel('Flows')
plt.ylabel('Reporting delay [ms]')
workers=range(100,1100,100)

for ax in fig.get_axes():  
    ax.set_xticks(range(0,10,1))
    ax.set_xticklabels(workers)
    ax.set_yticks(range(90,160,10))
    ax.set_ylim(90,150)
    ax.set_yticklabels([str(i) for i in range(90,160,10)])
    #ax.label_outer()

fig.tight_layout() 
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(.95, 1.125),loc="best",numpoints=1, frameon=True, ncol=3, columnspacing=0.5, handletextpad=0.1)
name='Waxman_avg_delay'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#----------------------------Time-----------------------------------------
set_paper_rcs_Erdos()
fig, axes = plt.subplots(nrows=1, ncols=1)
set_paper_rcs_Erdos()
axes.plot( (P4Flow_Time),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (FlowCover_Time),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (OpenTM_Time),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)

axes.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
plt.xlabel('Flows')
plt.ylabel('Execution time [s]')

workers=range(100,1100,100)

for ax in fig.get_axes():  
    ax.set_xticks(range(0,10,1))
    ax.set_xticklabels(workers)
    ax.set_yticks(np.arange(0,3.5,.5))
    ax.set_ylim(-.15,3.0)
    ax.set_yticklabels([str(i) for i in np.arange(0,4,.5)])
    #ax.label_outer()
plt.xticks(rotation=45)
fig.tight_layout() 
plt.legend(bbox_to_anchor=(.95, 1.15),loc="best",numpoints=1, frameon=True, ncol=3, columnspacing=0.5, handletextpad=0.1)
name='WaxmanExecTime'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#----------------------------Hops-----------------------------------------
set_paper_rcs_Erdos()
fig, axes = plt.subplots(nrows=1, ncols=1)
axes.plot( (P4Flow_Hops),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (FlowCover_Hops),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( (OpenTM_Hops),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)

axes.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
plt.xlabel('Flows')
plt.ylabel('Hops')

workers=range(100,1100,100)

for ax in fig.get_axes():  
    ax.set_xticks(range(0,10,1))
    ax.set_xticklabels(workers)
    ax.set_yticks(np.arange(2.0,5,0.5))
    ax.set_ylim(2.0,4)
    ax.set_yticklabels([str(i) for i in np.arange(2.0,5,0.5)])
    #ax.label_outer()
plt.xticks(rotation=45)
fig.tight_layout() 
plt.legend(loc="best",numpoints=1, frameon=True, ncol=1, columnspacing=0.5, handletextpad=0.1)
name='WaxmanHops'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#----------------------------Overhead-----------------------------------------

fig, axes = plt.subplots(nrows=1, ncols=1)
set_paper_rcs_habib2()
axes.plot( ([x*1438 for x in P4Flow_Hops]),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( ([x*1438 for x in FlowCover_Hops]),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
axes.plot( ([x*1438 for x in OpenTM_Hops]),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)

axes.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
plt.xlabel('Flows')
plt.ylabel('Overhead [bytes]')

workers=range(100,1100,100)

for ax in fig.get_axes():  
    ax.set_xticks(range(0,10,1))
    ax.set_xticklabels(workers)
    ax.set_yticks(range(3000,6500,500))
    ax.set_ylim(3000,6000)
    ax.set_yticklabels([str(i) for i in range(3000,6500,500)])
    #ax.label_outer()
plt.xticks(rotation=45)
fig.tight_layout() 
plt.legend(bbox_to_anchor=(0.95, 1.15),loc="best",numpoints=1, frameon=True, ncol=3, columnspacing=0.5, handletextpad=0.1)
name='WaxmanOverhead'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()