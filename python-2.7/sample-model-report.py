#!/usr/bin/env python2.7
#
# sample-model-report.py - A simple Python script to generate a report (.csv) of
# device model counts across multiple Meraki Dashboard organizations
# 05/19/2016 v0.1

import csv
import requests
import signal
import sys
import json

count = 0  
api_key = '' # <----- add your API key here
base_url = 'https://dashboard.meraki.com/api/v0/'
org_url = 'https://dashboard.meraki.com/api/v0/organizations/'
headers = {'X-Cisco-Meraki-API-Key': api_key,'Content-Type': 'application/json'}


#exit cleanly for SIGINT/Ctrl+C
def signal_handler(signal, frame):
    print("\n***Interrupt!*** ---> Exiting ...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Get full JSON info from all Organizations
def getallorgsinfo():
    global api_key, org_url
    orgs=requests.get(org_url, headers=headers).text
    result = json.loads(orgs)
    return result

#Filter IDs of Org Dictionary
def getallorgsid(all_orgs_info):
    all_org_ids=[]
    for d in all_orgs_info:
        for key, value in d.iteritems():
            if key=='id':
                all_org_ids.append(value)
    return all_org_ids

#Get the Org-Name of a specific org-id
def getorgname(id,all_orgs_info):
    for d in all_orgs_info:
        if d["id"]==id:
            return d["name"]

# Get all inventory, store models and their count in a dictionary
def getorginv(org_id):
    org_inventory = {}
    inv_url = org_url + '/' + str(org_id) + '/inventory'
    inventory = requests.get(inv_url, headers=headers).text
    result = json.loads(inventory)
    for row in result:
        if row == 'errors':
            return 'errors'
        else:
            for key, value in row.iteritems():
                if key == 'model':
                    if not value in org_inventory:
                        org_inventory[value] = 1
                    else:
                        org_inventory[value] += 1
    return org_inventory

# Set the CSV output file and settings
ofile = open('model_report.csv', mode='wb')
csv_writer = csv.writer(ofile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)

# Write the top row of the CSV file
top_row_text = "Org ID,Name,Model,Device Count"
csv_writer.writerow([top_row_text])

# Store the list of organizations in all_orgs_info
all_orgs_info = getallorgsinfo()

# Store the list of org id's in all_ids
all_ids = getallorgsid(all_orgs_info)

# Loop through each org id to get the name, device model, and count
# Assemble the row to be written to CSV
for i in all_ids:
    dev_count = 0
    org_name = getorgname(i, all_orgs_info)
    inv = getorginv(i)
    for k, v in inv.iteritems():
        model_name = k
        dev_count = v
        row_text = "%d, %s, %s, %d" % (i, str(org_name), model_name, dev_count)
        csv_writer.writerow([row_text])

ofile.close()