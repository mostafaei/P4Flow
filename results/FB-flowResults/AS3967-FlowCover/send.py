#!/usr/bin/env python
import sys
import time, json
from probe_hdrs import *
from collections import Counter
import statistics

def main():
    N = 20 # Total number of streams obtained by experiments
    K = 40 # Number of packets in the stream
    T = 0.00006 # Time in seconds
    data = "Technical University Berlin" * 49 # Packet size is 1341 bytes.

    probe_pkt = Ether(dst='ff:ff:ff:ff:ff:ff', src=get_if_hwaddr('h10-eth0')) / \
                Probe(hop_cnt=0) / \
                ProbeFwd(egress_spec=3) / \
                ProbeFwd(egress_spec=4) / \
                ProbeFwd(egress_spec=2) / \
            data

    bandwidth = []
    stream = 1
    while stream<=N:
        try:
            print("Stream: {}, Rate: {:.2f}Mbps".format(stream, len(probe_pkt)/T*0.008*0.001))
            for i in range(K): 
                sendp(probe_pkt / str(time.time()), iface='h10-eth0', verbose=0)
               # print("Length of packet is: {} bytes".format(len(probe_pkt)))
                bandwidth.append(len(probe_pkt)/T*0.008*0.001)
                time.sleep(T)
            with open('feedback.txt', 'r') as f:
                try:
                    feedback = json.load(f) # Feedback from receiver to adjust the Rate
                    print(feedback)
                    if feedback == 'R > A':
                        T += T/4 # Tuning required for higher bandwidth links
                    elif feedback == 'R <= A':
                        T -= T/20 # Tuning required for higher bandwidth links
                except ValueError:
                    pass
            stream += 1
        except ZeroDivisionError:
            pass
        except KeyboardInterrupt:
            sys.exit()
    print("\n-------------------------------------")
    print("Available Bandwidth: {:.2f}Mbps".format(statistics.mean(set(bandwidth))))
    print("-------------------------------------")

if __name__ == '__main__':
    main()
