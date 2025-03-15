### 测试代码
```shell
[root@QYTRocky ~]# /root/.virtualenvs/DevNet_For_TSMC/bin/python3.11 /DevNet_For_TSMC/part_4_snmp/practice_lab/orm_2_write_db.py
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
* * * * * root /root/.virtualenvs/DevNet_For_TSMC/bin/python3.11 /DevNet_For_TSMC/part_4_snmp/practice_lab/orm_2_write_db.py

```

### 重启服务
```shell
[root@QYTRocky ~]# systemctl restart crond.service

```
