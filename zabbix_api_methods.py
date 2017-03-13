
import sys
from zabbix.api import ZabbixAPI
from secrets import *



# Connect to ZabbixAPI
try:
    zapi = ZabbixAPI(url=ZABBIX_URL, user=ZABBIX_USERNAME, password=ZABBIX_PASSWORD)
except Exception as e:
    print("Failed to connect to Zabbix: " + str(e))
    sys.exit(0)


def zabbix_find_group(group_name):
    """
    Find Group ID by Group name.

    :param group_name:
    :return: group ID or 0 if group does not exist
    """
    group_filter = {
        'filter': {
            'name': group_name
        }
    }
    try:
        search_result = zapi.do_request('hostgroup.get', group_filter)  # Send request to Zabbix
    except Exception as error:
        print('Error while searching group:' + str(error))
        return 0
    # Check if group exists
    if search_result['result']:
        return search_result['result'][0]['groupid']
    else:
        return 0


def zabbix_print_all_groups():
    """
    Print all groups from zabbix.
    :return:
    """
    try:
        search_result = zapi.do_request('hostgroup.get')  # Send request to Zabbix
    except Exception as error:
        print('Error while searching group:' + str(error))
        return 0
    if search_result['result']:
        print('-' * 40)
        print('Groups:')
        for item in search_result['result']:
            print(item['name'], end=" | ")
        print()


def zabbix_find_template(template_name):
    """
    Find Template ID by Template name.

    :param template_name: Must be exactly as in Zabbix
    :return: template ID or 0 if template does not exist
    """
    template_filter = {
        'filter': {
            'name': template_name
        }
    }
    try:
        search_result = zapi.do_request('template.get', template_filter)  # Send request to Zabbix
    except Exception as error:
        print('Error while search template: ' + str(error))
        return 0
    # Check if template exists
    if search_result['result']:
        return search_result['result'][0]['templateid']
    else:
        return 0


def map_template_names(raw_name):
    """
    Map convinient template name with Zabbix template names. For often used templates only.
    :param raw_name: name from input. if it is 'print' - prints all available templates
    :return: name from Zabbix or False if name is not in list
    """
    template_names_map = {
        'juniper': 'JuniperT SNMP Device',
        'cisco': 'Cisco SNMP Device___T',
        'dlink': 'DLink SNMP Device macro',
        'mikrotik': 'Mikrotik SNMP Device T',
        'qtech': 'QTECH SNMP Device',
        'asa': 'Cisco ASA',
        'moxa': 'Moxa SNMP Device',
        'hp5800': 'HP 58xx SNMP Device',
        'hp5500': 'HP 5500 SNMP Device',
        'hp5120': 'HP 5120 SNMP Device',
        'hp1950': 'HP 1950 SNMP Device',
        'hp1920': 'HP 1920 SNMP Device',
        'ping': 'Ping_Loss'
    }
    if raw_name == 'print':
        print('-' * 40)
        print("Templates:")
        a = sorted(template_names_map.keys())
        print(' | '.join(a))
        return False
    if str(raw_name).lower().strip() in template_names_map.keys():
        return template_names_map[str(raw_name).lower().strip()]
    else:
        print(str(raw_name).lower().strip())
        print("Template name is not in list, use(" + ", ".join(template_names_map.keys()) + ")")
        return False


def zabbix_add_host(hostname, ip_address, group_name, template_name, snmp_community=DEFAULT_SNMP_COMMUNITY):
    """
    Add host to zabbix. do_request method in ZabbixAPI use 2 arguments:
        method - see full list on https://www.zabbix.com/documentation/3.2/manual/api
        parameters - parameters of host

    :param hostname: str, hostname of host
    :param ip_address: str, ip address of host
    :param group_name: str, group from zabbix where host belongs to
    :param template_name: str, name of template for host
    :param snmp_community: str, SNMP community string, if not specified it is DEFAULT_SNMP_COMMUNITY
    :return: True if host added, False if not
    """
    group_id = zabbix_find_group(group_name)
    template_name_mapped = map_template_names(template_name)
    template_id = zabbix_find_template(template_name_mapped)

    if not group_id or not template_id:
        print('Invalid Group or Template. Host does not added')
        return False
    print('Adding host...')
    parameters = {
        'host': hostname,
        'interfaces': [
            {
                'type': 2,  # 1 - Zabbix Agent, 2 - SNMP
                'main': 1,
                'useip': 1,
                'ip': ip_address,
                'dns': '',
                'port': '161'   # SNMP port
            }
        ],
        'groups': [
            {
                'groupid': group_id
            }
        ],
        'templates': [
            {
                'templateid': template_id
            }
        ],
        'macros': [
            {
                'macro': '{$SNMP_COMMUNITY}',
                'value': snmp_community
            }
        ],
        }
    try:
        zapi.do_request('host.create', parameters)
    except Exception as error:
        print('Can not add host: ' + str(error))
        return False
    print('Done')
    return True
