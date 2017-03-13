import sys
from zabbix_api_methods import *


def main():
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print('Wrong number of arguments.')
        print(' - python {} hostname ipaddress group template'.format(sys.argv[0]))
        print('ex. \n - python {} my-hostname 8.8.8.8 HP hp5800'.format(sys.argv[0]))
        zabbix_print_all_groups()
        map_template_names('print')
        exit(1)
    print('Connecting to Zabbix...')
    print('Hostname: {}'.format(sys.argv[1]))
    print('IP: {}'.format(sys.argv[2]))
    print('Group ID: {}'.format(sys.argv[3]))
    print('Template ID: {}'.format(sys.argv[4]))

    cont = input('Add host? Y/N: ')

    if (cont.lower() == 'y' or cont.lower() == 'yes') and check_if_ip(sys.argv[2]) is True:
                zabbix_add_host(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


def check_if_ip(address):
    a = address.strip().split('.')
    if len(a) != 4:
        print('IP address {} is too short.'.format(address))
        return False
    try:
        for item in a:
            if 0 <= int(item) < 256:
                continue
            else:
                print('Error in this octet ({}) of ip address: {}'.format(item, address))
                return False
        return True
    except Exception as e:
        print('Unknown error in ip address {}: {}'.format(address, e))
        return False


if __name__ == '__main__':
    main()
