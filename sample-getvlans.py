import merakiapi

#
# Sample Python Script Using Meraki API module to pull VLAN Details for MX Devices in an organization
# Enter API Key and Organization ID into variables
#

apikey = 'xxxxx'
organizationid = 'xxxxxxxxxxx'

networks = merakiapi.getnetworklist(apikey, organizationid)

for row in networks:
    vlans = merakiapi.getvlans(apikey, row['id'])
    print('VLAN Details for Network ID {0}'.format(str(row['id'])))
    for vlanrow in vlans:
        vlandetail = merakiapi.getvlandetail(apikey, row['id'], vlanrow['id'])
        print(vlandetail, end='\n')
