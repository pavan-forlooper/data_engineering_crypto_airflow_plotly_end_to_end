import pandas as pd
import os
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


def write_data_to_files(df_param, currency_name):
    print('write_data_to_files', df_param, currency_name)
    # Use the /usr/local/airflow/dags directory as the root path
    dags_path = "/usr/local/airflow/dags/"

    # Combine the 'dags' directory path and the file name to get the full file path
    file_path = os.path.join(dags_path, f"{currency_name}.csv")

    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        logger.info(f"File not found or empty: {e}")
        df = pd.DataFrame()

    if not df.empty:
        df = pd.concat([df, df_param])
        logger.debug(f"Appended data for currency: {currency_name}")
    else:
        logger.info(f"{currency_name} is empty")
        df = df_param
    logger.info(f"Saving DataFrame to CSV: {file_path}")
    df.to_csv(file_path, index=False)
