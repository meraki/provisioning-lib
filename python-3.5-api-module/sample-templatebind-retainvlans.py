########################################################################################################################
#
#  Sample Python Script using Meraki API module to migrate non-template bound networks to a specific template name
#  while retaining and re-applying static VLAN configuration
#
########################################################################################################################

import merakiapi

apikey = 'ENTER API KEY HERE'
orgid = 'ENTER ORG ID HERE'
templatename = 'ENTER THE NAME OF THE TARGET TEMPLATE HERE'


templates = merakiapi.gettemplates(apikey, orgid)

for template in templates:
    if template['name'] == templatename:
        templateid = template['id']

mxnetworks = []
networkvlans = []

x = 0

orgnets = merakiapi.getnetworklist(apikey, orgid)

for network in orgnets:
    if network['type'] == 'appliance':
        mxnetworks.append({'id': network['id']})

for mxnetwork in mxnetworks:
    vlans = merakiapi.getvlans(apikey, mxnetwork['id'])
    if vlans is None:
        pass
    else:
        for vlan in vlans:
            networkvlans.append({'id ': x, 'networkid': mxnetwork['id'], 'vlanid': vlan['id'], 'name': vlan['name'],
                                 'mxip': vlan['applianceIp'], 'subnet': vlan['subnet']})
            x += 1
            merakiapi.bindtotemplate(apikey,mxnetwork['id'],templateid)

for nvlan in networkvlans:
    merakiapi.updatevlan(apikey, nvlan['networkid'], nvlan['vlanid'], nvlan['name'], nvlan['mxip'], nvlan['subnet'])



