import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd

# External CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Data loading and using
df = pd.read_csv('data/restaurants_zomato.csv', encoding="ISO-8859-1")

running_df = pd.read_csv('data/running.csv')
running_df['date'] = pd.to_datetime(running_df['date'], format='%d/%m/%Y')

tmp = running_df.groupby('date')['distance'].sum().reset_index()
tmp['distance_sum'] = tmp['distance'].cumsum()
# running_fig = px.line(tmp, x="date", y="distance_sum", title='Running Distance')

running_fig = px.line(tmp, x='date', y='distance_sum', text='distance', markers=True, line_shape='spline')
running_fig.update_traces(textposition="bottom right")

# country iso with counts
col_label = "country_code"
col_values = "count"

v = df[col_label].value_counts()
new = pd.DataFrame({
    col_label: v.index,
    col_values: v.values
})

# Preparing panels
hexcode = 0
borders = [hexcode for x in range(len(new))]

running_graph = dcc.Graph(figure=running_fig)

# Layout setting
app.layout = html.Div([running_graph], style={'backgroundColor': 'black'})

# Run server
if __name__ == '__main__':
    app.run_server(debug=True,port=8056)
