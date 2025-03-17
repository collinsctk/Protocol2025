### 测试代码
```shell
[root@AIOps ~]# /root/.virtualenvs/protocol2022/bin/python3.11 /protocol2022/net_4_snmp/practice_lab/lab2/influxdb_monitor_router.py
```

### crond调度
```shell
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
* * * * * root /root/.virtualenvs/protocol2022/bin/python3.11 /protocol2022/net_4_snmp/practice_lab/lab1/orm_2_write_db.py
* * * * * root /root/.virtualenvs/protocol2022/bin/python3.11 /protocol2022/net_4_snmp/practice_lab/lab2/influxdb_monitor_router.py

```

### 重启服务
```shell
[root@AIOps ~]# systemctl restart crond.service
```
