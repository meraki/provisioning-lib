#######################################################################################################################
#
#  Cisco Meraki Provisioning API Python 3.x Module
#
# Overview
# The purpose of this Python module is to provide a standard Python module to interact with the Meraki Provisioning API.
# Each method in this function interacts seamlessly with the API and either returns data from the method call or a
# status message indicating the result of the API call
#
# Dependencies
# - Python 3.x
# - 'requests' module
#
#######################################################################################################################

import requests
import json
from ipaddress import ip_address
import re
import warnings


tzlist = ['Africa/Abidjan',
          'Africa/Accra',
          'Africa/Addis_Ababa',
          'Africa/Algiers',
          'Africa/Asmara',
          'Africa/Asmera',
          'Africa/Bamako',
          'Africa/Bangui',
          'Africa/Banjul',
          'Africa/Bissau',
          'Africa/Blantyre',
          'Africa/Brazzaville',
          'Africa/Bujumbura',
          'Africa/Cairo',
          'Africa/Casablanca',
          'Africa/Ceuta',
          'Africa/Conakry',
          'Africa/Dakar',
          'Africa/Dar_es_Salaam',
          'Africa/Djibouti',
          'Africa/Douala',
          'Africa/El_Aaiun',
          'Africa/Freetown',
          'Africa/Gaborone',
          'Africa/Harare',
          'Africa/Johannesburg',
          'Africa/Juba',
          'Africa/Kampala',
          'Africa/Khartoum',
          'Africa/Kigali',
          'Africa/Kinshasa',
          'Africa/Lagos',
          'Africa/Libreville',
          'Africa/Lome',
          'Africa/Luanda',
          'Africa/Lubumbashi',
          'Africa/Lusaka',
          'Africa/Malabo',
          'Africa/Maputo',
          'Africa/Maseru',
          'Africa/Mbabane',
          'Africa/Mogadishu',
          'Africa/Monrovia',
          'Africa/Nairobi',
          'Africa/Ndjamena',
          'Africa/Niamey',
          'Africa/Nouakchott',
          'Africa/Ouagadougou',
          'Africa/Porto-Novo',
          'Africa/Sao_Tome',
          'Africa/Timbuktu',
          'Africa/Tripoli',
          'Africa/Tunis',
          'Africa/Windhoek',
          'America/Adak',
          'America/Anchorage',
          'America/Anguilla',
          'America/Antigua',
          'America/Araguaina',
          'America/Argentina/Buenos_Aires',
          'America/Argentina/Catamarca',
          'America/Argentina/ComodRivadavia',
          'America/Argentina/Cordoba',
          'America/Argentina/Jujuy',
          'America/Argentina/La_Rioja',
          'America/Argentina/Mendoza',
          'America/Argentina/Rio_Gallegos',
          'America/Argentina/Salta',
          'America/Argentina/San_Juan',
          'America/Argentina/San_Luis',
          'America/Argentina/Tucuman',
          'America/Argentina/Ushuaia',
          'America/Aruba',
          'America/Asuncion',
          'America/Atikokan',
          'America/Atka',
          'America/Bahia',
          'America/Bahia_Banderas',
          'America/Barbados',
          'America/Belem',
          'America/Belize',
          'America/Blanc-Sablon',
          'America/Boa_Vista',
          'America/Bogota',
          'America/Boise',
          'America/Buenos_Aires',
          'America/Cambridge_Bay',
          'America/Campo_Grande',
          'America/Cancun',
          'America/Caracas',
          'America/Catamarca',
          'America/Cayenne',
          'America/Cayman',
          'America/Chicago',
          'America/Chihuahua',
          'America/Coral_Harbour',
          'America/Cordoba',
          'America/Costa_Rica',
          'America/Creston',
          'America/Cuiaba',
          'America/Curacao',
          'America/Danmarkshavn',
          'America/Dawson',
          'America/Dawson_Creek',
          'America/Denver',
          'America/Detroit',
          'America/Dominica',
          'America/Edmonton',
          'America/Eirunepe',
          'America/El_Salvador',
          'America/Ensenada',
          'America/Fort_Nelson',
          'America/Fort_Wayne',
          'America/Fortaleza',
          'America/Glace_Bay',
          'America/Godthab',
          'America/Goose_Bay',
          'America/Grand_Turk',
          'America/Grenada',
          'America/Guadeloupe',
          'America/Guatemala',
          'America/Guayaquil',
          'America/Guyana',
          'America/Halifax',
          'America/Havana',
          'America/Hermosillo',
          'America/Indiana/Indianapolis',
          'America/Indiana/Knox',
          'America/Indiana/Marengo',
          'America/Indiana/Petersburg',
          'America/Indiana/Tell_City',
          'America/Indiana/Vevay',
          'America/Indiana/Vincennes',
          'America/Indiana/Winamac',
          'America/Indianapolis',
          'America/Inuvik',
          'America/Iqaluit',
          'America/Jamaica',
          'America/Jujuy',
          'America/Juneau',
          'America/Kentucky/Louisville',
          'America/Kentucky/Monticello',
          'America/Knox_IN',
          'America/Kralendijk',
          'America/La_Paz',
          'America/Lima',
          'America/Los_Angeles',
          'America/Louisville',
          'America/Lower_Princes',
          'America/Maceio',
          'America/Managua',
          'America/Manaus',
          'America/Marigot',
          'America/Martinique',
          'America/Matamoros',
          'America/Mazatlan',
          'America/Mendoza',
          'America/Menominee',
          'America/Merida',
          'America/Metlakatla',
          'America/Mexico_City',
          'America/Miquelon',
          'America/Moncton',
          'America/Monterrey',
          'America/Montevideo',
          'America/Montreal',
          'America/Montserrat',
          'America/Nassau',
          'America/New_York',
          'America/Nipigon',
          'America/Nome',
          'America/Noronha',
          'America/North_Dakota/Beulah',
          'America/North_Dakota/Center',
          'America/North_Dakota/New_Salem',
          'America/Ojinaga',
          'America/Panama',
          'America/Pangnirtung',
          'America/Paramaribo',
          'America/Phoenix',
          'America/Port_of_Spain',
          'America/Port-au-Prince',
          'America/Porto_Acre',
          'America/Porto_Velho',
          'America/Puerto_Rico',
          'America/Rainy_River',
          'America/Rankin_Inlet',
          'America/Recife',
          'America/Regina',
          'America/Resolute',
          'America/Rio_Branco',
          'America/Rosario',
          'America/Santa_Isabel',
          'America/Santarem',
          'America/Santiago',
          'America/Santo_Domingo',
          'America/Sao_Paulo',
          'America/Scoresbysund',
          'America/Shiprock',
          'America/Sitka',
          'America/St_Barthelemy',
          'America/St_Johns',
          'America/St_Kitts',
          'America/St_Lucia',
          'America/St_Thomas',
          'America/St_Vincent',
          'America/Swift_Current',
          'America/Tegucigalpa',
          'America/Thule',
          'America/Thunder_Bay',
          'America/Tijuana',
          'America/Toronto',
          'America/Tortola',
          'America/Vancouver',
          'America/Virgin',
          'America/Whitehorse',
          'America/Winnipeg',
          'America/Yakutat',
          'America/Yellowknife',
          'Antarctica/Casey',
          'Antarctica/Davis',
          'Antarctica/DumontDUrville',
          'Antarctica/Macquarie',
          'Antarctica/Mawson',
          'Antarctica/McMurdo',
          'Antarctica/Palmer',
          'Antarctica/Rothera',
          'Antarctica/South_Pole',
          'Antarctica/Syowa',
          'Antarctica/Troll',
          'Antarctica/Vostok',
          'Arctic/Longyearbyen',
          'Asia/Aden',
          'Asia/Almaty',
          'Asia/Amman',
          'Asia/Anadyr',
          'Asia/Aqtau',
          'Asia/Aqtobe',
          'Asia/Ashgabat',
          'Asia/Ashkhabad',
          'Asia/Baghdad',
          'Asia/Bahrain',
          'Asia/Baku',
          'Asia/Bangkok',
          'Asia/Barnaul',
          'Asia/Beirut',
          'Asia/Bishkek',
          'Asia/Brunei',
          'Asia/Calcutta',
          'Asia/Chita',
          'Asia/Choibalsan',
          'Asia/Chongqing',
          'Asia/Chungking',
          'Asia/Colombo',
          'Asia/Dacca',
          'Asia/Damascus',
          'Asia/Dhaka',
          'Asia/Dili',
          'Asia/Dubai',
          'Asia/Dushanbe',
          'Asia/Gaza',
          'Asia/Harbin',
          'Asia/Hebron',
          'Asia/Ho_Chi_Minh',
          'Asia/Hong_Kong',
          'Asia/Hovd',
          'Asia/Irkutsk',
          'Asia/Istanbul',
          'Asia/Jakarta',
          'Asia/Jayapura',
          'Asia/Jerusalem',
          'Asia/Kabul',
          'Asia/Kamchatka',
          'Asia/Karachi',
          'Asia/Kashgar',
          'Asia/Kathmandu',
          'Asia/Katmandu',
          'Asia/Khandyga',
          'Asia/Kolkata',
          'Asia/Krasnoyarsk',
          'Asia/Kuala_Lumpur',
          'Asia/Kuching',
          'Asia/Kuwait',
          'Asia/Macao',
          'Asia/Macau',
          'Asia/Magadan',
          'Asia/Makassar',
          'Asia/Manila',
          'Asia/Muscat',
          'Asia/Nicosia',
          'Asia/Novokuznetsk',
          'Asia/Novosibirsk',
          'Asia/Omsk',
          'Asia/Oral',
          'Asia/Phnom_Penh',
          'Asia/Pontianak',
          'Asia/Pyongyang',
          'Asia/Qatar',
          'Asia/Qyzylorda',
          'Asia/Rangoon',
          'Asia/Riyadh',
          'Asia/Saigon',
          'Asia/Sakhalin',
          'Asia/Samarkand',
          'Asia/Seoul',
          'Asia/Shanghai',
          'Asia/Singapore',
          'Asia/Srednekolymsk',
          'Asia/Taipei',
          'Asia/Tashkent',
          'Asia/Tbilisi',
          'Asia/Tehran',
          'Asia/Tel_Aviv',
          'Asia/Thimbu',
          'Asia/Thimphu',
          'Asia/Tokyo',
          'Asia/Tomsk',
          'Asia/Ujung_Pandang',
          'Asia/Ulaanbaatar',
          'Asia/Ulan_Bator',
          'Asia/Urumqi',
          'Asia/Ust-Nera',
          'Asia/Vientiane',
          'Asia/Vladivostok',
          'Asia/Yakutsk',
          'Asia/Yekaterinburg',
          'Asia/Yerevan',
          'Atlantic/Azores',
          'Atlantic/Bermuda',
          'Atlantic/Canary',
          'Atlantic/Cape_Verde',
          'Atlantic/Faeroe',
          'Atlantic/Faroe',
          'Atlantic/Jan_Mayen',
          'Atlantic/Madeira',
          'Atlantic/Reykjavik',
          'Atlantic/South_Georgia',
          'Atlantic/St_Helena',
          'Atlantic/Stanley',
          'Australia/ACT',
          'Australia/Adelaide',
          'Australia/Brisbane',
          'Australia/Broken_Hill',
          'Australia/Canberra',
          'Australia/Currie',
          'Australia/Darwin',
          'Australia/Eucla',
          'Australia/Hobart',
          'Australia/LHI',
          'Australia/Lindeman',
          'Australia/Lord_Howe',
          'Australia/Melbourne',
          'Australia/North',
          'Australia/NSW',
          'Australia/Perth',
          'Australia/Queensland',
          'Australia/South',
          'Australia/Sydney',
          'Australia/Tasmania',
          'Australia/Victoria',
          'Australia/West',
          'Australia/Yancowinna',
          'Brazil/Acre',
          'Brazil/DeNoronha',
          'Brazil/East',
          'Brazil/West',
          'Canada/Atlantic',
          'Canada/Central',
          'Canada/Eastern',
          'Canada/East-Saskatchewan',
          'Canada/Mountain',
          'Canada/Newfoundland',
          'Canada/Pacific',
          'Canada/Saskatchewan',
          'Canada/Yukon',
          'CET',
          'Chile/Continental',
          'Chile/EasterIsland',
          'CST6CDT',
          'Cuba',
          'EET',
          'Egypt',
          'Eire',
          'EST',
          'EST5EDT',
          'Etc/GMT',
          'Etc/GMT+0',
          'Etc/GMT+1',
          'Etc/GMT+10',
          'Etc/GMT+11',
          'Etc/GMT+12',
          'Etc/GMT+2',
          'Etc/GMT+3',
          'Etc/GMT+4',
          'Etc/GMT+5',
          'Etc/GMT+6',
          'Etc/GMT+7',
          'Etc/GMT+8',
          'Etc/GMT+9',
          'Etc/GMT0',
          'Etc/GMT-0',
          'Etc/GMT-1',
          'Etc/GMT-10',
          'Etc/GMT-11',
          'Etc/GMT-12',
          'Etc/GMT-13',
          'Etc/GMT-14',
          'Etc/GMT-2',
          'Etc/GMT-3',
          'Etc/GMT-4',
          'Etc/GMT-5',
          'Etc/GMT-6',
          'Etc/GMT-7',
          'Etc/GMT-8',
          'Etc/GMT-9',
          'Etc/Greenwich',
          'Etc/UCT',
          'Etc/Universal',
          'Etc/UTC',
          'Etc/Zulu',
          'Europe/Amsterdam',
          'Europe/Andorra',
          'Europe/Astrakhan',
          'Europe/Athens',
          'Europe/Belfast',
          'Europe/Belgrade',
          'Europe/Berlin',
          'Europe/Bratislava',
          'Europe/Brussels',
          'Europe/Bucharest',
          'Europe/Budapest',
          'Europe/Busingen',
          'Europe/Chisinau',
          'Europe/Copenhagen',
          'Europe/Dublin',
          'Europe/Gibraltar',
          'Europe/Guernsey',
          'Europe/Helsinki',
          'Europe/Isle_of_Man',
          'Europe/Istanbul',
          'Europe/Jersey',
          'Europe/Kaliningrad',
          'Europe/Kiev',
          'Europe/Kirov',
          'Europe/Lisbon',
          'Europe/Ljubljana',
          'Europe/London',
          'Europe/Luxembourg',
          'Europe/Madrid',
          'Europe/Malta',
          'Europe/Mariehamn',
          'Europe/Minsk',
          'Europe/Monaco',
          'Europe/Moscow',
          'Europe/Nicosia',
          'Europe/Oslo',
          'Europe/Paris',
          'Europe/Podgorica',
          'Europe/Prague',
          'Europe/Riga',
          'Europe/Rome',
          'Europe/Samara',
          'Europe/San_Marino',
          'Europe/Sarajevo',
          'Europe/Simferopol',
          'Europe/Skopje',
          'Europe/Sofia',
          'Europe/Stockholm',
          'Europe/Tallinn',
          'Europe/Tirane',
          'Europe/Tiraspol',
          'Europe/Ulyanovsk',
          'Europe/Uzhgorod',
          'Europe/Vaduz',
          'Europe/Vatican',
          'Europe/Vienna',
          'Europe/Vilnius',
          'Europe/Volgograd',
          'Europe/Warsaw',
          'Europe/Zagreb',
          'Europe/Zaporozhye',
          'Europe/Zurich',
          'GB',
          'GB-Eire',
          'GMT',
          'GMT+0',
          'GMT0',
          'GMT-0',
          'Greenwich',
          'Hongkong',
          'HST',
          'Iceland',
          'Indian/Antananarivo',
          'Indian/Chagos',
          'Indian/Christmas',
          'Indian/Cocos',
          'Indian/Comoro',
          'Indian/Kerguelen',
          'Indian/Mahe',
          'Indian/Maldives',
          'Indian/Mauritius',
          'Indian/Mayotte',
          'Indian/Reunion',
          'Iran',
          'Israel',
          'Jamaica',
          'Japan',
          'Kwajalein',
          'Libya',
          'MET',
          'Mexico/BajaNorte',
          'Mexico/BajaSur',
          'Mexico/General',
          'MST',
          'MST7MDT',
          'Navajo',
          'NZ',
          'NZ-CHAT',
          'Pacific/Apia',
          'Pacific/Auckland',
          'Pacific/Bougainville',
          'Pacific/Chatham',
          'Pacific/Chuuk',
          'Pacific/Easter',
          'Pacific/Efate',
          'Pacific/Enderbury',
          'Pacific/Fakaofo',
          'Pacific/Fiji',
          'Pacific/Funafuti',
          'Pacific/Galapagos',
          'Pacific/Gambier',
          'Pacific/Guadalcanal',
          'Pacific/Guam',
          'Pacific/Honolulu',
          'Pacific/Johnston',
          'Pacific/Kiritimati',
          'Pacific/Kosrae',
          'Pacific/Kwajalein',
          'Pacific/Majuro',
          'Pacific/Marquesas',
          'Pacific/Midway',
          'Pacific/Nauru',
          'Pacific/Niue',
          'Pacific/Norfolk',
          'Pacific/Noumea',
          'Pacific/Pago_Pago',
          'Pacific/Palau',
          'Pacific/Pitcairn',
          'Pacific/Pohnpei',
          'Pacific/Ponape',
          'Pacific/Port_Moresby',
          'Pacific/Rarotonga',
          'Pacific/Saipan',
          'Pacific/Samoa',
          'Pacific/Tahiti',
          'Pacific/Tarawa',
          'Pacific/Tongatapu',
          'Pacific/Truk',
          'Pacific/Wake',
          'Pacific/Wallis',
          'Pacific/Yap',
          'Poland',
          'Portugal',
          'PRC',
          'PST8PDT',
          'ROC',
          'ROK',
          'Singapore',
          'Turkey',
          'UCT',
          'Universal',
          'US/Alaska',
          'US/Aleutian',
          'US/Arizona',
          'US/Central',
          'US/Eastern',
          'US/East-Indiana',
          'US/Hawaii',
          'US/Indiana-Starke',
          'US/Michigan',
          'US/Mountain',
          'US/Pacific',
          'US/Pacific-New',
          'US/Samoa',
          'UTC',
          'WET',
          'W-SU',
          'Zulu'
          ]

