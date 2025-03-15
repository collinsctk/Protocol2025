from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from orm_2_write_db import get_info_writedb, ip_address, username, auth_key, priv_key
from qyt_send_mail import qyt_smtp_attachment
import pendulum


# 定义时区
local_tz = pendulum.timezone("Asia/Shanghai")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 5, 0, 0, tzinfo=local_tz),
    'retries': 1,  # 重试次数
    'retry_delay': timedelta(seconds=10),  # 重试间隔
    'on_failure_callback': qyt_smtp_attachment,  # 添加失败回调函数
    # 'on_success_callback': qyt_smtp_attachment,  # 添加成功回调函数
}

with DAG(
    'get_snmp_info_writedb_dag',  # DAG的名称
    default_args=default_args,
    schedule_interval=timedelta(seconds=30),  # 设置为每 30 秒调度一次
    # ~~~~~~~~~~~~~~~ crontabs ~~~~~~~
                     # .---------------- minute (0 - 59)
                     # |  .------------- hour (0 - 23)
                     # |  |  .---------- day of month (1 - 31)
                     # |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
                     # |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
                     # |  |  |  |  |
                     # *  *  *  *  * user-name  command to be executed
    # schedule_interval='0  2  *  *  1',  # 每周一凌晨2点执行
    # schedule_interval='0  3  1  *  *',  # 每月1号凌晨3点执行
    catchup=False,
) as dag:
    run_my_script = PythonOperator(
        task_id='GET_SNMP_INFO_WriteDB',  # 不能使用中文,空格也不行
        python_callable=get_info_writedb,  # 执行的函数
        op_kwargs={'ip_address': ip_address,
                   'username': username,
                   'auth_key': auth_key,
                   'priv_key': priv_key
                   },  # 关键字参数字典
    )

# [root@AIOps dags]# docker compose restart airflow-webserver airflow-scheduler
