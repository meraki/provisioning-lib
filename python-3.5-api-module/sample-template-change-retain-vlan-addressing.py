########################################################################################################################
#
#  Sample Python script using the Meraki API module to migrate networks bound to an "old" template to a
#  "new" template while retaining and re-applying VLAN IP address configuration
#
########################################################################################################################

import merakiapi
import my_vars

# API key, Org, and Config template ID's can be set directly in this script instead of importing from a my_vars file
apikey = my_vars.api_key
orgid = my_vars.org_id
old_templateid = my_vars.old_template_id
new_templateid = my_vars.new_template_id
mxnetworks = []

# GET the list of networks under an Org ID
orgnets = merakiapi.getnetworklist(apikey, orgid)


# Create a list of networks bound to "old" configTemplateId
for network in orgnets:
    for k,v in network.items():
        if k == 'configTemplateId' and v == old_templateid:
            print('Network: {0} is bound to old template ID: {1} !'.format(str(network['name']), str(old_templateid)))
            mxnetworks.append({'id': network['id'], 'name': network['name']})


# Loop through each network, GET VLAN info, unbind/bind old/new template
for mxnetwork in mxnetworks:
    newnet = True
    vlans = merakiapi.getvlans(apikey, mxnetwork['id'])
    print('Storing current VLAN IP addressing...\n{0}'.format(str(vlans)))
    if vlans is None:
        pass
    elif newnet is True:
        print('\nUnbinding Network - {0}'.format(str(mxnetwork['name'])))
        merakiapi.unbindfromtemplate(apikey, mxnetwork['id'])
        print('\nBinding Network - {0} to new Template ID: {1}'.format(str(mxnetwork['name']), str(new_templateid)))
        merakiapi.bindtotemplate(apikey, mxnetwork['id'], new_templateid)
        newnet = False
    x = 0

    # Re-apply original VLAN IP addressing (with old template) to ALL VLANs following new template bind
    for vlan in vlans:
        nvlan = {'idx': x, 'networkid': mxnetwork['id'], 'vlanid': vlan['id'], 'name': vlan['name'],
                 'mxip': vlan['applianceIp'], 'subnet': vlan['subnet']}
        print('\nUpdating VLAN ID {0} in Network: {1}:\nSubnet IP {2}\nAppliance IP {3}'.format(str(nvlan['vlanid']),
                                                                                               str(mxnetwork['name']),
                                                                                               str(nvlan['subnet']),
                                                                                               str(nvlan['mxip'])))
        merakiapi.updatevlan(apikey, nvlan['networkid'], nvlan['vlanid'], mxip=nvlan['mxip'],
                             subnetip=vlan['subnet'])
        x += 1

