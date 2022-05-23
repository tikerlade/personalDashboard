import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# External CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Data loading and using
running_df = pd.read_csv('data/running.csv')
running_df['date'] = pd.to_datetime(running_df['date'], format='%d/%m/%Y')

# Data calculating
tmp = running_df.groupby('date')['distance'].sum().reset_index()
tmp['distance_sum'] = tmp['distance'].cumsum()

# Prepare plot
running_fig = px.line(tmp, x='date', y='distance_sum', text='distance_sum', hover_name='distance', markers=True, line_shape='spline')

running_fig.update_xaxes(title='Date')
running_fig.update_yaxes(title='Accumulated Distance')

running_fig.update_traces(textposition="bottom right")
running_fig.update_layout(
    {'title': 'Cumulative distance of running done'}
)

running_graph = dcc.Graph(
    figure=running_fig
)

# Layout setting
app.layout = html.Div([running_graph], style={'backgroundColor': 'black'})

# Run server
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
