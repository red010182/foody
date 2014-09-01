#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import cPickle as pickle
import sys
import ConfigParser
import sqlite3
import MySQLdb


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

def loadSQLite(file_name=None):
    conn = sqlite3.connect(file_name)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT _id,ITEM_LONGITUDE,ITEM_LATITUDE,ITEM_ADDRESS FROM delicacy")
        records =  [record for record in cursor.fetchall()]
    return records

def openDB():
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'db_config.txt'))
    db = MySQLdb.connect(host=config.get('DB','host'),
                     user=config.get('DB','user'),
                      passwd=config.get('DB','password'),
                      db=config.get('DB','db'),
                      port=int(config.get('DB','port')))
    return db

if __name__ == '__main__':
    api = ApiObject()

    newLocations = list()
    errorLocations = list()
    offset = int(sys.argv[1])

    db = openDB()
    cur = db.cursor()

    records = loadSQLite("delicacy.db")
    i = 0
    for record in records[offset:offset+2500]:
        i += 1
        try:
            time.sleep(0.1)
            id_ = record[0]
            address = record[3]
            r = api.reqAddress(address)
            if r.json()['status'] == 'OVER_QUERY_LIMIT':
                print 'OVER_QUERY_LIMIT => program terminate.'
                break
            if r.json()['status'] != 'OK':
                errorLocations.append(id_)
                raise FooException(line)
            location = r.json()['results'][0]['geometry']['location']
            newLon = location['lng']
            newLat = location['lat']
            
            # print "%f %f " %(newLon,newLat)

            sql = "UPDATE delicacy SET lon='%f',lat='%f' WHERE id=%i" % (newLon,newLat,id_)
            print sql
            try:
                cur.execute(sql)
                if i%100 == 0:
                    db.commit()
            except:
                print 'DB error'
                db.rollback()
            
        except:
            print 'API error'


    db.close()

    # j=0
    # for line in open('location.txt','r'):
    #     j+=1
    #     # 1,121.7817407,25.04357,台北市中正區八德路一段82巷9弄19號
    #     ary = line.strip().split(',')
    #     id_ = ary[0]
    #     address = ary[3]
    #     if int(id_) <= offset:
    #         print 'skip id: ' + id_
    #         continue
    #     try:
    #         time.sleep(0.1)
    #         r = api.reqAddress(address)
    #         if r.json()['status'] == 'OVER_QUERY_LIMIT':
    #             print 'OVER_QUERY_LIMIT => program terminate.'
    #             break
    #         if r.json()['status'] != 'OK':
    #             errorLocations.append(id_)
    #             raise FooException(line)
    #         location = r.json()['results'][0]['geometry']['location']
    #         newLocation = "%s,%f,%f,%s" %(id_,location['lng'], location['lat'],address)
    #         print newLocation
    #         newLocations.append(newLocation)
    #         if j % 500 == 0:
    #             with open('newLocation.pickle', 'w') as f:
    #                 pickle.dump(newLocations, f)
    #             with open('errorLocatioin.pickle','w') as f:
       #              pickle.dump(errorLocations, f)
    #         # f.write(newLocation+'\n')
    #     except FooException as e:
    #         print 'error'
            
    # with open('newLocation.pickle', 'w') as f:
    #         pickle.dump(newLocations, f)
    # with open('errorLocatioin.pickle','w') as f:
    #         pickle.dump(errorLocations, f)