import matplotlib.pyplot as plt
from pandas.plotting import table
from io import BytesIO
import base64
plt.switch_backend('agg')
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
import dash_bootstrap_components as dbc

from dash import dash_table as dt
import pandas as pd
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.layout = html.Div([
    
    html.Button('What do you want to do with null values?', id='button-2', n_clicks=0),
    
  
    html.Div(id='controls-container', children=[
        # all of your controls
        dcc.Dropdown(id='data-set-chosen', multi=False, value='gapminder',
                     options=[{'label':'Country Data', 'value':'gapminder'},
                              {'label':'Restaurant Tips', 'value':'tips'},
                              {'label':'Flowers', 'value':'iris'}])
        # ...
    ]),
])



@app.callback(
    Output('controls-container', 'style'),

    Input("button-2", "n_clicks"))

def update_graph(n_clicks):
    
    if n_clicks:
        
        return {'display': 'block'}
    else:
        return {'display': 'none'}




if __name__ == '__main__':
    app.run_server(host='localhost',port='5244', debug=True)