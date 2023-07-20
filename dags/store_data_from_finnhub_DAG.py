from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from get_data import get_data_finnhub
from write_data_to_files import write_data_to_files
from get_api_key import get_finnhub_api_key
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/usr/local/airflow/logs/<filename>.log')
    ]
)
logger = logging.getLogger(__name__)

default_args = {
    "owner": "airflow",
    "retries": 1,
    "start_date": datetime(2023, 7, 19),
    "retry_delay": timedelta(seconds=15),
}


def main(**kwargs):
    print('main_run')
    df_main_BTCUSDT = pd.DataFrame()
    df_main_BETHUSDT = pd.DataFrame()
    df_main_BXRPUSDT = pd.DataFrame()

    # Get the API key using the get_api_key task's output
    api_key = kwargs['ti'].xcom_pull(task_ids='get_api_key_task')
    logger.info('fetch api_key successful')

    # Call the get_data_finnhub task and pass the API key as an argument
    df = get_data_finnhub("https://finnhub.io/api/v1/quote", ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:XRPUSDT"], api_key)
    logger.info('api call successful')

    df_main_BTCUSDT = pd.concat([df[df['currency'] == 'BINANCE:BTCUSDT']])
    df_main_ETHUSDT = pd.concat([df[df['currency'] == 'BINANCE:ETHUSDT']])
    df_main_XRPUSDT = pd.concat([df[df['currency'] == 'BINANCE:XRPUSDT']])

    # Pass the DataFrames to the next tasks using XCom
    kwargs['ti'].xcom_push(key='df_main_BTCUSDT', value=df_main_BTCUSDT)
    kwargs['ti'].xcom_push(key='df_main_ETHUSDT', value=df_main_ETHUSDT)
    kwargs['ti'].xcom_push(key='df_main_XRPUSDT', value=df_main_XRPUSDT)


def write_BTCUSDT(**kwargs):
    df_main_BTCUSDT = kwargs['ti'].xcom_pull(task_ids='fetch_data_task', key='df_main_BTCUSDT')
    write_data_to_files(df_main_BTCUSDT, 'BTCUSDT')


def write_ETHUSDT(**kwargs):
    df_main_ETHUSDT = kwargs['ti'].xcom_pull(task_ids='fetch_data_task', key='df_main_ETHUSDT')
    write_data_to_files(df_main_ETHUSDT, 'ETHUSDT')


def write_XRPUSDT(**kwargs):
    df_main_XRPUSDT = kwargs['ti'].xcom_pull(task_ids='fetch_data_task', key='df_main_XRPUSDT')
    write_data_to_files(df_main_XRPUSDT, 'XRPUSDT')


# Define the DAG
with DAG(
        dag_id="store_data_from_finnhub_DAG",
        schedule_interval='*/1 * * * *',
        default_args=default_args,
        catchup=False) as dag:

    # Define the get_api_key task
    get_api_key_task = PythonOperator(
        task_id="get_api_key_task",
        python_callable=get_finnhub_api_key,
    )

    # Define the main task
    fetch_data_task = PythonOperator(
        task_id="fetch_data_task",
        python_callable=main,
        provide_context=True,  # To pass the task context to the function
    )

    # Define the write_BTCUSDT task
    write_BTCUSDT_task = PythonOperator(
        task_id="write_BTCUSDT_task",
        python_callable=write_BTCUSDT,
        provide_context=True,  # To pass the task context to the function
    )

    # Define the write_ETHUSDT task
    write_ETHUSDT_task = PythonOperator(
        task_id="write_ETHUSDT_task",
        python_callable=write_ETHUSDT,
        provide_context=True,  # To pass the task context to the function
    )

    # Define the write_XRPUSDT task
    write_XRPUSDT_task = PythonOperator(
        task_id="write_XRPUSDT_task",
        python_callable=write_XRPUSDT,
        provide_context=True,  # To pass the task context to the function
    )


# Set dependencies between tasks
get_api_key_task >> fetch_data_task
fetch_data_task >> write_BTCUSDT_task
fetch_data_task >> write_ETHUSDT_task
fetch_data_task >> write_XRPUSDT_task
