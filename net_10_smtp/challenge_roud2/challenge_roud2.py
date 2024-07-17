#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import sys
import re
from qyt_email import qyt_smtp_attachment

para_raw = ' '.join(sys.argv[1:])
para_raw = para_raw.strip()

# received from 202.100.12.2 : 4 exceeds limit 3


re_result = re.match('received from\s+(\S+)\s+:\s+(\d+)\s+exceeds\s+limit\s+(\d+)',
                     para_raw).groups()
if re_result:
    ipaddr = re_result[0]
    exceed_num = re_result[1]
    limit_num = re_result[2]

    body_string = "Neighbor: " + ipaddr + "\nNow: " + exceed_num + "\nExceed the limit: " + limit_num

    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'anchwprpwxfbdbif',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        'Bgp prefix limit exceed',
                        body_string)

else:
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'anchwprpwxfbdbif',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        'Bgp prefix limit exceed',
                        're failed')
