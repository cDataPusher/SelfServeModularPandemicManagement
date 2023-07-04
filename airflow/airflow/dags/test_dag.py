from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging

def test_airflow_functionality():
    logging.info("Airflow is working fine!")

dag = DAG(
    'test_airflow_functionality',
    description='Test DAG to check if Airflow is working',
    schedule_interval='*/1 * * * *',
    start_date=datetime(2023, 7, 4),
    catchup=False
)

task = PythonOperator(
    task_id='test_task',
    python_callable=test_airflow_functionality,
    dag=dag
)
