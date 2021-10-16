# P4Flow: Monitoring Traffic Flows with Programmable Networks

We conducted the experiments on a VM using Mininet network emulator on an `Intel Xeon CPU AMD Opteron(TM) Processor 6272 2.1GH` VM with 32 GB RAM and 16 CPU cores running `Ubuntu server 18.04`. We also use the
recommendation in [official BMv2](https://github.com/p4lang/behavioral-model/blob/main/docs/performance.md) to achieve high bandwidth throughput.
Contact for repeatability questions: [Habib Mostafaei](https://mostafaei.bitbucket.io/).
## The idea
P4Flow is a flow monitoring tool for cloud provider networks implemented on programmable data planes. Itallows the providers to monitor a set of desired flows according to their needs.


## Code organization
We organize the code into three main parts: 
 - the code evaluating the performance of P4Flow (called `code/python/`)  
 - the P4 source code of P4Flow (called `code/P4/`).
 - the code to experiments on different scenarios (called `results`)  


### Installing dependencies

We explain how one can install the missing dependencies on a vanilla Ubuntu 18.04:

```
sudo apt update
sudo apt-get --yes install git python python-pip python-numpy python-networkx
sudo python -m pip install matplotlib==2.0.2
sudo apt-get --yes install texlive-latex-extra dvipng 
```

## Run the code

You need to run the `topo.py` to collect the P4 results experiments. Please use the app runner for the Python part of P4Flow. It needs the network graph in graphml file with link latency and bandwidth and depending on the number of flows, it creates custom flows and checks the algorithms' performance. The results will be generated as txt files. The txt files can be used by the plot script to generate the plots.

```
sudo python topo.py
```

It will create the P4 network using the given topology in topo.txt file. This will use
the json representation file of P4 code to create the network and start P4 switches in 
Mininet. Then, it uses the s#-commands.txt to insert the initial forwarding rules on 
top of P4 switches. Now, the code is to run the measurements. 

## Publication
```
P4Flow: Monitoring Traffic Flows with Programmable Networks
Habib Mostafaei, Shafi Afridi
IEEE COMML 2021
```bibtex
@article{P4Flow-COMML21,
 author={H. Mostafaei and S. Afridi},
 title={{P4Flow}: Monitoring Traffic Flows with Programmable Networks},
 journal={IEEE Communications Letters},
 year={2021},
 volume={},
 number={},
 note={Impact factor: 3.436, to appear}
}
```
