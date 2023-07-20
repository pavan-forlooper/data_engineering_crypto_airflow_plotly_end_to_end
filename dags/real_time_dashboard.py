import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
from dash.dependencies import Input, Output

# Use the root path of your project
root_path = "/Users/PavanAray/PycharmProjects/af_end_to_end_in_finnhub" \
            "/finnhub_airflow_plotly_end_to_end_data_engineering/project/"

# Define the path to the CSV files
dags_path = os.path.join(root_path, "dags")

# Read the CSV files
df_BTCUSDT = pd.read_csv(os.path.join(dags_path, "BTCUSDT.csv"))
df_ETHUSDT = pd.read_csv(os.path.join(dags_path, "ETHUSDT.csv"))
df_XRPUSDT = pd.read_csv(os.path.join(dags_path, "XRPUSDT.csv"))

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Graph(id='btc-graph', figure={
            'data': [
                go.Scatter(x=df_BTCUSDT['t'], y=df_BTCUSDT['c'], mode='lines+markers', name='BTC/USDT')
            ],
            'layout': {
                'title': 'Bitcoin Current Value'
            }
        }),

        dcc.Graph(id='eth-graph', figure={
            'data': [
                go.Scatter(x=df_ETHUSDT['t'], y=df_ETHUSDT['c'], mode='lines+markers', name='ETH/USDT')
            ],
            'layout': {
                'title': 'Ethereum Current Value'
            }
        }),

        dcc.Graph(id='xrp-graph', figure={
            'data': [
                go.Scatter(x=df_XRPUSDT['t'], y=df_XRPUSDT['c'], mode='lines+markers', name='XRP/USDT')
            ],
            'layout': {
                'title': 'Ripple(XRP) Current Value'
            }
        }),

        dcc.Interval(
            id='interval-component',
            interval=2 * 60 * 1000,  # 2 minutes in milliseconds
            n_intervals=0
        )
    ]
)

@app.callback(
    Output('btc-graph', 'figure'),
    Output('eth-graph', 'figure'),
    Output('xrp-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n_intervals):
    # Read the CSV files again to get the latest data
    df_BTCUSDT = pd.read_csv(os.path.join(dags_path, "BTCUSDT.csv"))
    df_ETHUSDT = pd.read_csv(os.path.join(dags_path, "ETHUSDT.csv"))
    df_XRPUSDT = pd.read_csv(os.path.join(dags_path, "XRPUSDT.csv"))

    # Create the graph figures using Plotly
    fig_BTCUSDT = go.Figure()
    fig_BTCUSDT.add_trace(go.Scatter(x=df_BTCUSDT['t'], y=df_BTCUSDT['c'], mode='lines+markers', name='BTC/USDT'))

    fig_ETHUSDT = go.Figure()
    fig_ETHUSDT.add_trace(go.Scatter(x=df_ETHUSDT['t'], y=df_ETHUSDT['c'], mode='lines+markers', name='ETH/USDT'))

    fig_XRPUSDT = go.Figure()
    fig_XRPUSDT.add_trace(go.Scatter(x=df_XRPUSDT['t'], y=df_XRPUSDT['c'], mode='lines+markers', name='XRP/USDT'))

    return fig_BTCUSDT, fig_ETHUSDT, fig_XRPUSDT


if __name__ == '__main__':
    app.run_server(debug=True)
