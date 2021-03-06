import random

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


# External CSS
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    dbc.themes.MORPH
]

# Dash app initialization
# Themes: DARKLY, LITERA, MORPH, QUARTZ, SKETCHY, SUPERHERO, ZEPHYR
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Progress of Kuzya'
server = app.server

# Data loading and using
running_df = pd.read_csv('data/running.csv')
running_df['date'] = pd.to_datetime(running_df['date'], format='%d/%m/%Y')

# Data calculating
tmp = running_df.groupby('date')['distance'].sum().reset_index()
tmp['distance_sum'] = tmp['distance'].cumsum()

# Prepare plot
running_fig = px.line(tmp, x='date', y='distance_sum', text='distance_sum',
                      hover_name='distance', markers=True, line_shape='spline')

running_fig.update_xaxes(title='Date')
running_fig.update_yaxes(title='Accumulated Distance')

running_fig.update_traces(textposition="bottom right")
running_fig.update_layout({

})

# Layout setting
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🐱", className="header-emoji"),

                html.H1(
                    children="Progress of Kuzya", className="header-title"
                ),

                html.P(
                    children="Analyze my results and progress in my "
                             "life using this site could be much easier (I hope 🙏)",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(
                            children="Days until Thesis presentation", className="card-title"
                        ),
                        dbc.Progress(
                            value=0.1,
                            min=0,
                            max=1,
                            striped=True,
                            animated=True,
                            id="progress_bar",
                        ),
                    ],
                    className="card"
                )
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(
                            children="Distance I ran so far ...", className="card-title"
                        ),
                        dcc.Graph(
                            id="running-chart",
                            config={"displayModeBar": False},
                            figure={
                                'data': [
                                    {
                                        'x': tmp['date'],
                                        'y': tmp['distance_sum'],
                                        'text': tmp['distance'],
                                        'type': 'scatter',
                                        'line': {
                                            'shape': 'spline',
                                            'smoothing': .9
                                        },
                                        "hovertemplate": "Daily: %{text:.1f}<br>"
                                                         "Total: %{y:.1f}"
                                                        "<extra></extra>"
                                    }
                                ],
                                'layout': {
                                    # "title": {
                                    #     "text": "Distance I ran so far ...",
                                    # },
                                    "xaxis": {
                                        "title": "Date",
                                        "fixedrange": True
                                    },
                                    "yaxis": {
                                        "title": "Cumulative Distance",
                                        "fixedrange": True
                                    },
                                    "colorway": ["#E876D2"],
                                }
                            },
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
)

# Run server
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
