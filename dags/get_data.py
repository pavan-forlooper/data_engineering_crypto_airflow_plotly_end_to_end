import requests
import pandas as pd
import datetime
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


def get_data_finnhub(url, currency_symbols, authentication_key):

    df = pd.DataFrame()
    try:
        url = url
        for currency in currency_symbols:
            data = requests.get(url, {"symbol": currency, "token": authentication_key})
            json_data = data.json()
            json_data['currency'] = currency
            json_data['t'] = datetime.datetime.fromtimestamp(json_data['t']).strftime('%Y-%m-%d %H:%M:%S')
            df = df.append([json_data])
            logger.debug(f"Fetched data for currency: {currency}")
        logger.info("Fetched data from Finnhub API")
        return df
    except Exception as e:
        logger.exception(f"Error fetching data: {e}, Status Code: {data.status_code}")
