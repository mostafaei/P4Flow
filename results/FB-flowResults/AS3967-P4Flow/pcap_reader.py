import dpkt
import sys
import socket
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import time, datetime
from scapy.all import *
fname='h1-flow.pcap'


def printable_timestamp(ts, resol):
    ts_sec = ts // resol
    ts_subsec = ts % resol
    ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
    return '{}.{}'.format(ts_sec_str, ts_subsec)

with open(fname) as f:
    pcap = dpkt.pcap.Reader(f)
    i=0
    packets = rdpcap(fname)
    #for (pkt_data, pkt_metadata,) in RawPcapReader(fname):
    for ts, buf in pcap:
        #eth = dpkt.ethernet.Ethernet(buf)
        #ip = eth.data
        #udp = ip.data
        print('p:',i,packets[-1].time,ts,packets[-1].time-packets[-2].time )
        print ('Timestamp-1: ', str(datetime.datetime.utcfromtimestamp(packets[-1].time)))
        print ('Timestamp-2: ', str(datetime.datetime.utcfromtimestamp(packets[-2].time)))
        #first_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
        #first_pkt_timestamp_resolution = pkt_metadata.tsresol
        #print('First packet in connection: Packet #{} {}'.format(first_pkt_ordinal,  printable_timestamp(first_pkt_timestamp,first_pkt_timestamp_resolution)))
        i+=1
