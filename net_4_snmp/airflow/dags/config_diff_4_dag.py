from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from config_diff_3_get_md5_config import config_diff_and_notification
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
    # 'on_failure_callback': qyt_smtp_attachment,  # 添加失败回调函数
    # 'on_success_callback': qyt_smtp_attachment,  # 添加成功回调函数
}

with DAG(
    'config_bak_and_diff_notification_dag',  # DAG的名称
    default_args=default_args,
    # schedule_interval=timedelta(seconds=10),  # 设置为每 30 秒调度一次
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
    schedule_interval='*  *  *  *  *',  # 每一分钟执行一次
    catchup=False,
) as dag:
    run_my_script = PythonOperator(
        task_id='Config_BAK_and_Diff_Notification',  # 不能使用中文,空格也不行
        python_callable=config_diff_and_notification,  # 执行的函数
    )

# [root@AIOps dags]# docker compose restart airflow-webserver airflow-scheduler
