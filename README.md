# generate_config
Generate config for network devices and add device into Zabbix


Zabbix URL, login and password should be stored in secrets.py file in this format:

``` python
# Default configuration
ZABBIX_URL = "http://zabbix.companyname.ru"
ZABBIX_USERNAME = "username"
ZABBIX_PASSWORD = "password-in-plain-text"
DEFAULT_SNMP_COMMUNITY = "SNMP-community"
```
