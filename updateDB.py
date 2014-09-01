#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import cPickle as pickle
import sys
import sqlite3
import MySQLdb
from collections import OrderedDict
from multiprocessing import Pool, Process, Queue
import ConfigParser


class Worker(Process):
    def __init__(self, queue,patchNumber):
        super(Worker, self).__init__()
        self.queue= queue
        self.patchNumber = patchNumber
    def run(self):
        print 'Worker started'
        datas = []
        for data in iter( self.queue.get, None ):
            datas.append(data)
            if len(datas) >= self.patchNumber:
                upateDatabaseWithSpawnConn(datas,self.patchNumber)
                datas=[]


def upateDatabaseWithSpawnConn(records=None,patchNumber=0):
        if records is None or len(records) is 0:
            print 'No data to update'
            return
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(r'db_config.txt'))
            db = MySQLdb.connect(host=config.get('DB','host'),
                             user=config.get('DB','user'),
                              passwd=config.get('DB','password'),
                              db=config.get('DB','db'),
                              port=config.get('DB','port'))
            cur = db.cursor()
            i=1
            for record in records:
                sql = "REPLACE INTO delicacy SET id='%i',lon='%f',lat='%f',address='%s'" % (record[0],record[1],record[2],record[3])
                print sql
                cur.execute(sql)
                
                if i % patchNumber == 0:
                    db.commit()
                i += 1
        except:
            print 'error'
            db.rollback()
        finally:
            db.close()

def loadSQLite(file_name=None):
        conn = sqlite3.connect(file_name)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT _id,ITEM_LONGITUDE,ITEM_LATITUDE,ITEM_ADDRESS FROM delicacy")
            records =  [record for record in cursor.fetchall()]
        return records

def createCSV(file_name=None):
    records = loadSQLite("delicacy.db")
    with open(file_name,'w') as f:
        for record in records:
            # print type(record[0])
            # print type(record[1])
            # print type(record[2])
            # print "\"%s\""%record[3]

            if len(record) !=4:
                print "error record id:" + str(record[0])
                continue
            if type(record[1]) != float or type(record[2]) != float:
                print "error record id:" + str(record[0])
                continue
            string = "\"%i\",\"%f\",\"%f\",\"%s\"" % (record[0],record[1],record[2],record[3].encode('utf-8'))
            f.write(string+"\n")


if __name__ == '__main__':
    # createCSV('originLocations.csv')
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'db_config.txt'))
    db = MySQLdb.connect(host=config.get('DB','host'),
                     user=config.get('DB','user'),
                      passwd=config.get('DB','password'),
                      db=config.get('DB','db'),
                      port=int(config.get('DB','port')))
    # records = loadSQLite("delicacy.db")
    # upateDatabaseWithSpawnConn(records[0:1000],100)

    # N = 100 # num of workers
    # patchCommitNumber = 100 # number of sqls per transaction
    # records = loadSQLite("delicacy.db")
    # taskQueue = Queue()
    # for i in range(N):
    #     Worker(taskQueue,patchCommitNumber).start()
    # for record in records[30000:]:
    #     taskQueue.put( record )
    # for i in range(N):
    #     taskQueue.put(None)
    # upateDatabaseWithSpawnConn(records[-100:0],100)    
    