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
	for line in open('location.txt','r'):
		time.sleep(0.1)
		# 1,121.7817407,25.04357,台北市中正區八德路一段82巷9弄19號
		ary = line.strip().split(',')
		id_ = ary[0]
		address = ary[3]
		try:
			r = api.reqAddress(address)
			if r.json()['status'] == 'OVER_QUERY_LIMIT':
				print 'Fail to update anything, terminate.'
				sys.exit(0)
			if r.json()['status'] != 'OK':
				raise FooException(line)
			location = r.json()['results'][0]['geometry']['location']
			newLocation = "%s,%f,%f,%s" %(id_,location['lng'], location['lat'],address)
			print newLocation
			newLocations.append(newLocations)
			# f.write(newLocation+'\n')
		except FooException as e:
			print 'error'
			with open('errorLocatioin','w') as f:
				f.write(e.error+'\n')
	
	with open('newLocation.pickle', 'w') as f:
            pickle.dump(newLocations, f)			