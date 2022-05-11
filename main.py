import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
import dash_bootstrap_components as dbc

import pandas as pd

from page import page1, page2, page3

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)



app.layout = html.Div([
  dbc.Navbar(
    [
      dbc.Row(
                [
                    
                    dbc.Col(html.H1("Data Science Tutorial Application", className="ml-1",style={'font-size':'42px','font-weight':'bold', 'test-align': 'center'})),
                
                ]
                
            ),
        
    ],
    color="white",
    dark=True,
),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])



def getMainLayout():
    return [
        #
        # Section 1
        #
        html.Section(
            [
                #
                # ROW
                #
                html.Div(
                    [
                      #
                      # CARD 1
                      #
                      html.Div(
                            [
                                
                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-comment-dollar"),
                                                    html.H4("Data Analysis",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                          
                                        ],
                                        className="card__side card__side--front-1"
                                    ),
                                    className="card"
                                ),href="/page1")

                            ],
                            className="col-1-of-3"
                        ),
                        #
                        # CARD 2
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-users"),
                                                    html.H4("Data Visualization",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                          
                                        ],
                                        className="card__side card__side--front-2"
                                    ),
                                    className="card"
                                ),href="/page2")

                            ],
                            className="col-1-of-3"
                        ),
                        #
                        # CARD 2
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-box-open"),
                                                    html.H4("Machine Learning",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                           
                                        ],
                                        className="card__side card__side--front-3"
                                    ),
                                    className="card"
                                ),href="/page3")

                            ],
                            className="col-1-of-3"
                        ),

                    ],  # ROW
                    className="row-card"
                ),
            ],
            className="section-plans"
        ),
        #
        # Section 2
        #
        html.Section(
            [
                #
                # ROW
                #
                html.Div(
                    [
                      #
                      #CARD 3
                      #
                        html.Div(
                            [
                              
                               dcc.Link( html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-briefcase"),
                                                    html.H4("Deep Learning",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                          
                                        ],
                                        className="card__side card__side--front-4"
                                    ),
                                    className="card"
                            ),href="/suppliers/suppliersPage")
                            ],
                            className="col-1-of-3"
                        ),


                           html.Div(
                            [
                              
                               dcc.Link( html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-briefcase"),
                                                    html.H4("Big Data",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                          
                                        ],
                                        className="card__side card__side--front-5"
                                    ),
                                    className="card"
                            ),href="/suppliers/suppliersPage")
                            ],
                            className="col-1-of-3"
                        ),


                         html.Div(
                            [
                              
                               dcc.Link( html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-briefcase"),
                                                    html.H4("Database Queries",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                          
                                        ],
                                        className="card__side card__side--front-6"
                                    ),
                                    className="card"
                            ),href="/suppliers/suppliersPage")
                            ],
                            className="col-1-of-3"
                        ),
                      
                     
                    

                    ],  # ROW
                    className="row-card"
                ),
            ],
            className="section-plans"
        ),
    ]






@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):



    if pathname == '/':
        # if not data.empty:
        #     return dummyLayout()
        # else:
        return getMainLayout()

    
    
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout

    elif pathname == '/page3':
        return page3.layout

    
    else:
        return 'Usman Afridi'
    



if __name__ == '__main__':
    app.run_server(host='localhost',port='5242', debug=True)
