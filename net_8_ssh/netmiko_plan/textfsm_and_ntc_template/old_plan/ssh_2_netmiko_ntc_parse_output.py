from net_8_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
from ntc_templates.parse import parse_output
from pprint import pprint

raw_result = netmiko_show_cred('10.10.1.1',
                               'admin',
                               'Cisc0123',
                               'show ip inter brie')
print(raw_result)


show_ip_interface_brief = parse_output(platform="cisco_ios",
                                       command="show ip interface brief",
                                       data=raw_result)

pprint(show_ip_interface_brief)
