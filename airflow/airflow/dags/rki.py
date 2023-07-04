import os
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import logging
from sqlalchemy import create_engine

def download_xlsx_file():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab_aktuell.xlsx?__blob=publicationFile"
    file_path = "/opt/airflow/airflow_dag_data/data.xlsx"

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Check if the file already exists
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete existing file

    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)


def process_and_upload(sheet_name, table_name, header_row, skip_columns=None):
    # Read specific sheet
    df = pd.read_excel("/opt/airflow/airflow_dag_data/data.xlsx", sheet_name=sheet_name, header=header_row, skipfooter=1)


    logging.info(df.head())
    # Pivot the data if it is of type BL
    logging.info("Pivot the data if it is of type BL")
    if "BL" in sheet_name:
        df = pd.melt(df, id_vars=["MeldeLandkreisBundesland"], var_name="dat", value_name="val")
    
    else:
        df = pd.melt(df, id_vars=["LK", "LKNR"], var_name="dat", value_name="val")
        
    df['dat'] = pd.to_datetime(df['dat'], format='%d.%m.%Y')

    # Connect to PostgreSQL using SQLAlchemy
    logging.info("Connect to PostgreSQL using SQLAlchemy")
    engine = create_engine("postgresql+psycopg2://superset:superset@db:5432/superset")

    # Insert data into the table
    logging.info("Insert data into the table")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False, schema="public")

    # Close the connection
    engine.dispose()


def main_task(**kwargs):
    # Download the xlsx file
    logging.info("Download the xlsx file")
    download_xlsx_file()

    # Process each sheet and upload data
    logging.info("Process each sheet and upload data")
    sheets_info = [
        ("BL_7-Tage-Inz Hospital(fixiert)", "bl_7_inz_hospital", 4),
        ("BL_7-Tage-Fallzahlen (fixiert)", "bl7_fallzahlen", 4),
        ("BL_7-Tage-Inzidenz (fixiert)", "bl7_inzidenz", 4),
        ("LK_7-Tage-Fallzahlen (fixiert)", "lk_7_fallzahlen", 4),
        ("LK_7-Tage-Inzidenz (fixiert)", "lk_7_inzidenz", 4),
    ]

    for sheet_name, table_name, header_row in sheets_info:
        logging.info(f"Processing sheet '{sheet_name}'")
        process_and_upload(sheet_name, table_name, header_row)

    # Delete the xlsx file
    #os.remove("/opt/airflow/airflow_dag_data/data.xlsx")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}


dag = DAG(
    'rki_data_pipeline',
    default_args=default_args,
    description='Download RKI data and upload to PostgreSQL',
    schedule_interval='0 11 * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

with dag:
    main_task = PythonOperator(
        task_id='main_task',
        python_callable=main_task,
        provide_context=True,
    )

    main_task
