#!/usr/bin/env python2.7
#
# A basic script to retrieve an SSID PSK and POST to a Tropo app
# 10/05/2016

import requests
import json
import meraki_info

# Global variables
api_key = meraki_info.api_key
ssid_url = meraki_info.ssid_url
tropo_token = meraki_info.tropo_token
tropo_api_url = meraki_info.tropo_api_url
tropo_phone = meraki_info.tropo_phone
tropo_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

#get the psk for the ssid @ ssid_url
def get_wifi_pw():
    headers = {
        'x-cisco-meraki-api-key': format(str(api_key)),
        'Content-Type': 'application/json'
    }
    get_ssid_pw = requests.get(ssid_url,headers=headers).text
    result = json.loads(get_ssid_pw)
    for key, value in result.iteritems():
        if key == 'psk':
            pw = value
        else:
            continue
    return pw

#guest_pw = result of the get_wifi_pw function
guest_pw = get_wifi_pw()

#the data that will be passed in the POST to Tropo
post_data = {"token": tropo_token,
             "pw": guest_pw,
             "number": tropo_phone
             }
#tropo_data = post_data jsonified
tropo_data = json.dumps(post_data)

#issue the post and print the http response code and response
tropo_post = requests.post(tropo_api_url,headers=tropo_headers, data=tropo_data)
print "http response code: %d" % tropo_post.status_code
print "http post response: "
print tropo_post.text