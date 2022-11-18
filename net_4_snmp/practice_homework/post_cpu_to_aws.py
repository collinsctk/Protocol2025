from net_7_snmp.snmp_v2.snmpv2_get import snmpv2_get
import time
from datetime import datetime
import requests
import json

while True:
    try:
        cpu_percent = int(snmpv2_get("10.1.1.253", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1])
        router_name = 'R1'
        cpu_timestamp = str(datetime.now().timestamp())
        post_dict = {'cpu_percent': cpu_percent,
                     'router_name': router_name,
                     'cpu_timestamp': cpu_timestamp}
        print(post_dict)
        print(json.dumps(post_dict))
        result = requests.post('https://aws2022-serverless-api.mingjiao.org/api/cpu-usage', json=post_dict)
        # result = requests.post('https://api.mingjiao.org/api/cpu-usage', json=post_dict)
        print(result.json())
    except Exception as e:
        print(e)
        pass
    time.sleep(10)
