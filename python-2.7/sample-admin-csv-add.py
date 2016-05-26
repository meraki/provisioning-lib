#!/usr/bin/env python2.7
#
# admin-csv-add.py - A simple Python script to add
# admins across multiple Meraki Dashboard organizations
# 05/26/2016

import argparse
import csv
import pprint
import requests
import signal
import sys
import json

count = 0
params_list = []
api_key = '' # <--- add your API key here
baseurl = 'https://dashboard.meraki.com/api/v0/'
orgurl = 'https://dashboard.meraki.com/api/v0/organizations/'
headers = {'X-Cisco-Meraki-API-Key': api_key,'Content-Type': 'application/json'}

#use argparse to handle command line arguments
parser = argparse.ArgumentParser(description="a script for adding admins across multiple Meraki Dashboard organizations")
parser.add_argument('filename',
                    type=argparse.FileType('r'),
                    help='input CSV file' )

args = parser.parse_args()

#exit cleanly for SIGINT/Ctrl+C
def signal_handler(signal, frame):
    print("\n***Interrupt!*** ---> Exiting ...")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#read the CSV file into the csvReader object
csvFile = args.filename
csvReader = csv.reader(csvFile)

#loop through the rows in the csvReader object and create a new list (params_list) of JSON formatted attributes
for row in csvReader:
    pname = str(row[0])
    pemail = str(row[1])
    #you can change orgAccess to the appropriate permission level as needed
    params_format = '{"name":' + '"' + pname + '"' + ',' + ' "email":' + '"' + pemail + '"' + ',' + ' "orgAccess":"full"}'
    params_list.append(params_format)

#get all of the orgs this API key has access to
orgsjson = requests.get(orgurl, headers=headers)
output = json.loads(orgsjson.text)

#loop through the response (output), store the Org ID as 'id' and create the admins URL for each Org ID    
for row in output:
    id = row['id']
    admins_url = (str(orgurl) + str(id) + '/admins')
    #now loop through (params_list) and send them in an HTTP POST to every (admins_url), print HTTP status code & response per POST
    for line in params_list:
        count += 1
        linejson = json.loads(line)
        post_cmds = requests.post(admins_url, headers=headers, data=line)
        print "\n" + str(count) + '. Adding: ' + str(linejson['email']) + ' to Organization: ' + str(row['name'])
        print '     http status code: ' + str(post_cmds.status_code)
        print '     http response: ' + str(post_cmds.text)

csvFile.close();
