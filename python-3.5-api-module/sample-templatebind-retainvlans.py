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

orgnets = merakiapi.getnetworklist(apikey, orgid)

for network in orgnets:
    if network['type'] == 'appliance' and network['name'][:2] == 'zz':
        mxnetworks.append({'id': network['id'], 'name': network['name']})

for mxnetwork in mxnetworks:
    newnet = True
    vlans = merakiapi.getvlans(apikey, mxnetwork['id'])
    if vlans is None:
        pass
    elif newnet is True:
        print('\nBinding Network - {0}'.format(str(mxnetwork['name'])))
        merakiapi.bindtotemplate(apikey, mxnetwork['id'], templateid)
        newnet = False
    x = 0

    for vlan in vlans:
        nvlan = {'idx': x, 'networkid': mxnetwork['id'], 'vlanid': vlan['id'], 'name': vlan['name'],
                 'mxip': vlan['applianceIp'], 'subnet': vlan['subnet']}
        print('\nUpdating VLAN ID {0} in Network {1}:\nSubnet IP {2}\nAppliance IP {3}'.format(str(nvlan['vlanid']),
                                                                                               str(mxnetwork['name']),
                                                                                               str(nvlan['subnet']),
                                                                                               str(nvlan['mxip'])))
        merakiapi.updatevlan(apikey, nvlan['networkid'], nvlan['vlanid'], mxip=nvlan['mxip'],
                             subnetip=vlan['subnet'])
        x += 1
