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
from __future__ import print_function
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


class IgnoredArgument(Warning):
    #
    # Thrown when argument will be ignored
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


class DashboardObject(object):
    #
    # Base Dashboard object
    #
    pass


class SSID(DashboardObject):

    #  SSID Object Class
    #  Refer to https://dashboard.meraki.com/manage/support/api_docs#ssids for details on accepted parameters
    #
    #  Provides a simplified object for downloading and manipulating SSID Attributes from Dashboard

    validparams = ['name', 'enabled', 'authMode', 'encryptionMode', 'psk', 'radiusServers', 'radiusAccountingEnabled',
                   'radiusAccountingServers', 'ipAssignmentMode', 'useVlanTagging', 'concentratorNetworkId', 'vlanID',
                   'defaultVlanId', 'apTagsAndVlanIds', 'walledGardenEnabled', 'walledGardenRanges', 'splashPage',
                   'perClientBandwidthLimitUp', 'perClientBandwidthLimitDown']
    type = 'ssid'

    def __init__(self, ssidnum, **params):

        self.__setattr__('ssidnum', ssidnum)

        for p in params.keys():
            if p in self.validparams:
                self.__setattr__(p, params[p])
            else:
                raise ValueError('Invalid parameter {0}, please refer to https://dashboard.meraki.com/manage/support/'
                                 'api_docs#ssids for valid parameters'.format(str(p)))



def __isjson(myjson):
    #
    # Validates if passed object is valid JSON, used to prevent json.loads exceptions
    #
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


def __isvalidtz(tz):
    #
    # Validates if TZ exists in accepted TZ list
    #
    validtz = False

    for zone in tzlist:
        if validtz is False and format(str(tz)) == zone:
            validtz = True
            break
        else:
            validtz = False

    if validtz is False:
        raise ValueError(
            'Please enter a valid tz value from https://en.wikipedia.org/wiki/List_of_tz_database_time_zones')

    return None


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
        return 2
    else:
        return 0


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
    return None


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


def __listtotag(taglist):
    #
    # Converts list variable to space separated string for API pass to Dashboard
    #

    liststr = '  '

    if not isinstance(taglist, list):
        taglist = list(taglist)

    for t in taglist:
        liststr = liststr + t + '  '

    return liststr


