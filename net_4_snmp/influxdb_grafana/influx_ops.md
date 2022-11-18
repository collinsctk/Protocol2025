### 容器安装
docker pull influxdb

docker run -idt --name influxdb -p 8086:8086 -v /Users/ssj/influxdb:/var/lib/influxdb influxdb

### 进入容器
docker exec -it influxdb /bin/bash

### 创建普通用户
CREATE USER "qytdbuser" WITH PASSWORD 'Cisc0123'

### 创建管理员
CREATE USER admin WITH PASSWORD 'Cisc0123' WITH ALL PRIVILEGES

### 删除用户
drop user admin

### 创建数据库
create database qytdb

### 使用数据库
use qytdb

### 给与普通用户数据库权限
grant all on qytdb to qytdbuser

### 创建retention policies
create retention policy "qytdb_rp_policy" on "qytdb" duration 3w replication 1 default

### 修改
alter retention policy "qytdb_rp_policy" on "qytdb" duration 30d default

### 查看retention policies
show retention policies on "qytdb"

### 删除retention policies
drop retention policy "qytdb_rp_policy" on qytdb