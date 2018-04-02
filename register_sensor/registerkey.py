#Usage python registerkey.py -c "$NEWCLIENT" -s "$NAME"
import os, sys, getopt
import re
from pymongo import MongoClient, InsertOne
import datetime
from pytz import timezone, utc
import pytz
import glob
import urllib2
from pprint import pprint

def main(argv):
    CLIENT_NAME=""
    SENSOR_NAME=""
    FORCED_IP=""

    try:
        opts, args = getopt.getopt(argv,"hc:s:i:",["client_name=","sensor_name=","ip="])
    except getopt.GetoptError:
        print 'python register_sensor.py -c "$NEWCLIENT" -s "$NAME" -i "$IP"'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python register_sensor.py -c "$NEWCLIENT" -s "$NAME" -i "$IP"'
            sys.exit()
        elif opt in ("-c", "--client_name"):
            CLIENT_NAME = arg
        elif opt in ("-s", "--sensor_name"):
            SENSOR_NAME = arg
        elif opt in ("-i", "--ip"):
            FORCED_IP = arg
    print 'CLIENT_NAME is ', CLIENT_NAME
    print 'SENSOR_NAME is ', SENSOR_NAME

    #Initiate Database Connection
    mclient = MongoClient()
    db = mclient.vpnstatus
    collection = db.clients

    found=False
    for clientdoc in collection.find():
        mname=clientdoc.get('common_name')
        if mname==CLIENT_NAME:
            collection.update_one({'common_name':CLIENT_NAME}, {"$set": {'name':SENSOR_NAME}}, upsert=False)
            found = True
    if found == False:
        doc = {'common_name':CLIENT_NAME,'name':SENSOR_NAME}
        result = collection.insert(doc)
    if not FORCED_IP == "":
        collection.update_one({'common_name':CLIENT_NAME}, {"$set": {'forced_ip':FORCED_IP}}, upsert=False)

    print "Result:"
    for clientdoc in collection.find():
        if clientdoc.get('common_name') == CLIENT_NAME :
            pprint(clientdoc)

if __name__ == "__main__":
    main(sys.argv[1:])
