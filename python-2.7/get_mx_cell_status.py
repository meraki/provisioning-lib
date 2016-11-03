#!/usr/bin/env python2.7
#
# A basic script to poll the devCellularStatus OID and report devices with
# 'Active' status on the terminal and to a CSV file
# Note: devices that go offline after 'Active' cellular continue to report as
# active until they reconnect to dashboard to update their status

import csv
import meraki_info
# snmp_helper courtesy Kirk Byers: https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py
import snmp_helper


# Global variables
snmp_port = meraki_info.snmp_port
community_string = meraki_info.community_string

# Set the CSV output file and settings
output_file = open('mx_active_cellular_report.csv', mode='wb')
csv_writer = csv.writer(output_file, delimiter=',', escapechar=' ',
                        quoting=csv.QUOTE_NONE)

# Write the header row of the CSV file
header_row_text = "Device(s) with active celluar"
csv_writer.writerow([header_row_text])

# A blank list of device names with active cellular status
cell_active_list = []


def get_cell_status():
    # community_string and snmp_port are set under global variables
    device = ('snmp.meraki.com', community_string, snmp_port)
    # devCellularStatus
    snmp_data = snmp_helper.snmp_get_oid(device, oid='.1.3.6.1.4.1.29671.1.1.4.1.14', display_errors=True)

    for row in snmp_data:
        # for each response with 'Active' cellular status, append the devName to cell_active_list
        if row[0][1] == 'Active':
            # dup of the original function to extract [0][0] vs. [0][1]
            extract_oid = snmp_helper.snmp_extract2(row)
            # replace the front of the oid to create a new oid for name lookup
            name_oid = extract_oid.replace('SNMPv2-SMI::enterprises.29671.1.1.4.1.14', '.1.3.6.1.4.1.29671.1.1.4.1.2')
            # lookup and extract the devName of the device with 'Active' cellular status
            # dup of the original function that issues a get vs. getNext
            snmp_name = snmp_helper.snmp_get_oid2(device, oid=name_oid, display_errors=True)
            dev_name = snmp_helper.snmp_extract(snmp_name)
            # append devName to cell_active_list
            cell_active_list.append(dev_name)
            # write devName to CSV
            csv_row_text = format(str(dev_name))
            csv_writer.writerow([csv_row_text])
            print "writing to CSV: %s" % csv_row_text  # for watching live
        else:
            # ignoring anything without 'Active' status
            continue
    return cell_active_list


output = get_cell_status()
speech_output = "%s device(s) reported active cellular status: %s" % \
                    (str(len(output)), " , ".join(output))
print speech_output

output_file.close()
