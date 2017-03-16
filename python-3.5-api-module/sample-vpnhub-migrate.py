import sys
import getopt
import merakiapi
from vars import apikey, org
import csv
import copy
import requests
import json

base_url = 'https://dashboard.meraki.com/api/v0'


########################################################################################################################
#   Cisco Meraki VPN Hub Migration Script
#
#   Takes a CSV input file of network name to VPN Hub Network name mappings and assigns VPN hub priority based on CSV
#
#   CSV Format = networkname,hub1name,hub1defaultroute,hub2name,hub2defaultroute,hub3name,hub3defaultroute...
#
#   There is no limit to the number of hubs per network, script will parse all until line is complete.
#   Default Route Parameter is either true or false PER hub
#
#   Create vars.py with an apikey and org variable that contain your api key and organization ID values
#   Place the merakiapi.py file in directory
#
########################################################################################################################

def main(argv):
    outputfile = 'results.csv'
    hasinput = False
    hasoutput = False
    hasinvalidin = False

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Usage: python3 sample-vpnhub-migrate.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: python3 sample-vpnhub-migrate.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            hasinput = True
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            hasoutput = True

    if hasinput is False:
        print('Usage: python3 sample-vpnhub-migrate.py -i <inputfile> -o <outputfile>\n')
        print('Input file must be specified')
        exit()

    if hasoutput is False:
        print('\n***WARNING***\nNo output file specified, "{0}" will be used for output'.format(str(outputfile)))

    try:
        infile = open(inputfile)
        vpnnetmap = list(csv.reader(infile))
        errorcsv = inputfile+'.error'

    except IOError:
            print("***ERROR***\nInput file does not exist: {0}".format(str(inputfile)))
            exit()
    finally:
        infile.close()

    orgnets = merakiapi.getnetworklist(apikey, org, suppressprint=True)
    hubs = []

    for net in orgnets:
        if net['type'] in ('appliance', 'combined'):
            vpntype = merakiapi.getvpnsettings(apikey,net['id'], suppressprint=True)
            if vpntype['mode'] == 'hub':
                hubs.append({'id':net['id'], 'name':net['name']})

    vpnnetmap.pop(0)
    originalmap = copy.deepcopy(vpnnetmap)

    out = open(outputfile,'w+')
    for idx, v in enumerate(vpnnetmap):
        x = 1
        invalidname = False

        try:
            v[0] = next(item for item in orgnets if item['name'] == v[0])['id']
        except StopIteration:
            print('\n***ERROR***\nNetwork name "{0}" is invalid'.format(str(v[0])))
            v[0] = 'INVALID NAME'
            originalmap[idx][0] = 'INVALID NAME'
            hasinvalidin = True
            invalidname = True
        if invalidname == False:
            while x < len(v) and len(v) > 1:
                if x % 2 == 0:
                    if str(v[x]).lower() not in ['true', 'false']:
                        print('\n***ERROR***\nVPN hub default route must BE True or False')
                        v[x] = 'NOT TRUE/FALSE'
                        originalmap[idx][x] = 'NOT TRUE/FALSE'
                        hasinvalidin = True
                else:
                    try:
                        v[x] = next(item for item in hubs if item['name'] == v[x])['id']
                    except StopIteration:
                        print('\n***ERROR***\n"{0}" is not a valid VPN Hub Network - See output file for details'
                              .format(str(v[x])))
                        v[x] = 'INVALID HUB'
                        originalmap[idx][x] = 'INVALID HUB'
                        hasinvalidin = True
                x += 1

    for idx, n in enumerate(vpnnetmap):
        if ('INVALID HUB' in n) or ('NOT TRUE/FALSE' in n) or ('INVALID NAME' in  n):
            pass
        else:
            newhubs = []
            oldvpn = merakiapi.getvpnsettings(apikey,n[0],suppressprint=True)
            for h, d in zip(n[1::2], n[2::2]):
                newhubs.append({'useDefaultRoute': bool(d), 'hubId': h})
            newvpn = copy.deepcopy(oldvpn)
            newvpn['hubs'] = newhubs

            headers = {
                'x-cisco-meraki-api-key': format(str(apikey)),
                'Content-Type': 'application/json'
            }

            putdata = json.dumps(newvpn)
            puturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(n[0]))
            dashboard = requests.put(puturl, data=putdata, headers=headers)
            if dashboard.status_code == 200:
                print('\nUpdating Network - "{0}"'.format(str(originalmap[idx][0])))
                print('Network:\n{0}\nOld Data:\n{1}\nNew Data:\n{2}'.format(str(originalmap[idx][0]), str(oldvpn),
                                                                             str(newvpn)), file=out)
            else:
                print('Network:\n{0}\nAPI Call Failed\n{1}'.format(str(originalmap[idx][0]), str(dashboard.text)),
                      file=out)
    if hasinvalidin == True:
        print('\n****ERRORS FOUND IN INPUT FILE****\nInvalid Entries in input CSV, see {0} for details'
              .format(str(errorcsv)))
        with open(errorcsv, 'w+', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(originalmap)
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])