base_url = 'https://dashboard.meraki.com/api/v0'


class Error(Exception):
    #
    # Base module exception.
    #
    pass


class ListLengthWarn(Warning):
    #
    # Thrown when zip list lengths mismatch
    #
    pass


class OrgPermissionError(Error):
    #
    # Thrown when supplied API Key does not have access to supplied Organization ID
    #
    def __init__(self):
        self.default = 'Invalid Organization ID - Current API Key does not have access to this Organization'

    def __str__(self):
        return repr(self.default)


class EmailFormatError(Error):
    #
    # #Thrown when incorrect email format has been entered
    #
    def __init__(self):
        self.default = 'Incorrect E-mail Address Format Entered - Must be in the format name@domain.dom'

    def __str__(self):
        return repr(self.default)


class ListError(Error):
    #
    # Raised when empty list is passed when required
    #
    def __init__(self, message):
        self.message = message


def __isjson(myjson):
    #
    # Validates if passed object is valid JSON, used to prevent json.loads exceptions
    #
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


def __comparelist(*args):
    #
    # Compare length of multiple list arguments passed to function and exception if any are none and warn if any are
    # different in length the first list passed
    #
    length = len(args[0])
    if any(lst is None for lst in args):
        raise ListError('Empty list passed to function')
    if any(len(lst) != length for lst in args):
        warnings.warn('All lists are not of equal length', ListLengthWarn)


