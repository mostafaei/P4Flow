# Import the libraries
import matplotlib
from matplotlib import colors as mcolors
import matplotlib as mpl
import os, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import glob
#from itertools import izip
from utils import *
os.chdir(".")

#from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,mark_inset)

import matplotlib.font_manager
matplotlib.font_manager._rebuild()

matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
mpl.rcParams['font.family'] = ['serif']
mpl.rcParams['font.serif'] = ['Times New Roman']

def avgFCT(template):
    tempList=[]
    stdList=[]
    myl=sorted(glob.glob(template))
    #print("len:", len(myl))
    for x in myl:
        #print ("%s  " % (x))
        with open(x, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "flows/requests (0, 100KB) average completion time: " in line:
                    #print('line:',line)
                    x= re.findall(r'\d+',line)
		    #print(x)
                    tempList.append(float(x[3]))
    #print sorted(tempList)
    return np.mean(tempList)

def FCT99(template):
    tempList=[]
    stdList=[]
    myl=sorted(glob.glob(template))
    #print("len:", len(myl))
    for x in myl:
        #print ("%s  " % (x))
        with open(x, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "flows/requests (0, 100KB) 99th percentile completion time:" in line: 
                    x= re.findall(r'\d+',line)
                    tempList.append(float(x[4]))
    #print sorted(tempList)
    return np.mean(tempList)
def avgFCTmidSizeFlows(template):
    tempList=[]
    stdList=[]
    myl=sorted(glob.glob(template))
    #print("len:", len(myl))
    for x in myl:
        #print ("%s  " % (x))
        with open(x, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "flows/requests [100KB, 10MB) average completion time:" in line: 
                    x= re.findall(r'\d+',line)
                    tempList.append(float(x[3]))
    #print sorted(tempList)
    return np.mean(tempList)
def avgFCTLargeFlows(template):
    tempList=[]
    stdList=[]
    myl=sorted(glob.glob(template))
    #print("len:", len(myl))
    for x in myl:
        #print ("%s  " % (x))
        with open(x, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "flows/requests [10MB, ) average completion time:" in line: 
                    x= re.findall(r'\d+',line)
                    tempList.append(float(x[2]))
    #print sorted(tempList)
    return np.mean(tempList)
def Goodput(template):
    tempList=[]
    stdList=[]
    myl=sorted(glob.glob(template))
    #print("len:", len(myl))
    for x in myl:
        #print ("%s  " % (x))
        with open(x, 'r') as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if "flows/requests overall average goodput:" in line: 
                    x= re.findall(r'\d+',line)
                    tempList.append(float(x[1]))
    #print sorted(tempList)
    return np.sum(tempList)/(2*10)    


OpenTM_avgFCT_FB=[]
OpenTM_FCT99_FB=[]
OpenTM_avgFCTMidSize_FB=[]
OpenTM_Goodput_FB=[]
OpenTM_avgFCTLarge_FB=[]
OpenTM_Goodput_FB=[]


P4Flow_avgFCT_FB=[]
P4Flow_FCT99_FB=[]
P4Flow_avgFCTMidSize_FB=[]
P4Flow_Goodput_FB=[]
P4Flow_avgFCTLarge_FB=[]



smallColor='black'

FlowCover_avgFCT_FB =[]
FlowCover_FCT99_FB =[]
FlowCover_avgFCTMidSize_FB =[]
FlowCover_avgFCTLarge_FB =[]
FlowCover_Goodput_FB =[]



F10=[]
for i in range(1,7,1):
    OpenTM_avgFCT_FB.append(avgFCT('FB-flowResults/AS3967-OpenTM/results/h*-L%d-Run*.txt'%(i))/1000000)
    OpenTM_FCT99_FB.append(FCT99('FB-flowResults/AS3967-OpenTM/results/h*-L%d-Run*.txt'%(i))/1000000)
    OpenTM_avgFCTMidSize_FB.append(avgFCTmidSizeFlows('FB-flowResults/AS3967-OpenTM/results/h*-L%d-Run*.txt'%(i))/1000000)
    OpenTM_avgFCTLarge_FB.append(avgFCTLargeFlows('FB-flowResults/AS3967-OpenTM/results/h*-L%d-Run*.txt'%(i))/1000000)
    P4Flow_avgFCT_FB.append(avgFCT('FB-flowResults/AS3967-P4Flow/results/h*-L%d-Run*.txt'%(i))/1000000)
    P4Flow_FCT99_FB.append(FCT99('FB-flowResults/AS3967-P4Flow/results/h*-L%d-Run*.txt'%(i))/1000000)
    P4Flow_avgFCTMidSize_FB.append(avgFCTmidSizeFlows('FB-flowResults/AS3967-P4Flow/results/h*-L%d-Run*.txt'%(i))/1000000)
    P4Flow_avgFCTLarge_FB.append(avgFCTLargeFlows('FB-flowResults/AS3967-P4Flow/results/h*-L%d-Run*.txt'%(i))/1000000)
    P4Flow_Goodput_FB.append(Goodput('FB-flowResults/AS3967-P4Flow/results/h*-L%d-Run*.txt'%(i)))

    FlowCover_avgFCT_FB.append(avgFCT('FB-flowResults/AS3967-FlowCover/results/h*-L%d-Run*.txt'%(i))/1000000)
    FlowCover_FCT99_FB.append(FCT99('FB-flowResults/AS3967-FlowCover/results/h*-L%d-Run*.txt'%(i))/1000000)
    FlowCover_avgFCTMidSize_FB.append(avgFCTmidSizeFlows('FB-flowResults/AS3967-FlowCover/results/h*-L%d-Run*.txt'%(i))/1000000)
    FlowCover_avgFCTLarge_FB.append(avgFCTLargeFlows('FB-flowResults/AS3967-FlowCover/results/h*-L%d-Run*.txt'%(i))/1000000)
    FlowCover_Goodput_FB.append(Goodput('FB-flowResults/AS3967-FlowCover/results/h*-L%d-Run*.txt'%(i)))


	
	#F10.append(percentileLatency('F10/h*-F%d*'%(i)))
                    

for i in range(len(P4Flow_avgFCT_FB)):
	print('P4Flow over OpenTM- Small FCT:',OpenTM_avgFCT_FB[i]/P4Flow_avgFCT_FB[i])
for i in range(len(P4Flow_avgFCT_FB)):
	print('P4Flow over OpenTM- Small 99FCT:',OpenTM_FCT99_FB[i]/P4Flow_FCT99_FB[i])

for i in range(len(P4Flow_avgFCT_FB)):
	print('P4Flow over FlowCover- Small FCT:',FlowCover_avgFCT_FB[i]/P4Flow_avgFCT_FB[i])
for i in range(len(P4Flow_avgFCT_FB)):
	print('P4Flow over FlowCover- Small 99FCT:',FlowCover_FCT99_FB[i]/P4Flow_FCT99_FB[i])	

#******************************** avgFCT small*************************************
set_paper_rcs_Erdos()
fig,ax = plt.subplots(nrows=1, ncols=1)

ax.plot(sorted(P4Flow_avgFCT_FB),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(FlowCover_avgFCT_FB),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(OpenTM_avgFCT_FB),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)





ax.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
legend =plt.legend(bbox_to_anchor=(0.95, 1.05),loc="best",numpoints=2, frameon=True, ncol=3, columnspacing=0.8, handletextpad=0.2)
ax.title.set_text('Flow size (0, 100KB)')
ytic=[0.35,0.40,0.45,0.50,0.55]
ax.set_ylim(0.35,.55)
ax.set_yticks(ytic)
ax.set_yticklabels([str(i) for i in ytic])

for ax in fig.get_axes():
    ax.set_xticks(range(0,6))
    ax.set_xticklabels([str(i) for i in range(10,70,10)])
    ax.set_xlabel('Load (\%)')
    ax.set_ylabel('Average FCT (s)')
    

fig.tight_layout() 
name='FaceBook-avgFCT'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#******************************** 99FCT small*************************************

set_paper_rcs_Erdos()
fig,ax = plt.subplots(nrows=1, ncols=1)
set_paper_rcs_Erdos()
ax.plot(sorted(P4Flow_FCT99_FB),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(FlowCover_FCT99_FB),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(OpenTM_FCT99_FB),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)



ax.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
legend =plt.legend(bbox_to_anchor=(0.95, 1.05),loc="best",numpoints=2, frameon=True, ncol=3, columnspacing=0.8, handletextpad=0.2)

ytic=[2.5,3.0,3.5,4.0,4.5]
ax.set_ylim(2.5,4.5)
ax.set_yticks(ytic)
ax.set_yticklabels([str(i) for i in ytic])
'''
ax.set_yscale('log')
ax.set_ylim(0.1,int(max(FlowCover_FCT99_FB)))
'''
ax.title.set_text('Flow size (0, 100KB)')
for ax in fig.get_axes():
    ax.set_xticks(range(0,6))
    ax.set_xticklabels([str(i) for i in range(10,70,10)])
    ax.set_xlabel('Load (\%)')
    ax.set_ylabel('99-percentile FCT (s)')    

fig.tight_layout() 
name='FaceBook-FCT99'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#**************************MidSize********************************************

fig,ax = plt.subplots(nrows=1, ncols=1)
ax.plot(sorted(P4Flow_avgFCTMidSize_FB),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(FlowCover_avgFCTMidSize_FB),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(OpenTM_avgFCTMidSize_FB),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)

ax.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
ax.title.set_text('Flow size [100KB, 10MB)')
legend =plt.legend(loc="best",numpoints=2, frameon=False, ncol=1, columnspacing=0.8, handletextpad=0.2)
'''
ax.set_ylim(0,700)
ax.set_yticks(range(0,800,100))
ax.set_yticklabels([str(i) for i in range(0,800,100)], fontsize=11)

ax.set_yscale('log')
ax.set_ylim(100,int(max(FlowCover_avgFCTMidSize_FB)))
'''
for ax in fig.get_axes():
    ax.set_xticks(range(0,6))
    ax.set_xticklabels([str(i) for i in range(10,70,10)])
    ax.set_xlabel('Load (\%)')
    ax.set_ylabel('Average FCT (s)')
       

fig.tight_layout() 
name='FaceBook-avgFCTMidSize'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#**************************Large********************************************

fig,ax = plt.subplots(nrows=1, ncols=1)
ax.plot(sorted(FlowCover_avgFCTLarge_FB),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(P4Flow_avgFCTLarge_FB),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot(sorted(OpenTM_avgFCTLarge_FB),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.title.set_text('Flow size [10MB, )')
legend =plt.legend(loc="best",numpoints=2, frameon=False, ncol=1, columnspacing=0.8, handletextpad=0.2)

'''
ax.set_ylim(0,700)
ax.set_yticks(range(0,800,100))
ax.set_yticklabels([str(i) for i in range(0,800,100)], fontsize=11)

ax.set_yscale('log')
ax.set_ylim(1000,int(max(FlowCover_avgFCTLarge_FB)))
'''
for ax in fig.get_axes():
    ax.set_xticks(range(0,6))
    ax.set_xticklabels([str(i) for i in range(10,70,10)])
    ax.set_xlabel('Load (\%)')
    ax.set_ylabel('Average FCT (s)')
       
ax.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
fig.tight_layout() 
name='FaceBook-avgFCTLarge'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()
#*******************************************************************************

fig,ax = plt.subplots(nrows=1, ncols=1)
ax.plot((P4Flow_Goodput_FB),label='P4Flow' ,color=smallColor,linestyle='-', mfc='tab:red',marker='d', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot((FlowCover_Goodput_FB),label='FlowCover' ,color=smallColor,linestyle='-', mfc='tab:blue',marker='s', markersize=4,lw=1, mec=smallColor,  mew=0.65)
ax.plot((OpenTM_Goodput_FB),label='OpenTM' ,color=smallColor,linestyle='-', mfc='tab:orange',marker='o', markersize=4,lw=1, mec=smallColor,  mew=0.65)


legend =plt.legend(loc="best",numpoints=2, frameon=False, ncol=1, columnspacing=0.8, handletextpad=0.2)
'''
ax.set_ylim(0,120)
ax.set_yticks(range(0,140,20))
ax.set_yticklabels([str(i) for i in range(0,140,20)], fontsize=11)
'''

for ax in fig.get_axes():
    ax.set_xticks(range(0,6))
    ax.set_xticklabels([str(i) for i in range(10,70,10)])
    ax.set_xlabel('Load (\%)')
    ax.set_ylabel('\\textbf{Goodput (Mbps)}' )
ax.grid(color='black', ls = '--',dashes=(5, 15), lw = 0.2,alpha=1)
fig.tight_layout() 
name='FaceBook-Goodput'
plt.savefig('%s.pdf'%name,format="pdf", bbox_inches='tight', pad_inches=0.05)
plt.close()


