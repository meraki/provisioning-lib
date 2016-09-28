#!/usr/bin/env python2.7

import requests
import json
import merakiapi
import meraki_info
import csv

# Global variables
api_key = meraki_info.api_key
base_url = meraki_info.base_url
org_id_list = []  # create a blank list

# Set the CSV output file and settings
output_file = open('network_id_list_report.csv', mode='wb')
csv_writer = csv.writer(output_file, delimiter=',', escapechar=' ', 
                        quoting=csv.QUOTE_NONE)

# Write the header row of the CSV file
header_row_text = "Net ID,Name"
csv_writer.writerow([header_row_text])

# Get all Org ID's
org_ids_json = merakiapi.myorgaccess(api_key)
# print org_ids_json

# Create a list of Org ID's called org_id_list
# For every row of JSON output, append the value of "v" (org ID) when k = 'id'
for row in org_ids_json:
    # print row
    for k,v in row.iteritems():
        if k == 'id':
            org_id_list.append(v)
        else:
            continue

# print org_id_list

# For every 'org' in org_id_list, use the getnetworklist function in the
# merakiapi library (Rob Watt) feeding it the api_key and Org ID it needs
for org in org_id_list:
    per_net_list = merakiapi.getnetworklist(api_key,org)
    for row in per_net_list:
        # For each 'row' of JSON in per_net_list, print the row to the terminal
        print "Raw JSON: %s \n" % row # for watching live
        # print str(row['type']) # just an example of how to reference a
        # specific value in the JSON
        for key, value in row.iteritems():
            # print "k,v is %s,%s" % (key,value) # example
            if key == 'name':
                net_name = value
            elif key == 'id':
                net_id = value
            else:
                continue
        csv_row_text = "%s, %s" % (str(net_id), str(net_name))
        csv_writer.writerow([csv_row_text])
        print "Writing to CSV: %s \n" % csv_row_text # for watching live

output_file.close()




