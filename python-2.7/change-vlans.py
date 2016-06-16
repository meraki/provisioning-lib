#!/usr/bin/env python2.7
#
# filevlan.py - A simple Python script to change VLANs to Appliance Networks that are bound to a Template
# 06/06/2016

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
parser = argparse.ArgumentParser(description="a script for changing VLAN settings for Appliance Networks bound to a Template")
parser.add_argument('filename',
                    type=argparse.FileType('r'),
                    help='input CSV file' )
parser.add_argument("ORGName",help='name of the ORG where you would like the CSV applied to')

args = parser.parse_args()
#get the organization-name where the networks have to be updated as an argument
org=args.ORGName

#exit cleanly for SIGINT/Ctrl+C
def signal_handler(signal, frame):
    print("\n***Interrupt!*** ---> Exiting ...")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#read the CSV file into the csvReader object
csvFile = args.filename
csvReader = csv.reader(csvFile)
next(csvReader,None) #skip headers

#loop through the rows in the csvReader object and create a new list (paramslist) of JSON formatted attributes
for row in csvReader:
    NetworkName = str(row[0])
    IPSubnet = str(row[1])
    IPGateway = str(row[2])
    VLANID = str(row[3])
    params= '{"name":' + '"' + NetworkName + '"' + ',' + ' "subnet":' + '"' + IPSubnet + '"' + ',' + ' "applianceIp":' + '"' + IPGateway + '"' + ',' + ' "id":' + '"' + VLANID + '"}'
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
    print "Checking networks....."
#get the list of networks in the ORG
    networksjson = requests.get(networks_url, headers=headers).text
    output = json.loads(networksjson)
    print "Checking vlans......"
#go through every network in the ORG
    for row in output:
        checknet=0
        vlans_URL = (str(networks_url) + '/' + row["id"] + '/vlans')
#go through every line in the csv-list
        for line in paramslist:
            linejson = json.loads(line)
#if network in csv matches network in dashboard, get the vlan-list
            if linejson["name"] == row['name']:
                checknet+=1
                if vlanoutput == 0:
                    vlansinnetwork = requests.get(vlans_URL, headers=headers).text
                    vlanoutput = json.loads(vlansinnetwork)
#if vlan in csv exists in dashboard-network then update it
                if any(str(f['id']) == str(linejson["id"]) for f in vlanoutput):
                    change_URL = vlans_URL + '/' + linejson['id']
                    putdata = {
                        'applianceIp': format(str(linejson["applianceIp"])),
                        'subnet': format(str(linejson["subnet"]))
                    }
                    putdata = json.dumps(putdata)
                    print "Reconfiguring VLAN " + linejson["id"] + " in Network " + linejson["name"]
                    dashboard = requests.put(change_URL, data=putdata, headers=headers)
                    print '     http status code: ' + str(dashboard.status_code)
                    print '     http response: ' + str(dashboard.text)
                else:
                    print "VLAN " + linejson['id'] + " in Network " + linejson['name'] + " does not exist. Please check the CSV and dashboard."              
#check whether there are networks in the ORG that have not been updated
        if checknet==0:
            print "No Updates have been made in Network " + row['name'] + " as there's no entry in the CSV file."
#check whether networks in there are networks in the CSV that do not exist in this ORG
    for line in paramslist:
        netexist=0
        linejson = json.loads(line)
        for row in output:
            if str(row['name']) == str(linejson['name']):
                netexist+=1
        if netexist==0:
            print "The network " + linejson['name'] + " mentioned in the csv does not exist in this organization."

else:
    print "This ORG does not exist for your admin account"

csvFile.close();
