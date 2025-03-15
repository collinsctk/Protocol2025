# docker compose 文件下载位置
# https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
FROM apache/airflow:2.10.2-python3.11

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
