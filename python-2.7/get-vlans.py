#!/usr/bin/env python2.7
#
# Aaron Blair
# RIoT Solutions
# 
# aaron@aaronpb.me
#
# get-vlans.py - A simple Python script to get VLANs from Appliance Networks
# 15/03/2017

import argparse
import csv
import pprint
import requests
import signal
import sys
import json

count = 0
checknet = 0
paramslist = []
vlanoutput = 0
api_key = 'xxxxxxxxxxxxxxxxx' # <--- add your API key here
baseurl = 'https://dashboard.meraki.com/api/v0/'
orgurl = 'https://dashboard.meraki.com/api/v0/organizations/'
headers = {'X-Cisco-Meraki-API-Key': api_key,'Content-Type': 'application/json'}

#use argparse to handle command line arguments
parser = argparse.ArgumentParser(description="a script for getting the VLAN settings of a list of provided networks")
parser.add_argument('filename',
                    type=argparse.FileType('r'),
                    help='input txt file containing network IDs' )
parser.add_argument("ORGName",help='name of the ORG where you would like to get the VLANs for')

args = parser.parse_args()
#get the organization-name where the networks have to be updated as an argument
org=args.ORGName

#exit cleanly for SIGINT/Ctrl+C
def signal_handler(signal, frame):
    print("\n***Interrupt!*** ---> Exiting ...")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#read the txt file 
csvFile = args.filename
csvReader = csv.reader(csvFile)

#loop through the rows in the csvReader object and create a new list (paramslist) of JSON formatted attributes
for row in csvReader:
    NetworkId = str(row[0])
    params = NetworkId
    paramslist.append(params)

#get all of the orgs this API key has access to
orgsjson = requests.get(orgurl, headers=headers).text
output = json.loads(orgsjson)
#check whether the organization exists under the administered organization
if any(d['name'] == org for d in output):
    for row in output:
        orgname = row['name']
#get the ID of the ORG to create the networks URL
        if org == orgname:
            orgid = row['id']
            networks_url = (str(orgurl) + str(orgid) + '/networks')
            break
    
    #get the list of networks in the ORG
    networksjson = requests.get(networks_url, headers=headers).text
    output = json.loads(networksjson)

#go through every network in the input file
    for nwid in paramslist:
        checknet=0
        vlans_URL = (str(networks_url) + '/' + nwid + '/vlans')
#if network in csv matches network in dashboard, get the vlan-list
        vlansinnetwork = requests.get(vlans_URL, headers=headers).text
        vlanoutput = json.loads(vlansinnetwork)
        print json.dumps(vlanoutput, indent=4)          
#check whether networks in there are networks in the CSV that do not exist in this ORG
    for nwid in paramslist:
        netexist=0
        for row in output:
            if str(row['id']) == nwid:
                netexist+=1
        if netexist==0:
            print "The network " + nwid + " mentioned in the input file does not exist in this organization."

else:
    print "This ORG does not exist for your admin account"

csvFile.close();