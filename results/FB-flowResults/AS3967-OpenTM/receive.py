#!/usr/bin/env python

from probe_hdrs import *
import json


cache = []
more = []
less = []

def rowd():
    for i in range(1, len(cache)):
        rwd = cache[i] - cache[i-1]
        print("ROWD: {}".format(rwd)) # Relative One Way Delay
        if rwd > 0:
            more.append('R>A')
        else:
            less.append('R<=A')

def export():
    with open('feedback.txt', 'w') as f:
        if len(more) > len(less):
            json.dump('R > A', f)
        elif len(more) < len(less):
            json.dump('R <= A', f)

def custom(x):
    time_sent = str(x.payload).split('Technical University Berlin')[-1]
    owd = (time.time() - float(time_sent))*1000
    owd = float(format(owd, '.2f'))
    cache.append(owd) 
    print "OWD: {:.2f}ms".format(owd)

def main():
    N = 20 # Number of streams
    K = 40 # Number of packets in each stream
    stream = 1
    iface = 'h13-eth0'
    print "sniffing on {}".format(iface)
    try:
        while stream<=N: 
            print "---------------Stream: {}---------------".format(stream)
            sniff(iface = iface, prn = custom, count = K)
            rowd()
            export()
            del cache[:], more[:], less[:]
            stream += 1
    except ValueError:
        pass

if __name__ == '__main__':
    main()
