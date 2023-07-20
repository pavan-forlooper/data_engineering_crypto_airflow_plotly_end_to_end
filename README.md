# data_engineering_crypto_airflow_plotly_end_to_end

## Summary

This repository contains an end-to-end data pipeline built using Apache Airflow and a real-time dashboard created with Dash. The project fetches cryptocurrency data from the Finnhub API, stores it as CSV files, and displays real-time visualizations on a web-based dashboard.

The data pipeline uses Apache Airflow to schedule and orchestrate the data retrieval process. It fetches data for three cryptocurrencies (BTC, ETH, and XRP) every minute from the Finnhub API using the provided API key. The data is then saved into separate CSV files for each currency.

The real-time dashboard is built using Dash, a Python web application framework based on Plotly. It visualizes the latest cryptocurrency prices as time-series line charts for Bitcoin (BTC/USDT), Ethereum (ETH/USDT), and Ripple (XRP/USDT). The dashboard automatically updates every two minutes to display the most recent data.

## Getting Started

### Prerequisites

- Python 3.x
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)
- [Dash](https://dash.plotly.com/installation)

## The project is organized as follows:
|-- dags/
|   |-- get_api_key.py
|   |-- get_data.py
|   |-- store_data_from_finnhub_DAG.py
|   |-- write_data_to_files.py
|-- real_time_dashboard.py
|-- requirements.txt
|-- README.md


## Airflow DAG Setup
Start the Airflow web server and scheduler:

airflow webserver -p 8080
airflow scheduler
Access the Airflow web UI at http://localhost:8080, and set up the DAG named store_data_from_finnhub_DAG.

Make sure you have a valid Finnhub API key. You can get it by signing up at Finnhub.io.

# Update the get_api_key.py script with your API key.

## Running the DAG
The DAG is scheduled to run every minute by default. You can manually trigger it from the Airflow web UI, or it will run automatically based on the schedule defined in the DAG.

## Real-Time Dashboard
To view the real-time dashboard:
Make sure the Airflow DAG is running and fetching data.
Run the Dash app: python real_time_dashboard.py
Access the dashboard at http://127.0.0.1:8050/

