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
    outfile = 'results.out'
    backupfile = 'backup.vpn'
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
            outfile = arg
            hasoutput = True

    if hasinput is False:
        print('Usage: python3 sample-vpnhub-migrate.py -i <inputfile> -o <outputfile>\n')
        print('Input file must be specified')
        exit()

    if hasoutput is False:
        print('\n***WARNING***\nNo output file specified, "{0}" will be used for output'.format(str(outfile)))

    print('\n*** Original VPN JSON results will be backed up to {0}'.format(str(backupfile)))

    try:
        filein = open(inputfile)
        fileout = open(outfile, 'w')
        backup = open(backupfile, 'w')
        vpnnetmap = list(csv.DictReader(filein))
        originalmap = copy.deepcopy(vpnnetmap)

        keys = vpnnetmap[0].keys()

        if len(keys) % 2 != 1 or len(keys) < 3:
            raise KeyError('Invalid number of columns, CSV file must include a network name and at least one pair of '
                           'hubname and defaultroute definitions, e.g. "networkname,vpn1hubname,vpn1defaultroute"')
        numhubs = int(((len(keys) - 1) / 2))

        newhublist = []
        newhub = {}

        orgnets = merakiapi.getnetworklist(apikey, org, suppressprint=True)

        for idx, vl in enumerate(vpnnetmap):
            invalidentry = False
            originalmap[idx].update({'error': None, 'posterror': None})
            if not any(n['name'] == str(vl['networkname']) for n in orgnets):
                originalmap[idx]['error'] = 'INVALID NETWORK NAME'
                hasinvalidin = True
                invalidentry = True

            else:
                networkdetails = next((net for net in orgnets if net['name'] == vl['networkname']), None)

                if networkdetails is not None:
                    nid = str(networkdetails['id'])
                    oldvpn = merakiapi.getvpnsettings(apikey, nid, suppressprint=True)
                    backup.write(json.dumps(oldvpn) + '\n')
                    newvpn = copy.deepcopy(oldvpn)
                    newvpn.update({'networkId': nid})

                else:
                    oldvpn = None

                if oldvpn['mode'] == 'none' or oldvpn is None:
                    originalmap[idx]['error'] = 'NETWORK NOT CURRENTLY CONFIGURED FOR VPN'
                    hasinvalidin = True
                    invalidentry = True
                else:
                    x = 1
                    while x <= numhubs:
                        # if not any(n['name'] == vl['vpn{0}hubname'.format(str(x))] for n in orgnets):
                        #     originalmap[idx]['error'] == 'INVALID HUB NAME FOR HUB {0}'.format(str(x))
                        #     hasinvalidin == True
                        newhub.clear()
                        hubkey = 'vpn' + str(x) + 'hubname'
                        drkey = 'vpn' + str(x) + 'defaultroute'
                        if vl[hubkey] is not None and vl[drkey] is not None:
                            temphubid = (n['id'] for n in orgnets if n['name'] == vl[hubkey])
                            newhub['hubId'] = ''.join(temphubid)
                            if str(vl[drkey]).lower() in {'true', 'false'} and vl[drkey] is not None:
                                if str(vl[drkey]).lower() == 'true':
                                    newhub['useDefaultRoute'] = bool(1)
                                elif str(vl[drkey]).lower() == 'false':
                                    newhub['useDefaultRoute'] = bool(0)
                                newhublist.append(copy.deepcopy(newhub))
                            else:
                                originalmap[idx]['error'] = 'HUB {0}, INVALID DEFAULT ROUTE MUST BE TRUE/FALSE IF HUB' \
                                                            'DEFINED'.format(str(x))
                                hasinvalidin = True
                                invalidentry = True
                        x += 1

            if newvpn['mode'] != 'none' and invalidentry is not True:
                newvpn['hubs'] = newhublist

                headers = {
                    'x-cisco-meraki-api-key': format(str(apikey)),
                    'Content-Type': 'application/json'
                }
                nid = newvpn.pop('networkId', None)
                putdata = json.dumps(newvpn)
                puturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(nid))
                dashboard = requests.put(puturl, data=putdata, headers=headers)
                if dashboard.status_code == 200:
                    print('\nUpdated Network - "{0}"'.format(str(nid)))
                else:
                    originalmap[idx]['posterror'] = 'UNABLE TO POST - STATUS CODE {0}'.format(str(dashboard.status_code))
                    hasinvalidin == True

            for e in originalmap:
                try:
                    if e['error'] is not None or e['posterror'] is not None:
                        print(json.dumps(e) + '\n', file=fileout)
                except KeyError:
                    pass

        if hasinvalidin == True:
            print('\n****ERRORS FOUND IN INPUT FILE****\nInvalid Entries in input CSV, see {0} for details'
                  .format(str(outfile)))


    except IOError:
            print("***ERROR***\nInput file does not exist: {0}".format(str(inputfile)))
            exit()



    finally:
        filein.close()
        fileout.close()
        backup.close()

if __name__ == "__main__":
    main(sys.argv[1:])