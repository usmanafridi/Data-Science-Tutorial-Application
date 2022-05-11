import base64
import datetime
import io

import dash
from dash import Dash, dcc, html, Input, Output, State, callback
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq

import pandas as pd



layout = html.Div([ 
    
    html.Div([

        html.H1('Data Visualization Section', style={'text-align': 'center'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    ],className="row-flex display"),

    html.Div([
    
    html.Div([ 
        html.Div(id='output-div'),], className= "create_container five columns"),
    

    html.Div(id='output-datatable'),

    ],className="row-flex display"),


], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        
        html.Div([

        html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        

       

        html.P("Inset X axis data"),
        dcc.Dropdown(id='xaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),

        html.P("Inset Z axis data"),
        dcc.Dropdown(id='zaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),


         html.P("Choose Graph"),
        dcc.Dropdown(id='chart-type',
                     options=[{'label': 'Bar chart', 'value': 'bar'},

                             {'label': 'Line chart', 'value': 'line'},

                             {'label': 'Pie chart', 'value': 'pie'},

                             {'label': 'Bubble chart', 'value': 'bubble'} ]),

        html.Button(id="submit-button", children="Create Graph"),

        html.Br(),

        html.P('Choose one:'),


        dcc.RadioItems(options=[
        {'label': 'Total Sum', 'value': 'sum'},
        {'label': 'Number', 'value': 'number'},
        
    ],
        value='sum',
        id='radio'
),

    ],className="create_container two columns"),

        html.Div([

        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     page_size=15
        # ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Div([daq.ColorPicker(id='color-picker', label='Color Picker', value=dict(hex='#119DFF'))]),

        html.Div([html.P("Figure Width"),dcc.Slider(id='width', min=200, max=500, step=25, value=300, marks={x: str(x) for x in [200, 300, 400, 500]}),
    
]),
     ],className="create_container three columns"),

        html.Div([


        html.P("Enter the title"),
        dcc.Input(id="input-title", type="text", placeholder=""),

        html.P("Enter the x-axis"),
        dcc.Input(id="input-x", type="text", placeholder=""),

        html.P("Enter the y-axis"),
        dcc.Input(id="input-y", type="text", placeholder=""),

   

        ],className="create_container three columns"),

        html.Hr(),  # horizontal line

        
    ], className="row-flex display")


@callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'),
              State('zaxis-data', 'value'),
              State('chart-type', 'value'),
              Input('color-picker', 'value'),
              Input('width', 'value'),

              Input('input-title', 'value'),

              Input('input-x', 'value'),

              Input('input-y', 'value'),

              Input('radio', 'value'),

        


              )
def make_graphs(n, data, x_data, y_data, z_data, chart, color, width_size, title, xvalue, yvalue, radio):
    if n is None:
        return dash.no_update
    else:
        
        if chart == 'line':
        
            df = pd.DataFrame.from_dict(data)

            if radio == 'sum':
                data= df.groupby(x_data)[y_data].sum().reset_index()

            else:
                data= df.groupby(x_data)[y_data].count().reset_index()


            

            

            color_choice= list(color.items())[0][1]   #For color-picker



            fig = go.Figure(
            data=[

            go.Line(
                x=data[x_data],
                y=data[y_data],
                line=dict(color=f'{color_choice}', width=3),
            ),




            ],
            layout=go.Layout(
                xaxis=dict(
                title=f" <b> {xvalue} </b>",
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title=f" <b> {yvalue} </b>",
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            )
        )
    )
            fig.update_layout(
             title={
            'text': f'<b> {title} </b>'},
            title_font_size=20,
            autosize=True,
            # bargap=0.15, # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1, # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',

            width=int(width_size),
        )

            return dcc.Graph(figure=fig)

            

        elif chart == 'bar':

            df = pd.DataFrame.from_dict(data)

            if radio == 'sum':
                data= df.groupby(x_data)[y_data].sum().reset_index()

            else:
                data= df.groupby(x_data)[y_data].count().reset_index()



            


            ###Since the data is in the form of dictionary, to convert it into a datafreame, we will use the following code.
            

            color_choice= list(color.items())[0][1]   #For color-picker

            fig = go.Figure(
                data=[
                    go.Bar(
                        marker_color=f"{color_choice}",
                    
                        x=data[x_data],
                        y=data[y_data]),
               
            
                ],

                layout=go.Layout(
                xaxis=dict(
                title=f"<b> {xvalue} </b>",
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title=f" <b> {yvalue} </b>",
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            )
        )
                )            
     
            fig.update_layout(
              title={
            'text': f' <b> {title} </b>'},
            title_font_size=14,
            autosize=True,
            # bargap=0.15, # gap between bars of adjacent location coordinates.
            # bargroupgap=0.1, # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',

            width=int(width_size),
        )



            return dcc.Graph(figure=fig)



        elif chart == 'pie':


            df = pd.DataFrame.from_dict(data)

            if radio == 'sum':
                data= df.groupby(x_data)[y_data].sum().reset_index()

            else:
                data= df.groupby(x_data)[y_data].count().reset_index()

            
            pie_chart = px.pie(data, values=y_data, names=x_data)
            return dcc.Graph(figure=pie_chart)


        else:


            df = pd.DataFrame.from_dict(data)

            if radio == 'sum':
                data= df.groupby(x_data)[y_data].sum().reset_index()

            else:
                data= df.groupby(x_data)[y_data].count().reset_index()

            bubble = px.scatter(data, x=x_data, y=y_data, size= z_data, log_x=True, size_max=60)
            return dcc.Graph(figure=bubble)
