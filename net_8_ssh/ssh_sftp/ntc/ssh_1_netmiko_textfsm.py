from net_8_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
from textfsm import TextFSM
# TextFSM的中文翻译https://www.jianshu.com/p/e75daa3af0a4
from pprint import pprint

raw_result = netmiko_show_cred('10.1.1.253', 'admin', 'Cisc0123', 'show ip interface brief')
print(raw_result)
# raw_result = """
# Interface              IP-Address      OK? Method Status                Protocol
# GigabitEthernet1       10.1.1.253      YES NVRAM  up                    up
# GigabitEthernet2       20.1.1.1        YES manual up                    up
# GigabitEthernet3       30.1.1.253      YES manual administratively down down
# """


# 模板正则表达式 ?: 的介绍
# 匹配 'x' 但是不记住匹配项。这种括号叫作非捕获括号，使得你能够定义与正则表达式运算符一起使用的子表达式。
# 看看这个例子 /(?:foo){1,2}/。如果表达式是 /foo{1,2}/，{1,2} 将只应用于 'foo' 的最后一个字符 'o'。
# 如果使用非捕获括号，则 {1,2} 会应用于整个 'foo' 单词。
# https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Regular_Expressions

# Value INTER (\D+\d+((/\d+)+(\.\d+)?)?)
# \D+ 首位不能为数字 \d+ 紧接着是数字 ((/\d+)+(\.\d+)?)? 后续可能有/或者.的子接口
# Value IPADD (\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)
# \b匹配字符边界 第一位可能25x 2[0-4]x 1xx ....

with open('testfsm_template_(show ip interface brief).template') as f:
    template = TextFSM(f)
    show_vlan_dict = template.ParseText(raw_result)
    pprint(show_vlan_dict)
