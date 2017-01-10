#!/usr/bin/env python2.7
#
# msp-license-inventory-report.py
# A simple Python script to generate a report of license status and
# device type counts (similar to the MSP Portal page)
# across multiple Meraki Dashboard organizations


import csv
import merakiapi
import meraki_info


# global variables used in the script
my_api_key = meraki_info.api_key
base_url = 'https://dashboard.meraki.com/api/v0/organizations'
headers = {'X-Cisco-Meraki-API-Key': my_api_key,
           'Content-Type': 'application/json'
           }


# create a list of org id's
def get_all_orgids():
    all_org_ids = []
    result = merakiapi.myorgaccess(my_api_key)
    for row in result:
        all_org_ids.append(row['id'])
    return all_org_ids

# get the org name of an org id
# read the name from the full org info we already have
def getorgname(id,all_orgs_info):
    for d in all_orgs_info:
        if d['id']==id:
            return d["name"]


# get org inventory and store models and their counts in a dictionary
def get_org_inv_count(org_id):
    """
    This function uses requests to GET the org inventory, counts the model
    types, and writes them to a dictionary called org_inventory
    """
    # creates the dictionary called org_inventory to store key,value pairs
    org_inventory = {}
    result = merakiapi.getorginventory(my_api_key, org_id)
    for row in result:
        if row == 'errors':
            return 'errors'
        elif row == '':
            return 'empty'
        else:
            # iterate through the json response from the GET inventory
            """
            if the model (example:'MX65') does not already exist in the dictionary: 'org_inventory',
            set the value of org_inventory['MX65'] to 1 (for the first one). if 'MX65' is an existing
            key in 'org_inventory', then +1 the value (count) of org_inventory['MX65'].
            """
            if not row['model'] in org_inventory:
                org_inventory[(row['model'])] = 1
            else:
                org_inventory[(row['model'])] += 1
    return org_inventory


# Set the CSV output file and settings
ofile = open('msp_license_inventory_report.csv', mode='wb')
csv_writer = csv.writer(ofile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)


# Write the top row of the CSV file
top_row_text = "Name,License Expiration,MX,MS,MR"
csv_writer.writerow([top_row_text])


# Store the list of organizations in all_orgs_info
all_orgs_info = merakiapi.myorgaccess(my_api_key)


# Store the list of org id's in all_ids
all_ids = get_all_orgids()


# get all org license state and inventory, then write to CSV file
def create_license_model_report():
    # Loop through each org id to grab the name, license state, and device inventory
    for i in all_ids:
        mr_count = 0
        mx_count = 0
        ms_count = 0
        org_name = getorgname(i, all_orgs_info)
        license_state = merakiapi.getlicensestate(my_api_key, i)
        # remove the comma from the expiration date to avoid CSV trouble
        lic_exp_date = license_state['expirationDate'].replace(',','')
        # skip orgs with no licensing
        if lic_exp_date == 'N/A':
            print("{0} - License N/A, skipping !".format(str(org_name)))
            continue
        else:
            inventory = get_org_inv_count(i)
            for model in inventory:
                print("model:{0}, count: {1}".format(str(model),inventory[model]))
                # aggregate the individual model counts into MX/MR/MS totals
                if model[:2] == 'MR':
                    mr_count += inventory[model]
                elif model[:2] == 'MX':
                    mx_count += inventory[model]
                elif model[:2] == 'MS':
                    ms_count += inventory[model]
                else:
                    # for future use beyond MR/MX/MS
                    dev_model = model
                    dev_count = inventory[model]

            csv_row = "{0}, {1}, {2}, {3}, {4}".format(str(org_name), str(lic_exp_date), str(mx_count), str(ms_count), str(mr_count))
            print("Writing to CSV: {0}".format(str(csv_row)))
            csv_writer.writerow([csv_row])

create_license_model_report()

ofile.close()
