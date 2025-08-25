from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/opt/airflow/scripts")
from fetch_stock import fetch_stock_data, store_to_db

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_pipeline():
    rows = fetch_stock_data()
    if rows:
        store_to_db(rows)

with DAG(
    "stock_pipeline",
    default_args=default_args,
    description="Fetch and store stock data in MySQL",
    schedule_interval="@hourly",  # runs every hour
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="fetch_and_store_stock_data",
        python_callable=run_pipeline
    )
