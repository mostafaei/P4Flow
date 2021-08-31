# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 11:46:55 2021

@author: inet
"""

#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep
import os, time, re
import subprocess


_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 9090
_SERVER_BASE_PORT = 5001

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral_exe', help='Path to behavioral executable',
                    type=str, action="store", required=False)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=False)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=False)
parser.add_argument('--size', help='UDP packet size',
                    type=str, action="store", required=False)

args = parser.parse_args()

args.json="P4Flow.json"
args.behavioral_exe="simple_switch"
args.cli="simple_switch_CLI"

class MyTopo(Topo):
    def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, **opts):
        # Initialize topology and default options
        print('opts',opts)
        Topo.__init__(self, **opts)

        for i in range(nb_switches):
            #G.add_node('s%d' % (i + 1))
           	switch = self.addSwitch('s%d' % (i + 1),
                                    sw_path = sw_path,
                                    json_path = args.json,
                                    thrift_port = _THRIFT_BASE_PORT + i,
                                    log_console = False,
                                    pcap_dump = False,
                                    device_id = i)

        
        for h in range(nb_hosts):
            #host_ip = "10.0.%d.%d" % (nb_switches, h+1)
            host_ip = "10.0.%d.%d/24" % (h+1, h+1)
            print('host_ip',host_ip)
            #host_mac = '00:00:00:00:%02x:%02x' % (nb_switches, h+1)
            host_mac = '00:00:00:00:%02x:%02x' % (h+1, h+1)
            print('host_mac',host_mac)
            host = self.addHost('h%d' % (h + 1),ip=host_ip,mac=host_mac)

        for a, b in links:
            #delay_key = ''.join([host_name, sw])
            #delay = latencies[delay_key] if delay_key in latencies else '0ms'
            #bw = bws[delay_key] if delay_key in bws else None
            self.addLink(a, b, bw=10)
            

def read_topo():
    nb_hosts = 0
    nb_switches = 0
    links = []
    with open("topo.txt", "r") as f:
        line = f.readline()[:-1]
        w, nb_switches = line.split()
        assert(w == "switches")
        line = f.readline()[:-1]
        w, nb_hosts = line.split()
        assert(w == "hosts")
        for line in f:
            if not f: break
            a, b = line.split()
            links.append( (a, b) )
    return int(nb_hosts), int(nb_switches), links
    

def main(b,t,l,Run):
    nb_hosts, nb_switches, links = read_topo()

    topo = MyTopo(args.behavioral_exe,
                  args.json,
                  nb_hosts, nb_switches, links)

    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  link = TCLink,
                  controller = None )
    net.start()

    for host_name in topo.hosts():
            h = net.get(host_name)
            h_iface = list(h.intfs.values())[0]
            link = h_iface.link

            sw_iface = link.intf1 if link.intf1 != h_iface else link.intf2
            # phony IP to lie to the host about
            host_id = int(host_name[1:])
            sw_ip = '10.0.%d.254' % host_id

            # Ensure each host's interface name is unique, or else
            # mininet cannot shutdown gracefully
            h.defaultIntf().rename('%s-eth0' % host_name)
            # static arp entries and default routes
            h.cmd('arp -i %s -s %s %s' % (h_iface.name, sw_ip, sw_iface.mac))
            h.cmd('ethtool --offload %s rx off tx off' % h_iface.name)
            h.cmd('ip route add %s dev %s' % (sw_ip, h_iface.name))
            h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
            h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
            h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
            #h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
            h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")

            h.setDefaultRoute("via %s" % sw_ip)

    sleep(1)

    for i in range(nb_switches):
        s = net.get('s%d' % (i + 1))
        print("##################################\n")
        print("Switch (s%d)" % (i + 1))
        result = s.cmd('ifconfig')
        #print	result
	#print("MAC Address: \t%s"% s.MAC())
	#print("IP Address: \t%s\n"% s.IP())
        #print("##################################")
        cmd = [args.cli, "--json", args.json,"--thrift-port", str(_THRIFT_BASE_PORT + i)]
        with open("s%d-commands.txt"%(i + 1), "r") as f:
            print(" ".join(cmd))
            try:
                output = subprocess.check_output(cmd, stdin = f)
                print(output)
            except subprocess.CalledProcessError as e:
                print(e)
                print(e.output)

    sleep(1)
    hostList=[]
    processList=[]
    file1 = open('flowSet.txt', 'r')
    Lines = file1.readlines()
    #file1 = open('portSet.txt', 'r')
    #portLists = file1.readlines()

    flowSet=[]
    for f in Lines:
        f=[int(s) for s in f.split() if s.isdigit()] 
        flowSet.append(list(map(str,f)))
    
    	
    for f in flowSet:
        dst=f[-1]
        h=net.getNodeByName('h%d'%(int(dst)+1))
        h.cmd(' TrafficGenerator/bin/server -p 5001 -d 2>&1 &')
        #h.popen(' TrafficGenerator/bin/server -p 5001 -d 2>&1 &', shell=True)
        #hostList.append(h)
        
        
    cl=1        
    for f in flowSet:
        src=f[0]
        dst=f[-1]
        h=net.getNodeByName('h%d'%(int(src)+1))
        #p=h.popen(' TrafficGenerator/bin/client -b %d -c TrafficGenerator/conf/cfg-%s-client%d.txt -n 500 -l flows%d.txt -s 123 -r TrafficGenerator/bin/result.py > results/h%d-%d-L%d-Run%d.txt'%(b,t,cl,cl,int(src)+1,int(dst)+1,l,Run), shell=True)
        p=h.popen(' TrafficGenerator/bin/client -b %d -c TrafficGenerator/conf/cfg-%s-client%d.txt -n 1000 -l flows%d.txt -s 123 '%(b,t,cl,cl), shell=True)
        processList.append(p)
        cl+=1

    print("Ready !")
    for pp in processList:
        pp.wait()
    os.system('pkill -f iperf3')
    os.system("pkill -f 'TrafficGenerator'")
    cl=1 
    for f in flowSet:
        src=f[0]
        dst=f[-1]
        os.system(' sudo python3 TrafficGenerator/bin/result.py flows%d.txt  > results/h%d-%d-%s-L%d-Run%d.txt'%(cl,int(src)+1,int(dst)+1,t,l,Run))
	cl+=1

    #CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    Traffic=['FB']
    for t in Traffic:
        for r in range(1,11):
            for b in range(1,7,1):
                main(b,t,b,r)