def __hasorgaccess(apikey, targetorg):
    #
    # Validate if API Key has access to passed Organization ID
    #
    geturl = '{0}/organizations'.format(str(base_url))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    dashboard = requests.get(geturl, headers=headers)
    currentorgs = json.loads(dashboard.text)
    orgs = []
    validjson = __isjson(dashboard.text)
    if validjson is True:
        for org in currentorgs:
            if int(org['id']) == int(targetorg):
                orgs.append(org['id'])
                return None
            else:
                pass
        raise OrgPermissionError


def __validemail(emailaddress):
    #
    # Validate email address format
    #
    if not re.match(r"[^@]+@[^@]+\.[^@]+", emailaddress):
        raise EmailFormatError


def __validip(ip):
    #
    # Validate IP format
    #
    try:
        ip_address(ip)
    except ValueError:
        raise ValueError('Invalid IP Address')


def __validsubnetip(subnetip):
    #
    # Validate correct subnet entry
    #
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[/]\d{1,2}$", subnetip):
        raise ValueError('Invalid Subnet IP Address {0} - Address must be formatted as #.#.#.#/#'.format(str(subnetip)))
    else:
        ip, netmask = str.split(subnetip, '/')

    if int(netmask) < 1 or int(netmask) > 30:
        raise ValueError('Invalid Subnet Mask Length {0} - Must be between 1 and 30'.format(str(subnetip)))
    try:
        ip_address(ip)
    except ValueError:
        raise ValueError('Invalid Subnet IP Address {0}'.format(str(subnetip)))


