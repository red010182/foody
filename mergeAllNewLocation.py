#!/usr/bin/python

from __future__ import with_statement
import cPickle as pickle
from collections import OrderedDict
from collections import Counter

def mergeAllNewLocation():
    dirs = ['0','3500','6000','8500','11000','13500','16000','18500','21000','23500','26000','28500','31000']
    newLocations = []
    for folder in dirs:
        with open('correct_location/'+folder+'/newLocation.pickle', 'r') as f:
            for line in pickle.load(f):
                newLocations.append(line) 
    print len(newLocations)
    with open('newLocations.pickle', 'w') as f:    
        pickle.dump(newLocations,f)

if __name__ == '__main__':
    ids = []
    longitudes = []
    latidues = []
    addresses= []
    with open('newLocations.pickle', 'r') as f:
        lines = pickle.load(f)
        # del lines[-1]
    
    for line in lines:
        print line
        a,b,c,d = line.split(',')
        ids.append(a)
        longitudes.append(b)
        latidues.append(c)
        addresses.append(d)

    print len([x for x, y in Counter(ids).items() if y > 1])
    # uids = list(OrderedDict.fromkeys(ids))
    # print len(uids)