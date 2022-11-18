from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host, router_ip

client = InfluxDBClient(influx_host, 8086, 'admin', 'Cisc0123', 'qytdb')

# 绝对值
abs_result = client.query('select ABS("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
# print(abs_result)

# ACOS()  返回field value的反余弦(以弧度表示)。field value必须在-1和1之间。
# ASIN()  返回field value的反正弦(以弧度表示)。field value必须在-1和1之间。
# ATAN()  返回field value的反正切(以弧度表示)。field value必须在-1和1之间。
# ATAN2() 返回以弧度表示的y/x的反正切。
# CEIL() 返回大于指定值的最小整数
# COS() 返回field value的余弦值

# 返回field value的累积总和。
cumulative_sum_result = client.query('select CUMULATIVE_SUM("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
# print(cumulative_sum_result)


# DERIVATIVE() 返回field value之间的变化率，即导数
# TSDB For InfluxDB®计算field value之间的差值，并将这些结果转换为每个unit的变化率。
# 参数unit的值是一个整数，后跟一个时间单位。这个参数是可选的，不是必须要有的。如果查询没有指定unit的值，
# 那么unit默认为一秒(1s)。
if_monitor_result = client.query('select in_bytes from if_monitor group by \"device_ip\", \"device_type\";')
# print(if_monitor_result)
derivative_result = client.query('select DERIVATIVE("in_bytes") from if_monitor group by \"device_ip\", \"device_type\";')
# print(derivative_result)

# 直接计算得到速率
derivative_result_8 = client.query('select DERIVATIVE("in_bytes") * 8 from if_monitor group by \"device_ip\", \"device_type\";')
# print(derivative_result_8)
for x in derivative_result_8.get_points(tags={'device_ip': router_ip, 'device_type': 'IOS-XE'}):
    print(x)

# DIFFERENCE() 返回field value之间的差值。
difference_result = client.query('select DIFFERENCE("in_bytes") from if_monitor group by \"device_ip\", \"device_type\";')
# print(difference_result)

# ELAPSED() 返回field value的时间戳之间的差值。
elapsed_result = client.query('select ELAPSED("in_bytes") from if_monitor group by \"device_ip\", \"device_type\";')
# print(elapsed_result)

# EXP() 返回field value的指数
# FLOOR() 返回小于指定值的最大整数
# LN() 返回field value的自然对数
# LOG() 返回field value的以b为底数的对数。
# LOG2() 返回field value的以2为底数的对数。
# LOG10() 返回field value的以10为底数的对数。
# MOVING_AVERAGE() 返回field value窗口的滚动平均值
# NON_NEGATIVE_DERIVATIVE() 返回field value之间的非负变化率。非负变化率包括正的变化率和等于0的变化率。
# NON_NEGATIVE_DIFFERENCE() 返回field value之间的非负差值。非负差值包括正的差值和等于0的差值。
# POW() 返回field value的x次方
# ROUND() 返回指定值的四舍五入后的整数。
# SIN() 返回field value的正弦值。
# SQRT() 返回field value的平方根
# TAN() 返回field value的正切值。
