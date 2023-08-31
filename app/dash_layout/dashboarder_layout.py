from dash import html, dcc, dash_table

INTERVAL = 1000

DASHBOARDER_LAYOUT = html.Div(
    children=[
        html.Div(
            children=[
                dash_table.DataTable(id="asks"),
                html.Div(
                    children=[
                        html.Div(id="midprice"),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "padding": "10px 0px",
                        "font-weight": "bold",
                        "font-family": "monospace",
                        "font-size": "20px"
                    }
                ),
                dash_table.DataTable(id="bids"),
                dcc.Interval(id="timer", interval=INTERVAL),
            ],
            style={
                "width": "300px"
            }
        ),
        html.Div(
            children=[
                dcc.Graph(id="depth_graph")
            ]
        )
    ],
    style={
        "display": "flex"
    }
)