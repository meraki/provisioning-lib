import json
import os
import sys
import time

import merakiapi
import requests

# Enter User's API Key
apikey = 'xxxxxx'

# Enter Organization ID Here
organizationid = 'xxxxxxxxx'

# Device Model to apply tags to: MR/MS/MX
devicemodel = 'MR'

# Enter Tag String Below
# NOTE: Tag String MUST begin with a single space and end with a single space.  Separate tags with a single space
# CAUTION: Existing tags will be replaced with the tags defined in this script
newtags = ' Lab Test API '
#
# Get Organization Wide Device Inventory
#
print('Getting Dashboard Inventory for Organization - {0}'.format(organizationid))
devicelist = merakiapi.getorgdevices(apikey, organizationid)

#
# Check for existence of error results text file, if exists remove
#
if os.path.isfile('results.txt'):
    if os.path.isfile('results.old'):
        os.remove('results.old')
    os.rename('results.txt', 'results.old')


resultfile = open('results.txt', 'w')
errorcount = 0
changecount = 0
filterresults = []
#
# Parse the Inventory for MR devices and create an object containing only the networkId and Serial
#
for row in devicelist:
    if row['networkId'] is not None:
        model = row['model']
        if model[:2] == devicemodel:
            filterresults.append({'networkId': row['networkId'], 'serial': row['serial']})
print('Applying settings to the following devices:')
#
# Perform HTTP PUT for each row in filtered inventory, print serial number and settings applied
#
headers = {
    'x-cisco-meraki-api-key': apikey,
    'Content-Type': 'application/json'
    }
x = 0
loop_start=time.time()
for row in filterresults:
    deviceurl = 'https://dashboard.meraki.com/api/v0/networks/' + row['networkId'] + '/devices/' + row['serial']
    data = {'tags': newtags}
    putresult = requests.put(deviceurl, data=json.dumps(data), headers=headers)
    print(row['serial'] + " - " + data['tags'])
    #
    # If the HTTP PUT results in anything other than status code 200, increment error count and log URL
    #
    if putresult.status_code != 200:
        errorresult = "PUT resulted in status code: {0}\nPUT URL used was: {1}".format(str(
             putresult.status_code), deviceurl)
        print(errorresult, file=resultfile)
        errorcount += 1
    else:
        changecount += 1
loop_total=time.time()-loop_start
print('Total Loop Time: {0}\nPut/second: {1}'.format(str(loop_total),str(changecount/loop_total)))
#
# If error counter is greater than 0 exit with error
#
print("Total Number of Devices Changed: {0}\nTotal Number of Errors: {1}".format(str(changecount), str(errorcount)),
      file=resultfile)
resultfile.close()
print('\nChange Summary:\nTotal Number of Devices Changed: {0}\nTotal Number of Errors: {1}'.format(str(changecount),
                                                                                                    str(errorcount)))

if errorcount > 0:
    sys.exit("\nAn error occured during execution, check results.txt for details")
