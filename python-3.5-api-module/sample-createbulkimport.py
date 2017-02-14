import merakiapi
import os
import re

from vars import org, apikey

# bulk network import filename

bncfile = 'bncimport.csv'

# API doesn't provide DNS information for device, these variables allow defining DNS manually

dns1 = '8.8.8.8'
dns2 = '8.8.4.4'

# API doesn't provide network mask information for device, this variable allows defining mask manually

netmask = '255.255.255.0'

# API doesn't provide VLAN ID information for device, this variable allows defining VLAN ID manually

vlan = '#'

# API doesn't provide notes information for device, this variable allows defining notes manually

notes = 'This text will be inserted in the notes field of all devices'

# API doesn't provide gateway information for devices, this variable allows defining gateway manually

gateway = '###.###.###.###'

# Check for existing bulk import file, if it doesn't exist create new file with header line

if os.path.isfile(bncfile):
    writefile = open(bncfile, 'a+')
else:
    writefile = open(bncfile, 'w+')
    print('Network name,Serial,Network tags,Name,Tags,Address,Notes,Static IP,Netmask,Gateway,DNS1,DNS2,VLAN',
          file=writefile)

orgnetworks = merakiapi.getnetworklist(apikey, org, suppressprint=True)

for network in orgnetworks:
    networkname = network['name']
    if 'tags' not in network:
        networktags = ''
    else:
        networktags = network['tags']
    devicelist = merakiapi.getnetworkdevices(apikey, network['id'], suppressprint=True)
    for device in devicelist:
        if 'serial' not in device:
            serialnum = ''
        else:
            serialnum = device['serial']
        if 'name' not in device:
            devicename = ''
        else:
            devicename = device['name']
        if 'model' not in device:
            devicemodel = ''
        else:
            devicemodel = device['model']
        if 'lanIp' not in device:
            deviceip = ''
        else:
            deviceip = device['lanIp']
        if 'tags' not in device:
            devicetags = ''
        else:
            devicetags = device['tags']
        if 'address' not in device:
            deviceaddr = ''
        else:
            deviceaddr = device['address']

            # Remove commas from address information as bulk network creator doesn't accept commas in field data

            deviceaddr = re.sub(',', ' ', deviceaddr)
            deviceaddr = re.sub('\n', ' ', deviceaddr)

        print('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}'.format(str(networkname), str(serialnum),
                                                                              str(networktags), str(devicename),
                                                                              str(devicetags), str(deviceaddr),
                                                                              str(notes), str(deviceip), str(netmask),
                                                                              str(gateway), str(dns1), str(dns2),
                                                                              str(vlan)), file=writefile)
writefile.close()