def __returnhandler(statuscode, returntext, objtype, suppressprint):
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
        if suppressprint is False:
            print('{0} Operation Successful - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '200':
        if suppressprint is False:
            print('{0} Operation Successful\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '201' and validreturn:
        if suppressprint is False:
            print('{0} Added Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '201':
        if suppressprint is False:
            print('{0} Added Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '204' and validreturn:
        if suppressprint is False:
            print('{0} Deleted Successfully - See returned data for results\n'.format(str(objtype)))
        return returntext
    elif str(statuscode) == '204':
        print('{0} Deleted Successfully\n'.format(str(objtype)))
        return None
    elif str(statuscode) == '400' and validreturn and noerr is False:
        if suppressprint is False:
            print('Bad Request - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '400' and validreturn and noerr:
        if suppressprint is False:
            print('Bad Request - See returned data for details\n')
        return returntext
    elif str(statuscode) == '400':
        if suppressprint is False:
            print('Bad Request - No additional error data available\n')
    elif str(statuscode) == '401' and validreturn and noerr is False:
        if suppressprint is False:
            print('Unauthorized Access - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '401' and validreturn:
        if suppressprint is False:
            print('Unauthorized Access')
        return returntext
    elif str(statuscode) == '404' and validreturn and noerr is False:
        if suppressprint is False:
            print('Resource Not Found - See returned data for error details\n')
        return errmesg
    elif str(statuscode) == '404' and validreturn:
        if suppressprint is False:
            print('Resource Not Found')
        return returntext
    elif str(statuscode) == '500':
        if suppressprint is False:
            print('HTTP 500 - Server Error')
        return returntext
    elif validreturn and noerr is False:
        if suppressprint is False:
            print('HTTP Status Code: {0} - See returned data for error details\n'.format(str(statuscode)))
        return errmesg
    else:
        print('HTTP Status Code: {0} - No returned data\n'.format(str(statuscode)))


def myorgaccess(apikey, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getorg(apikey, orgid, suppressprint=False):
    calltype = 'Organization'
    geturl = '{0}/organizations/{1}'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getorginventory(apikey, orgid, suppressprint=False):
    #
    # Pull organization inventory and return decoded JSON string
    #
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Inventory'

    geturl = '{0}/organizations/{1}/inventory'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnetworkdevices(apikey, networkid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getorgadmins(apikey, orgid, suppressprint=False):
    #
    # Get administrators for organization and return decoded JSON string
    #
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Organization'

    geturl = '{0}/organizations/{1}/admins'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnetworklist(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Network'

    geturl = '{0}/organizations/{1}/networks'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getlicensestate(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'License'

    geturl = '{0}/organizations/{1}/licenseState'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getdevicedetail(apikey, networkid, serialnumber, suppressprint=False):

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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnetworkdetail(apikey, networkid, suppressprint=False):

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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnetworktrafficstats(apikey, networkid, timespan=86400, devicetype='combined', suppressprint=False):

    calltype = 'Network Detail'
    geturl = '{0}/networks/{1}/traffic?timespan={2}&deviceType={3}'.format(str(base_url), str(networkid), str(timespan),
                                                                           str(devicetype))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnonmerakivpnpeers(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Non-Meraki VPN'

    geturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getsnmpsettings(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SNMP Settings'

    geturl = '{0}/organizations/{1}/snmp'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getsamlroles(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SAML Roles'

    geturl = '{0}/organizations/{1}/samlRoles'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getsamlroledetail(apikey, orgid, roleid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SAML Role Detail'

    geturl = '{0}/organizations/{1}/samlRoles/{2}'.format(str(base_url), str(orgid), str(roleid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getswitchstacks(apikey, networkid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getswitchstackmembers(apikey, networkid, stackid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getswitchports(apikey, serialnum, suppressprint=False):
    calltype = 'Switch Port'
    geturl = '{0}/devices/{1}/switchPorts'.format(str(base_url), str(serialnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getswitchportdetail(apikey, serialnum, portnum, suppressprint=False):
    calltype = 'Switch Port Detail'
    geturl = '{0}/devices/{1}/switchPorts/{2}'.format(str(base_url), str(serialnum), str(portnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getssids(apikey, networkid, suppressprint=False):
    calltype = 'SSID'
    geturl = '{0}/networks/{1}/ssids'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getssiddetail(apikey, networkid, ssidnum, suppressprint=False):
    calltype = 'SSID Detail'
    geturl = '{0}/networks/{1}/ssids/{2}'.format(str(base_url), str(networkid), str(ssidnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getvlans(apikey, networkid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getvlandetail(apikey, networkid, vlanid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def gettemplates(apikey, orgid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Templates'

    geturl = '{0}/organizations/{1}/configTemplates'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getclients(apikey, serialnum, timestamp=86400, suppressprint=False):
    calltype = 'Device Clients'
    geturl = '{0}/devices/{1}/clients?timespan={2}'.format(str(base_url), str(serialnum), str(timestamp))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def bindtotemplate(apikey, networkid, templateid, autobind=False, suppressprint=False):
    calltype = 'Template Bind'
    posturl = '{0}/networks/{1}/bind'.format(str(base_url), str(networkid))
    postdata={}
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    postdata.update({'configTemplateId': format(str(templateid))})

    if autobind is not False:
        postdata['autoBind'] = autobind

    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def adddevtonet(apikey, networkid, serial, suppressprint=False):
    calltype = 'Device'
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def claim(apikey, orgid, serial=None, licensekey=None, licensemode=None, orderid=None, suppressprint=False):
    calltype = 'Claim'
    posturl = '{0}/organization/{1}/claim'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    x = 0
    postdata = {}
    for x in [serial, licensekey, orderid]:
        if x is None:
            pass
        else:
            x += 1
    if x > 1:
        raise AttributeError('Mutiple identifiers passed, please pass only one of either serial number, license key, '
                             'or order ID')
    if (licensekey is None and licensemode is not None) or (licensemode is None and licensekey is not None):
        raise AttributeError('If claiming a license key both license and licensemode attributes must be passed')

    if serial is not None:
        postdata['serial'] = serial
    elif licensekey is not None and licensemode is not None:
        postdata['license'] = serial
        postdata['licenseMode'] = serial
    elif orderid is not None:
        postdata['orderId'] = orderid

    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def unbindfromtemplate(apikey, networkid, suppressprint=False):
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def deltemplate(apikey, orgid, templateid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Template'

    delurl = '{0}/organizations/{1}/configTemplates/{2}'.format(str(base_url), str(orgid), str(templateid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def delsamlrole(apikey, orgid, roleid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SAML Role'

    delurl = '{0}/organizations/{1}/samlRoles/{2}'.format(str(base_url), str(orgid), str(roleid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatevlan(apikey, networkid, vlanid, vlanname=None, mxip=None, subnetip=None, suppressprint=False):
    calltype = 'VLAN'
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def addvlan(apikey, networkid, vlanid, vlanname, mxip, subnetip, suppressprint=False):
    calltype = 'VLAN'
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def delvlan(apikey, networkid, vlanid, suppressprint=False):
    calltype = 'VLAN'
    delurl = '{0}/networks/{1}/vlans/{2}'.format(str(base_url), str(networkid), str(vlanid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def addadmin(apikey, orgid, email, name, orgaccess=None, tags=None, tagaccess=None, networks=None,
             netaccess=None, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Administrator'

    posturl = '{0}/organizations/{1}/admins'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    posttags = []

    if orgaccess is None and tags is None and networks is None:
        print("Administrator accounts must be granted access to either an Organization, Networks, or Tags")
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def deladmin(apikey, orgid, adminid, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Administrator'

    delurl = '{0}/organizations/{1}/admins/{2}'.format(str(base_url), str(orgid), str(adminid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def addnetwork(apikey, orgid, name, nettype, tags, tz, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Network'

    posturl = '{0}/organizations/{1}/networks'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    __isvalidtz(tz)

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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def delnetwork(apikey, networkid, suppressprint=False):
    calltype = 'Network'
    delurl = '{0}/networks/{1}'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.delete(delurl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updateadmin(apikey, orgid, adminid, email, name=None, orgaccess=None, tags=None, tagaccess=None,
                networks=None, netaccess=None, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Administrator'

    puturl = '{0}/organizations/{1}/admins/{2}'.format(str(base_url), str(orgid), str(adminid))
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getvpnsettings(apikey, networkid, suppressprint=False):
    calltype = 'AutoVPN'
    geturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatevpnsettings(apikey, networkid, mode='None', subnets=None, usevpn=None, hubnetworks=None, defaultroute=None,
                      suppressprint=False):
    calltype = 'AutoVPN'
    puturl = '{0}/networks/{1}/siteToSiteVpn'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    __comparelist(hubnetworks, defaultroute)
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatenonmerakivpn(apikey, orgid, names, ips, secrets, remotenets, tags=None, suppressprint=False):
    #
    # Function to update non-Meraki VPN peer information for an organization.  This function will desctructively
    # overwrite ALL existing peer information.  If you only wish to add/update an existing peer you must download
    # all current peer information and make re-upload the modified array of all peers
    #

    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Non-Meraki VPN'

    puturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(orgid))
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
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def getnonmerakivpn(apikey, orgid, suppressprint=False):
    calltype = 'Non-Meraki VPN'
    geturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.get(geturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def appendnonmerakivpn(apikey, orgid, names, ips, secrets, remotenets, tags=None, suppressprint=False):
    #
    # Function to update non-Meraki VPN peer information for an organization.  This function will desctructively
    # overwrite ALL existing peer information.  If you only wish to add/update an existing peer you must download
    # all current peer information and make re-upload the modified array of all peers
    #

    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'Non-Meraki VPN'

    puturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(orgid))
    geturl = '{0}/organizations/{1}/thirdPartyVPNPeers'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    currentpeers = json.loads(requests.get(geturl, headers=headers).text)

    #
    # Will only upload peer information if lists are passed to the function, otherwise will fail.  If tags argument is
    # None will assume all peers should be available to all networks.
    #
    if any(isinstance(el, list) for el in remotenets) is False:
        remotenets = [remotenets]
        warnings.warn('Variable remotenets was not passed as list of lists, it has been converted', ListLengthWarn)

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
        for x in currentpeers:
            peer['name'] = x['name']
            peer['publicIp'] = x['publicIp']
            peer['privateSubnets'] = x['privateSubnets']
            peer['secret'] = x['secret']
            peer['tags'] = x['tags']
            putdata.append((peer.copy()))
            peer.clear()
    else:
        raise TypeError('All peer arguments must be passed as lists, tags argument may be excluded')
    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatesnmpsettings(apikey, orgid, v2c=False, v3=False, v3authmode='SHA', v3authpw=None, v3privmode='AES128',
                       v3privpw=None, allowedips=None, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SNMP'
    puturl = '{0}/organizations/{1}/snmp'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = {}

    if v3authmode not in ['SHA', 'MD5']:
        raise ValueError('Valid authentication modes are "SHA" or "MD5"')

    if v3privmode not in ['DES', 'AES128']:
        raise ValueError('Valid privacy modes are "DES" and "AES128"')
    if v3 and (v3authpw is None or v3privpw is None):
        raise ValueError('If SNMPv3 is enabled a authentication and privacy password must be provided')
    elif v3 and (len(v3authpw) < 8 or len(v3privpw) < 8):
        raise ValueError('Authentication and privacy passwords must be a minimum of 8 characters')
    elif v3:
        putdata['v3AuthMode'] = v3authmode
        putdata['v3AuthPass'] = v3authpw
        putdata['v3PrivMode'] = v3privmode
        putdata['v3PrivPass'] = v3privpw

    putdata['v2cEnabled'] = v2c
    putdata['v3Enabled'] = v3

    if allowedips is not None:
        if isinstance(allowedips, list):
            allowiplist = str(allowedips[0])
            __validip(allowiplist)
            if len(allowedips) > 1:
                for i in allowedips[1:]:
                    __validip(str(i))
                    allowiplist = allowiplist + ':' + i
        else:
            __validip(str(allowedips))
            allowiplist = str(allowedips)
        putdata['peerIps'] = allowiplist
    else:
        putdata['peerIps'] = None

    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def removedevfromnet(apikey, networkid, serial, suppressprint=False):
    calltype = 'Device'
    posturl = '{0}/networks/{1}/devices/{2}/remove'.format(str(base_url), str(networkid), str(serial))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    dashboard = requests.post(posturl, headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def addorg(apikey, neworgname, suppressprint=False):
    calltype = 'Organization'
    posturl = '{0}/organizations/'.format(str(base_url))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    postdata = {
        'name': format(str(neworgname))
    }
    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def cloneorg(apikey, orgid, neworgname, suppressprint=False):
    __hasorgaccess(apikey, orgid)
    calltype = 'Organization Clone'
    posturl = '{0}/organizations/{1}/clone'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    postdata = {
        'name': format(str(neworgname))
    }
    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def renameorg(apikey, orgid, neworgname, suppressprint=False):
    __hasorgaccess(apikey, orgid)
    calltype = 'Organization Rename'
    puturl = '{0}/organizations/{1}'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }
    putdata = {
        'name': format(str(neworgname))
    }
    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatenetwork(apikey, networkid, name, tz, tags, suppressprint=False):

    calltype = 'Network'
    puturl = '{0}/organizations/{1}'.format(str(base_url), str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}

    if name:
        putdata['name'] = name

    if tz:
        __isvalidtz(tz)
        putdata['timeZone'] = format(str(tz))

    if tags:
        putdata['tags'] = __listtotag(tags)

    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatedevice(apikey, networkid, sn, name, tags, lat, lng, address, suppressprint=False):

    calltype = 'Device'
    posturl = '{0}/networks/{1}/devices/{2}'.format(str(base_url), str(networkid), str(sn))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}

    if name:
        putdata['name'] = name

    if tags:
        putdata['tags'] = __listtotag(tags)

    if lat and not lng:
        raise ValueError('If latitude is entered a longitude value must also be entered')
    elif lng and not lat:
        raise ValueError('If longitude is entered a latitude value must also be entered')
    elif lat and lng:
        putdata['lat'] = lat
        putdata['lng'] = lng

    if address:
        putdata['address'] = address

    dashboard = requests.put(posturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatessid(apikey, networkid, ssidnum, name, enabled, authmode, encryptionmode, psk, suppressprint=False):

    calltype = 'SSID'
    puturl = '{0}/networks/{1}/ssids/{2}'.format(str(base_url), str(networkid), str(ssidnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}

    if name:
        putdata['name'] = str(name)

    if enabled and (enabled is not False or not True):
        raise ValueError("Enabled must be a boolean variable")
    else:
        putdata['enabled'] = str(enabled)

    if authmode not in ['psk', 'open']:
        raise ValueError("Authentication mode must be psk or open")
    elif authmode == 'psk' and (not encryptionmode or not psk):
        raise ValueError("If authentication mode is set to psk, encryption mode and psk must also be passed")
    elif authmode == 'open' and (encryptionmode or psk):
        warnings.warn(IgnoredArgument("If authentication mode is open, encryption mode and psk will be ignored"))
    elif authmode:
        putdata['authMode'] = str(authmode)

    if encryptionmode and (authmode is not 'psk' or not psk or not authmode):
        raise ValueError("If encryption mode is passed, authentication mode must be psk and psk must also be passed")
    elif encryptionmode:
        putdata['encryptionMode'] = str(encryptionmode)

    if psk and (authmode is not 'psk' or not encryptionmode or not authmode):
        raise ValueError("If psk is passed, authentication mode and encryption mode must also be passed")
    elif len(psk) < 8 and encryptionmode == 'wpa':
        raise ValueError("If encryption mode is wpa, the psk must be a minimum of 8 characters")
    elif psk:
        putdata['psk'] = str(psk)

    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updateswitchport(apikey, serialnum, portnum, name, tags, enabled, porttype, vlan, voicevlan, allowedvlans, poe,
                     isolation, rstp, stpguard, accesspolicynum, suppressprint=False):

    calltype = 'Switch Port'
    puturl = '{0}/devices/{1}/switchPorts/{2}'.format(str(base_url), str(serialnum), str(portnum))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {}

    if name:
        putdata['name'] = str(name)

    if tags:
        putdata['tags'] = __listtotag(tags)

    if enabled and (enabled is not False or not True):
        raise ValueError("Enabled must be a boolean variable")
    elif enabled:
        putdata['enabled'] = str(enabled)

    if porttype and porttype not in ['access', 'trunk']:
        raise ValueError("Type must be either 'access' or 'trunk'")
    elif porttype:
        putdata['type'] = str(porttype)

    if vlan:
        putdata['vlan'] = str(vlan)

    if voicevlan:
        putdata['voiceVlan'] = voicevlan

    if allowedvlans:
        putdata['allowedVlans'] = allowedvlans

    if poe and (poe is not False or not True):
        raise ValueError("PoE enabled must be a boolean variable")
    elif poe:
        putdata['poeEnabled'] = str(poe)

    if isolation and (isolation is not False or not True):
        raise ValueError("Port isolation enabled must be a bolean variable")
    elif isolation:
        putdata['isolation'] = isolation

    if rstp and (rstp is not False or not True):
        raise ValueError("RSTP enabled must be a boolean variable")
    elif rstp:
        putdata['rstpEnabled'] = rstp

    if stpguard and stpguard not in ['disabled', 'root guard', 'BPDU guard']:
        raise ValueError("Valid values for STP Guard are 'disabled', 'root guard',  or 'BPDU Guard'")
    elif stpguard:
        putdata['stpGuard'] = stpguard

    if accesspolicynum:
        putdata['accessPolicyNumber'] = accesspolicynum

    dashboard = requests.put(puturl, data=json.dumps(putdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def addsamlrole(apikey, orgid, rolename, orgaccess, tags, tagaccess, networks, netaccess, suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SAML Role'

    posturl = '{0}/organizations/{1}/samlRoles'.format(str(base_url), str(orgid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    if not orgaccess and not tags and not networks:
        raise AttributeError("At least one of organization access, tag based access, or network based access must be "
                             "defined")
    if orgaccess and orgaccess not in ['read-only', 'full', 'none']:
        raise ValueError("Organization access must be either 'read-only' or 'full' or 'none'")

    posttags = []

    taglist = False

    if (tags and not tagaccess) or (tagaccess and not tags):
        raise AttributeError("Both tags and tag access lists must be passed if tag based permissions are defined")
    elif tags and tagaccess:
        taglist = True

    if taglist is True:
        tagcompare = __comparelist(tags, tagaccess)

        if tagcompare == 2:
            warnings.warn(ListLengthWarn("Tags and tag access list are not the same length, lists will be joined to "
                                         "the shortest length list"))
            tagzip = zip(tags, tagaccess)
            for t, ta in tagzip:
                posttags.append({'tag': t, 'access': ta})

        elif tagcompare == 0:

            tagzip = zip(tags, tagaccess)
            for t, ta in tagzip:
                posttags.append({'tag': t, 'access': ta})

    postnets = []

    netlist = False

    if (networks and not netaccess) or (netaccess and not networks):
        raise AttributeError("Both network and network access lists must be passed if network based permissions "
                             "are defined")
    elif networks and netaccess:
        netlist = True

    if netlist is True:
        netcompare = __comparelist(networks, netaccess)
        if netcompare == 2:
            warnings.warn(ListLengthWarn("Networks and tag access list are not the same length, lists will be joined to"
                                         " the shortest length list"))
            netzip = zip(networks, netaccess)

            for n, na in netzip:
                postnets.append({'id': n, 'access': na})
        elif netcompare == 0:
            netzip = zip(networks, netaccess)

            for n, na in netzip:
                postnets.append({'id': n, 'access': na})

    postdata = {}

    if not rolename:
        raise ValueError("Role name must be passed for role creation")
    else:
        postdata['role'] = str(rolename)

    if orgaccess:
        postdata['orgAccess'] = str(orgaccess)

    if taglist is True:
        postdata['tags'] = posttags

    if netlist is True:
        postdata['networks'] = postnets

    dashboard = requests.post(posturl, data=json.dumps(postdata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


def updatesamlrole(apikey, orgid, roleid, rolename, orgaccess, tags, tagaccess, networks, netaccess,
                   suppressprint=False):
    #
    # Confirm API Key has Admin Access Otherwise Raise Error
    #
    __hasorgaccess(apikey, orgid)
    calltype = 'SAML Role'

    puturl = '{0}/organizations/{1}/samlRoles/{2}'.format(str(base_url), str(orgid), str(roleid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    if orgaccess and orgaccess not in ['read-only', 'full', 'none']:
        raise ValueError("Organization access must be either 'read-only' or 'full' or 'none")

    puttags = []

    taglist = False

    if (tags and not tagaccess) or (tagaccess and not tags):
        raise AttributeError("Both tags and tag access lists must be passed if tag based permissions are defined")
    elif tags and tagaccess:
        taglist = True

    if taglist is True:
        tagcompare = __comparelist(tags, tagaccess)

        if tagcompare == 2:
            warnings.warn(ListLengthWarn("Tags and tag access list are not the same length, lists will be joined to "
                                         "the shortest length list"))
            tagzip = zip(tags, tagaccess)
            for t, ta in tagzip:
                puttags.append({'tag': t, 'access': ta})

        elif tagcompare == 0:

            tagzip = zip(tags, tagaccess)
            for t, ta in tagzip:
                puttags.append({'tag': t, 'access': ta})

    putnets = []

    netlist = False

    if (networks and not netaccess) or (netaccess and not networks):
        raise AttributeError("Both network and network access lists must be passed if network based permissions "
                             "are defined")
    elif networks and netaccess:
        netlist = True

    if netlist is True:
        netcompare = __comparelist(networks, netaccess)
        if netcompare == 2:
            warnings.warn(ListLengthWarn("Networks and tag access list are not the same length, lists will be joined to"
                                         " the shortest length list"))
            netzip = zip(networks, netaccess)

            for n, na in netzip:
                putnets.append({'id': n, 'access': na})
        elif netcompare == 0:
            netzip = zip(networks, netaccess)

            for n, na in netzip:
                putnets.append({'id': n, 'access': na})

    roledata = {}

    if rolename:
        roledata['role'] = str(rolename)

    if orgaccess:
        roledata['orgAccess'] = str(orgaccess)

    if taglist is True:
        roledata['tags'] = puttags

    if netlist is True:
        roledata['networks'] = putnets

    putdata = [roledata]
    print(roledata, putdata, sep='\n')
    dashboard = requests.put(puturl, data=json.dumps(roledata), headers=headers)
    #
    # Call return handler function to parse Dashboard response
    #
    result = __returnhandler(dashboard.status_code, dashboard.text, calltype, suppressprint)
    return result


# def updateobject(apikey, networkid, newelement: DashboardObject, suppressprint=False):
#
#     puturl = '{0}/networks/{1}/ssids/{2}'.format(str(base_url), str(networkid), newelement.ssidnum)
#     headers = {
#         'x-cisco-meraki-api-key': format(str(apikey)),
#         'Content-Type': 'application/json'
#     }
#     if newelement.type == 'ssid':
#         puturl = '{0}/networks/{1}/ssids/{2}'.format(str(base_url), str(networkid), newelement.ssidnum)
#
#     putdata = json.dumps(newelement.__dict__)
#     print(putdata)
#     dashboard = requests.put(puturl, data=putdata, headers=headers)
#     #
#     # Call return handler function to parse Dashboard response
#     #
#     result = __returnhandler(dashboard.status_code, dashboard.text, str(newelement.type).upper() , suppressprint)
#     return result