#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import cPickle as pickle
import sys

class FooException(Exception):
    def __init__(self, error):
        self.error = error

class ApiObject(object):
    """docstring for ApiObject"""
    def __init__(self, arg=None):
        super(ApiObject, self).__init__()
        self.arg = arg
    def linkToDataBase(self):
        pass
    def reqAddress(self,address=None):
        if not address:
            return
        r = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true_or_false&language=zh-TW'%address)
        return r



if __name__ == '__main__':
    api = ApiObject()

    newLocations = list()
    errorLocations = list()
    offset = int(sys.argv[1])
    j=0
    for line in open('location.txt','r'):
        j+=1
        # 1,121.7817407,25.04357,台北市中正區八德路一段82巷9弄19號
        ary = line.strip().split(',')
        id_ = ary[0]
        address = ary[3]
        if int(id_) <= offset:
            print 'skip id: ' + id_
            continue
        try:
            time.sleep(0.1)
            r = api.reqAddress(address)
            if r.json()['status'] == 'OVER_QUERY_LIMIT':
                print 'OVER_QUERY_LIMIT => program terminate.'
                break
            if r.json()['status'] != 'OK':
            	errorLocations.append(id_)
                raise FooException(line)
            location = r.json()['results'][0]['geometry']['location']
            newLocation = "%s,%f,%f,%s" %(id_,location['lng'], location['lat'],address)
            print newLocation
            newLocations.append(newLocation)
            if j % 500 == 0:
                with open('newLocation.pickle', 'w') as f:
                    pickle.dump(newLocations, f)
                with open('errorLocatioin.pickle','w') as f:
	                pickle.dump(errorLocations, f)
            # f.write(newLocation+'\n')
        except FooException as e:
            print 'error'
            
    with open('newLocation.pickle', 'w') as f:
            pickle.dump(newLocations, f)
    with open('errorLocatioin.pickle','w') as f:
            pickle.dump(errorLocations, f)