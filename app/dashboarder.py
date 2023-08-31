from itertools import accumulate
import operator
import os

from dash import Dash, Input, Output
import plotly.graph_objects as go
import pandas as pd

from kafka_pc.consumer import Consumer
from dash_layout.dashboarder_layout import DASHBOARDER_LAYOUT

LEVELS_TO_SHOW = int(os.environ.get('LEVELS_TO_SHOW'))
TOPIC = os.environ.get('TOPIC')
BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BROKER_ADDRESSES')

app = Dash()
app.layout = DASHBOARDER_LAYOUT


def build_orderbook_table(message_data: dict):
    ask_df = pd.DataFrame(message_data["asks"], columns=["price", "amount"], dtype=float)
    bid_df = pd.DataFrame(message_data["bids"], columns=["price", "amount"], dtype=float)
    ask_df = ask_df.sort_values("price", ascending=False)
    bid_df = bid_df.sort_values("price", ascending=False)
    ask_df = ask_df.iloc[-LEVELS_TO_SHOW:]
    bid_df = bid_df.iloc[:LEVELS_TO_SHOW]

    mid_price = (bid_df.iloc[0].price + ask_df.iloc[-1].price) / 2
    mid_price = mid_price.round(2)

    return ask_df.to_dict("records"), bid_df.to_dict("records"), mid_price


def build_depth_graph(message_data: dict):
    ask_df = pd.DataFrame(message_data["asks"], columns=["price", "amount"], dtype=float)
    bid_df = pd.DataFrame(message_data["bids"], columns=["price", "amount"], dtype=float)
    bid_df_graph = bid_df.sort_values("price", ascending=False)
    ask_df_graph = ask_df.sort_values("price", ascending=True)
    
    bid_trace = go.Scatter(
        x=bid_df_graph.price,
        y=list(accumulate(bid_df_graph.amount, operator.add)),
        mode="lines", name="Buy", line={"color": "blue"},
    )
    ask_trace = go.Scatter(
        x=ask_df_graph.price,
        y=list(accumulate(ask_df_graph.amount, operator.add)),
        mode="lines", name="Sell", line={"color": "red"},
    )
    layout = go.Layout( title="Depth Graph (ETH/USDT)" )

    return {"data": [ask_trace, bid_trace], "layout": layout}


@app.callback(
    Output("asks", "data"),
    Output("bids", "data"),
    Output("midprice", "children"),
    Output("depth_graph", "figure"),
    Input("timer", "n_intervals")
)
def redraw_orderbook(_):
    print("="*30)
    kafka_consumer = Consumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    message_data = kafka_consumer.get_latest_message()

    ask_table, bid_table, mid_price = build_orderbook_table(message_data)
    depth_graph = build_depth_graph(message_data)
    
    return ask_table, bid_table, mid_price, depth_graph


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)