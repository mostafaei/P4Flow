# Copyright (c) 2015, Malte Schwarzkopf
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of qjump-nsdi15-plotting nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from matplotlib import use, rc
use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# plot saving utility function
def writeout(filename_base, tight=True):
  for fmt in ['pdf']:
    if tight:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt, bbox_inches='tight')
    else:
      plt.savefig("%s.%s" % (filename_base, fmt), format=fmt)

def set_leg_fontsize(size):
  rc('legend', fontsize=size)

def set_paper_rcs():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Helvetica'],'size':11})
  rc('text', usetex=True)
  rc('legend', fontsize=10)
  rc('figure', figsize=(3.33,2.22))
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)

def set_rcs():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Times'],'size':14})
  rc('text', usetex=True)
  rc('legend', fontsize=12)
  rc('figure', figsize=(7,5))
  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)
def set_rcs2():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Times'],'size':12})
  rc('text', usetex=True)
  rc('legend', fontsize=7)
  rc('figure', figsize=(7.92,2.02))
  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)
def set_paper_rcs_habib():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Helvetica'],'size':12})
  rc('text', usetex=True)
  rc('legend', fontsize=11)
  rc('figure', figsize=(7.92,2.02))
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)
def set_paper_rcs_habib2():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Helvetica'],'size':11})
  rc('text', usetex=True)
  rc('legend', fontsize=7)
  rc('figure', figsize=(2.93,1.93))
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)
def set_paper_rcs_Erdos():
  rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],
               'serif':['Helvetica'],'size':11})
  rc('text', usetex=True)
  rc('legend', fontsize=7)
  rc('figure', figsize=(3.33,2.22))
#  rc('figure.subplot', left=0.10, top=0.90, bottom=0.12, right=0.95)
  rc('axes', linewidth=0.5)
  rc('lines', linewidth=0.5)
  
def append_or_create(d, i, e):
  if not i in d:
    d[i] = [e]
  else:
    d[i].append(e)

def add_or_create(d, i, e):
  if not i in d:
    d[i] = e
  else:
    d[i] = d[i] + e


# event log constants
RESOURCE_UTILIZATION_SAMPLE = 0
TX_SUCCEEDED = 1
TX_FAILED = 2
COLLECTION_ENDING = 3
VMS_CHANGED_STATE = 4
SCHEDULING_OUTCOME = 5
COLLECTION_SUBMITTED = 6
SCHEDULING_TIME = 7
ZOMBIE_COLLECTION_DROPPED = 8
OVERLAP_COLLECTION_DROPPED = 9
COLLECTION_TRUNCATED = 10
CELL_STATE_SETUP = 11
END_ONLY_ENDS = 12

ARRIVAL_SAMPLE = 100
LEAVING_SAMPLE = 101
RES_LIMIT_SAMPLE = 102
ACTIVE_SAMPLE = 103
COLLECTION_ARRIVING_EVENT = 104
COLLECTION_LEAVING_EVENT = 105

MAPREDUCE_PREDICTION = 200
MAPREDUCE_ORIGINAL_RUNTIME = 201
MAPREDUCE_RESOURCE_ADJUSTMENT = 202
MAPREDUCE_BASE_RUNTIME = 203

paper_figsize_small = (1.1, 1.1)
paper_figsize_small_square = (1.5, 1.5)
paper_figsize_medium = (2, 1.33)
paper_figsize_medium_square = (2, 2)
#paper_figsize_medium = (1.66, 1.1)
paper_figsize_large = (3.33, 2.22)
paper_figsize_bigsim3 = (2.4, 1.7)

#8e053b red
#496ee2 blue
#ef9708 orange
paper_colors = ['#496ee2', '#8e053b', 'g', '#ef9708', '0', '#eeefff', '0.5', 'c', '0.7']

# -----------------------------------

def think_time_fn(x, y, s):
  return x + y * s

# -----------------------------------

def get_mad(median, data):
  devs = [abs(x - median) for x in data]
  mad = np.median(devs)
  return mad

# -----------------------------------