def __returnhandler(statuscode, returntext, objtype):
    #
    # Parses Dashboard return information and returns error data based on status code and error JSON
    #

    validreturn = __isjson(returntext)
    noerr = False
    errmesg = ''

    if validreturn:
        returntext = json.loads(returntext)

        try:
            errmesg = returntext['errors']
        except KeyError:
            noerr = True
        except TypeError:
            noerr = True

    if str(statuscode) == '200' and validreturn:
        print('{0} Operation Successful - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '200':
        print('{0} Operation Successful\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '201' and validreturn:
        print('{0} Added Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '201':
        print('{0} Added Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '204' and validreturn:
        print('{0} Deleted Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '204':
        print('{0} Deleted Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '400' and validreturn and noerr is False:
        print('Bad Request - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '400' and validreturn and noerr:
        print('Bad Request - See returned data for details\n')
        return returntext
    elif str(statuscode) == '400':
        print('Bad Request - No additional error data available\n')
    elif str(statuscode) == '401' and validreturn and noerr is False:
        print('Unauthorized Access - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '401' and validreturn:
        print('Unauthorized Access')
        return returntext
    elif validreturn and noerr is False:
        print('HTTP Status Code: {0} - See returned data for error details\n'.format(str(statuscode)))
        return errmesg
    else:
        print('HTTP Status Code: {0} - No returned data\n'.format(str(statuscode)))


def myorgaccess(apikey):
    #
    # Query Dashboard for OrgID's that API key has access to
    #
    calltype = 'Organization'
    geturl = '{0}/organizations'.format(str(base_url))
    headers = {
        'X-Cisco-Meraki-API-Key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getorginventory(apikey, organizationid):
    #
    # Pull organization inventory and return decoded JSON string
    #
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Inventory'

    geturl = '{0}/organizations/{1}/inventory'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getnetworkdevices(apikey, networkid):
    #
    # Get network inventory and return as decoded JSON string
    #
    calltype = 'Network'
    geturl = '{0}/networks/{1}/devices'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getorgadmins(apikey, organizationid):
    #
    # Get administrators for organization and return decoded JSON string
    #
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Organization'

    geturl = '{0}/organizations/{1}/admins'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getnetworklist(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Network'

    geturl = '{0}/organizations/{1}/networks'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getlicensestate(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'License'

    geturl = '{0}/organizations/{1}/licenseState'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getdevicedetail(apikey, networkid, serialnumber):

    calltype = 'Device Detail'
    geturl = '{0}/networks/{1}/devices/{2}'.format(str(base_url), str(networkid), str(serialnumber))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getnetworkdetail(apikey, networkid):

    calltype = 'Network Detail'
    geturl = '{0}/networks/{1}'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getnonmerakivpnpeers(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'None-Meraki VPN Peer'

    geturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getsnmpsettings(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'SNMP Settings'

    geturl = '{0}/organizations/{1}/snmp'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getsamlroles(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'SAML Roles'

    geturl = '{0}/organizations/{1}/samlRoles'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getswitchstacks(apikey, networkid):
    calltype = 'Switch Stacks'
    geturl = '{0}/networks/{1}/switchStacks'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getswitchstackmembers(apikey, networkid, stackid):
    calltype = 'Switch Stack Members'
    geturl = '{0}/networks/{1}/switchStacks/{2}'.format(str(base_url), str(networkid), str(stackid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getvlans(apikey, networkid):
    calltype = 'VLANs'
    geturl = '{0}/networks/{1}/vlans'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getvlandetail(apikey, networkid, vlanid):
    calltype = 'VLAN Detail'
    geturl = '{0}/networks/{1}/vlans/{2}'.format(str(base_url), str(networkid), str(vlanid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def gettemplates(apikey, organizationid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Templates'

    geturl = '{0}/organizations/{1}/configTemplates'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getclients(apikey, serialnum):
    calltype = 'Clients'
    geturl = '{0}/devices/{1}/clients'.format(str(base_url), str(serialnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def bindtotemplate(apikey, networkid, templateid, autobind='false'):
    calltype = 'Template Bind'
    posturl = '{0}/networks/{1}/bind'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = {
        'configTemplateId': format(str(templateid)),
        'autobind': format(str(autobind))
    }
    dashboard = requests.post(posturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def adddevtonet(apikey, networkid, serial):
    calltype = 'Assign Device'
    posturl = '{0}/networks/{1}/devices/claim'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    postdata = {
        'serial': format(str(serial))
    }
    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def unbindfromtemplate(apikey, networkid):
    calltype = 'Network Unbind'
    posturl = '{0}/networks/{1}/unbind'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.post(posturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def deltemplate(apikey, organizationid, templateid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Template Delete'

    delurl = '{0}/organizations/{1}/configTemplates/{2}'.format(str(base_url), str(organizationid), str(templateid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def updatevlan(apikey, networkid, vlanid, vlanname=None, mxip=None, subnetip=None):
    calltype = 'VLAN Update'
    puturl = '{0}/networks/{1}/vlans/{2}'.format(str(base_url), str(networkid), str(vlanid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = {}
    if vlanname is not None:
        putdata['name'] = format(str(vlanname))
    if mxip is not None:
        putdata['applianceIp'] = format(str(mxip))
    if subnetip is not None:
        putdata['subnet'] = format(str(subnetip))

    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def addvlan(apikey, networkid, vlanid, vlanname, mxip, subnetip):
    calltype = 'VLAN Add'
    posturl = '{0}/networks/{1}/vlans'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    postdata = {
        'id': format(str(vlanid)),
        'name': format(str(vlanname)),
        'applianceIp': format(str(mxip)),
        'subnet': format(str(subnetip))
    }
    postdata = json.dumps(postdata)
    dashboard = requests.post(posturl, data=postdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def delvlan(apikey, networkid, vlanid):
    calltype = 'VLAN Delete'
    delurl = '{0}/networks/{1}/vlans/{2}'.format(str(base_url), str(networkid), str(vlanid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def addadmin(apikey, organizationid, email, name, orgaccess=None, tags=None, tagaccess=None, networks=None,
             netaccess=None):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Add Administrator'

    posturl = '{0}/organizations/{1}/admins'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    posttags = []

    if orgaccess is None and tags is None and networks is None:
        print("Administrator accounts must be granted access to either the Organization, Networks, or Tags")
        return None

    if tags is not None and tagaccess is None:
        print("If tags are defined you must define matching access arguments.\nFor example, tags = ['tag1', 'tag2'], "
              "must have matching access arguments: tagaccess = 'full', 'read-only'")
        return None
    elif tagaccess is not None and tags is None:
        print("If tag access levels are defined you must define matching tag arguments\nFor example, tags = "
              "['tag1', 'tag2'] must have matching access arguments: tagaccess = 'full', 'read-only'")
        return None
    elif tagaccess is None and tags is None:
        pass
    elif len(tags) != len(tagaccess):
        print("The number of tags and access arguments must match.\n")
        print("For example, tags = ['tag1', 'tag2'] must have matching access arguments: tagaccess = "
              "['full', 'read-only']")
        return None
    elif tags is not None and tagaccess is not None:
        x = 0
        while x < len(tags):
            posttags.append({'tag': tags[x], 'access': tagaccess[x]})
            x += 1
    else:
        pass

    postnets = []

    if networks is not None and netaccess is None:
        print("If networks are defined you must define matching access arguments\nFor example networks = "
              "['net1', 'net2'] must have matching access arguments: netaccess = 'full', 'read-only'")
        return None
    elif netaccess is not None and networks is None:
        print("If network access levels are defined you must define matching network arguments\nFor example, networks"
              " = ['net1', 'net2'] must have matching access arguments: netaccess = 'full', 'read-only'")
        return None
    elif netaccess is None and networks is None:
        pass
    elif len(networks) != len(netaccess):
        print("The number of networks and access arguments must match.\n")
        print("For example, networks = ['net1', 'net2'] must have matching access arguments: netaccess = "
              "['full', 'read-only']")
        return None
    elif networks is not None and netaccess is not None:
        x = 0
        while x < len(networks):
            postnets.append({'id': networks[x], 'access': netaccess[x]})
            x += 1
    else:
        pass
    postdata = []
    if len(posttags) == 0 and len(postnets) == 0:
        postdata = {
            'orgAccess': orgaccess,
            'email': format(str(email)),
            'name': format(str(name))
        }

    elif len(posttags) > 0 and len(postnets) == 0:
        postdata = {
            'name': format(str(name)),
            'email': format(str(email)),
            'orgAccess': orgaccess,
            'tags': posttags
        }

    elif len(postnets) > 0 and len(posttags) == 0:
        postdata = {
            'name': format(str(name)),
            'email': format(str(email)),
            'orgAccess': orgaccess,
            'networks': postnets
        }

    elif len(postnets) > 0 and len(posttags) > 0:
        postdata = {
            'name': format(str(name)),
            'email': format(str(email)),
            'orgAccess': orgaccess,
            'tags': posttags,
            'networks': postnets
        }
    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def deladmin(apikey, organizationid, adminid):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Delete Administrator'

    delurl = '{0}/organizations/{1}/admins/{2}'.format(str(base_url), str(organizationid), str(adminid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def addnetwork(apikey, organizationid, name, nettype, tags, tz):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Add Network'

    posturl = '{0}/organizations/{1}/networks'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    validtz = False
    for zone in tzlist:
        if validtz is False and format(str(tz)) == zone:
            validtz = True
            break
        else:
            validtz = False

    if validtz is False:
        print('Please enter a valid tz value from https://en.wikipedia.org/wiki/List_of_tz_database_time_zones')
        return None

    postdata = {
        'name': format(str(name)),
        'type': format(str(nettype)),
        'tags': format(str(tags)),
        'timeZone': format(str(tz))
    }
    postdata = json.dumps(postdata)
    dashboard = requests.post(posturl, data=postdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def delnetwork(apikey, networkid):
    calltype = 'Delete Network'
    delurl = '{0}/networks/{1}'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def updateadmin(apikey, organizationid, adminid, email, name=None, orgaccess=None, tags=None, tagaccess=None,
                networks=None, netaccess=None):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Update Administrator'

    puturl = '{0}/organizations/{1}/admins/{2}'.format(str(base_url), str(organizationid), str(adminid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
        }

    puttags = []

    if orgaccess is None and tags is None and networks is None and name is None:
        print("Administrator account updates must include Organization, Networks, or Tags permission changes or an "
              "updated name attribute")
        return None

    if tags is not None and tagaccess is None:
        print("If tags are defined you must define matching access arguments.\nFor example, tags = ['tag1', 'tag2'], "
              "must have matching access arguments: tagaccess = 'full', 'read-only'")
        return None
    elif tagaccess is not None and tags is None:
        print("If tag access levels are defined you must define matching tag arguments\nFor example, tags = "
              "['tag1', 'tag2'] must have matching access arguments: tagaccess = 'full', 'read-only'")
        return None
    elif tagaccess is None and tags is None:
        pass
    elif len(tags) != len(tagaccess):
        print("The number of tags and access arguments must match.\n")
        print("For example, tags = ['tag1', 'tag2'] must have matching access arguments: tagaccess = "
              "['full', 'read-only']")
        return None
    elif tags is not None and tagaccess is not None:
        x = 0
        while x < len(tags):
            puttags.append({'tag': tags[x], 'access': tagaccess[x]})
            x += 1
    else:
        pass

    putnets = []

    if networks is not None and netaccess is None:
        print("If networks are defined you must define matching access arguments\nFor example networks = "
              "['net1', 'net2'] must have matching access arguments: netaccess = 'full', 'read-only'")
        return None
    elif netaccess is not None and networks is None:
        print("If network access levels are defined you must define matching network arguments\nFor example, networks"
              " = ['net1', 'net2'] must have matching access arguments: netaccess = 'full', 'read-only'")
        return None
    elif netaccess is None and networks is None:
        pass
    elif len(networks) != len(netaccess):
        print("The number of networks and access arguments must match.\n")
        print("For example, networks = ['net1', 'net2'] must have matching access arguments: netaccess = "
              "['full', 'read-only']")
        return None
    elif networks is not None and netaccess is not None:
        x = 0
        while x < len(networks):
            putnets.append({'id': networks[x], 'access': netaccess[x]})
            x += 1
    else:
        pass
    putdata = []

    if name is not None:
        if len(puttags) == 0 and len(putnets) == 0:
            putdata = {
                'orgAccess': orgaccess,
                'email': format(str(email)),
                'name': format(str(name))
            }

        elif len(puttags) > 0 and len(putnets) == 0:
            putdata = {
                'name': format(str(name)),
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'tags': puttags
                }

        elif len(putnets) > 0 and len(puttags) == 0:
            putdata = {
                'name': format(str(name)),
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'networks': putnets
                }

        elif len(putnets) > 0 and len(puttags) > 0:
            putdata = {
                'name': format(str(name)),
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'tags': puttags,
                'networks': putnets
                }

    elif name is None:
        if len(puttags) > 0 and len(putnets) == 0:
            putdata = {
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'tags': puttags
                }

        elif len(putnets) > 0 and len(puttags) == 0:
            putdata = {
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'networks': putnets
                }

        elif len(putnets) > 0 and len(puttags) > 0:
            putdata = {
                'email': format(str(email)),
                'orgAccess': orgaccess,
                'tags': puttags,
                'networks': putnets
                }

    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def getvpnsettings(apikey, networkid):
    calltype = 'Get AutoVPN Settings'
    geturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def updatevpnsettings(apikey, networkid, mode='None', subnets=None, usevpn=None, hubnetworks=None, defaultroute=None):
    calltype = 'Update AutoVPN Settings'
    puturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    __comparelist(hubnetworks, defaultroute, 'hubnetworks', 'defaultroute', True, True)
    if hubnetworks is not None and defaultroute is not None:
        hubmodes = zip(hubnetworks, defaultroute)
    else:
        hubmodes = []

    __comparelist(subnets, usevpn)
    vpnsubnets = list(zip(subnets, usevpn))

    hubs = []
    for h, d in hubmodes:
        hubs.append({'hubId': h, 'useDefaultRoute': d})

    subnets = []
    for s, i in vpnsubnets:
        __validsubnetip(s)
        subnets.append({'localSubnet': s, 'useVpn': i})

    putdata = {'mode': mode, 'hubs': hubs, 'subnets': subnets}
    print(putdata)

    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result


def updatenonmerakivpn(apikey, organizationid, names, ips, secrets, remotenets, tags=None):
    #
    # Function to update non-Meraki VPN peer information for an organization.  This function will desctructively
    # overwrite ALL existing peer information.  If you only wish to add/update an existing peer you must download
    # all current peer information and make re-upload the modified array of all peers
    #

    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, organizationid)
    calltype = 'Update Non-Meraki VPN Peers'

    puturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(organizationid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    #
    # Will only upload peer information if lists are passed to the function, otherwise will fail.  If tags argument is
    # None will assume all peers should be available to all networks.
    #

    if isinstance(names, list) and isinstance(ips, list) and isinstance(secrets, list)\
            and isinstance(remotenets, list) and (tags is None or isinstance(tags, list)):
        if len(names) + len(ips) + len(secrets) + len(remotenets) / 4 != len(names):
            warnings.warn('Peers will be added up to the length of the shortest list passed', ListLengthWarn)
        if tags is None:
            tags = []
            for x in names:
                tags.append(['all'])
        for n in remotenets:
            if isinstance(n, list):
                for sn in n:
                    __validsubnetip(sn)
            else:
                __validsubnetip(n)
        peerlist = list(zip(names, ips, secrets, remotenets, tags))
        putdata = []
        peer = {}
        for n, i, s, r, t in peerlist:
            peer['name'] = n
            peer['publicIp'] = i
            peer['privateSubnets'] = r
            peer['secret'] = s
            peer['tags'] = t
            putdata.append((peer.copy()))
            peer.clear()
    else:
        raise TypeError('All peer arguments must be passed as lists, tags argument may be excluded')

    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype)
    return result

