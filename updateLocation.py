#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import cPickle as pickle
import sys
import ConfigParser
import sqlite3
import MySQLdb
import re

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

def updateWithOffset(offset=None):
    api = ApiObject()

    newLocations = list()

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

def updateByCheckingDatabaseColumns():
    api = ApiObject()

    newLocations = list()

    db = openDB()
    cur = db.cursor()
    cur.execute('select * from delicacy where lon < 1 or lat < 1')
    records = cur.fetchall()
    for record in records:
        try:
            time.sleep(0.1)
            id_ = record[0]
            address = address = re.sub(r"\(.*\)","",record[3])
            # print address
            r = api.reqAddress(address)
            if r.json()['status'] == 'OVER_QUERY_LIMIT':
                print 'OVER_QUERY_LIMIT => program terminate.'
                raise
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
            break
    db.close()

if __name__ == '__main__':
    # updateWithOffset(offset = int(sys.argv[1]))
    updateByCheckingDatabaseColumns()
