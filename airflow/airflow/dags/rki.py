import requests
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
from airflow.utils.dates import days_ago

def fetch_rki_data():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab_aktuell.xlsx?__blob=publicationFile"
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    return df

def write_to_db(df, engine):
    df.to_sql('rki_infection_data', engine, if_exists='replace')

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'rki_infection_data',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
)

fetch_data = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_rki_data,
    dag=dag,
)

write_data = PythonOperator(
    task_id='write_data',
    python_callable=write_to_db,
    op_kwargs={'engine': create_engine('postgresql+psycopg2://superset:superset@db:5432/superset')},
    dag=dag,
)

fetch_data >> write_data
