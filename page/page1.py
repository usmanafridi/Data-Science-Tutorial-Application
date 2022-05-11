import matplotlib.pyplot as plt
from pandas.plotting import table
from io import BytesIO
import base64
plt.switch_backend('agg')
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
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


df= pd.read_csv("datasets/austin_weather_updated.csv")





######### For converting Matplotlib Figure to Plotly Dash ###################


def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)


######################################################################







external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']





##### This is the main layout   ######

layout = html.Div([

    html.H2('Data Analysis Section',  className="h2", style={'text-align' : 'center'}),


 html.Button(id='submit-button', children='Display data', className="button"),

 html.Br(),
 
 html.Div([
        

        html.Div(id="table1"),
        
        ], className='row flex-display'), 


 html.Br(),



html.Button('Shape of data', id='button-1', n_clicks=0, className="button"), 


html.Div([

html.H2(id="shape-of-data", children=''),

], className='row flex-display'),


html.Button('Null values?', id='button-2', n_clicks=0, className="button"), 



html.Div([

html.H2(id="null-check-data", children='')

], className='row flex-display'),


html.Div([
html.H2(id="input-id", children='')
], className='row flex-display'),

###############################################################################
  html.Div([
    
    html.Button('What to do?', id='button-4', n_clicks=0, className="button"),
    
  
    html.Div(id='controls-container', children=[
        
        dcc.Dropdown(id='data-set-chosen', multi=False, value='none',
                     options=[{'label':'Drop Null Values', 'value':'drop'},
                              {'label':'Mean Imputation', 'value':'mean'}]),

        
       html.H2(id="shape-of-data2", children=''),
        
        
    ]),

  ],className="row-flex display"),

 html.Br(),

#################################################################################


html.Div([ 

    html.Button('Describe', id='button-3', n_clicks=0, className="button"), 

    html.Div([
    html.Div([html.Img(id = 'df-describe-plot', src = '')]), ])
            

  ],className="row-flex display"),


  html.Div([ 

      html.H6('Change the column type of the data set'),


    dcc.Dropdown(df.columns, id='pandas-dropdown-1', className="select"),

    dcc.RadioItems(id='radio-items', options=[
        {'label': 'Datetime', 'value': 'date'},
        {'label': 'Integer', 'value': 'int'},
        {'label': 'Float', 'value': 'float'},
        {'label': 'String', 'value': 'str'}
    ], 
),
    
    html.Div(id='pandas-output-container-1')


  ],className="row-flex display"),



  html.Div([ 

    html.H6('Change the column names'), 
            

  ],className="row-flex display"),



dcc.Store(id='store-data', data=[], storage_type='memory'), # 'local' or 'session'

dcc.Store(id='store-data-2', data=[], storage_type='memory') # 'local' or 'session'

########################Saving the Modified CSV file#########################################



])




################################################################

## This call back is to store the data in the second store component, after changing the column type.

@callback(Output('store-data-2', 'data'),
              Input('store-data', 'data'),
              Input("pandas-dropdown-1", "value"),
              Input("radio-items", "value"))

def change_data_type(data, value, radio):

    if data is None:
        raise PreventUpdate

    

    
    if radio == 'date':
        dff= pd.DataFrame(data)
        dff[value] =  pd.to_datetime(dff[value], errors='coerce')
        print('Changes to Datetime')

        # print(dff.info())

        return dff.to_dict('records')

    
    if radio == 'int':
        dff_int= pd.DataFrame(data)
        dff_int[value] = pd.to_numeric(dff_int[value], errors='coerce').astype('Int64')
        

        print('Value converted to integer')
        print(dff_int.info())

        df_new= pd.DataFrame(dff_int)
        
        return df_new.to_dict('records')

        
    
    else:
         None











#########################################################

@callback(
    Output('controls-container', 'style'),

    Input("button-4", "n_clicks"))

def update_graph(n_clicks):
    
    if n_clicks:
        
        return {'display': 'block'}
    else:
        return {'display': 'none'}


##########################################################

@callback(
    Output('store-data', 'data'),

    Input("data-set-chosen", "value"))

def update_graph(value):
    
    dff=df.copy()
    if value == 'drop':
        df_new= dff.dropna()
        return df_new.to_dict('records')


    else:
        df_new_mean= dff.fillna(dff.mean())
        return df_new_mean.to_dict('records')
        


##########################################################

@callback(Output('shape-of-data2', 'children'),
              Input('store-data', 'data'),
              Input("data-set-chosen", "value"))
def on_data_set_table(data, value):
    if data is None:
        raise PreventUpdate

    dff= pd.DataFrame(data)
    df_shape_check= dff.shape

    row=df_shape_check[0]
    column=df_shape_check[1]

    data_shape= f"There are {row} rows and {column} columns in the dataframe."

    if value == 'drop':
        return "The null values have been dropped.",html.Br(),data_shape

    if value == 'mean':
        return "The values have been mean imputed.",html.Br(), data_shape

    else:
        None



##########################################################


@callback(
    Output('shape-of-data', 'children'),
    Input("button-1", "n_clicks"))

def update_output(n_clicks):
    df1=df.copy()

    df_shape_check= df1.shape

    row=df_shape_check[0]
    column=df_shape_check[1]

    data_shape= f"There are {row} rows and {column} columns in the dataframe"
    
    if n_clicks:
        return data_shape

    else:
        None

###########################################################

@callback(
    Output('null-check-data', 'children'),

    Input("button-2", "n_clicks"))

def update_graph(n_clicks):
    df1=df.copy()
    df_null_check= df1.isnull().values.any()

    null_values= [html.H2('There are null values in the data set')]
    no_null_values= []

    if n_clicks:
        
        if df_null_check == True:
            
            return null_values
            
        
        else:
            return [
                html.H6('Warkaa dang 2')]
        
    
        

   


@callback(Output('table1','children'),
            [Input('submit-button','n_clicks')],
            [State('submit-button','n_clicks')])

def update_datatable(n_clicks,csv_file):            
    if n_clicks:                            
        data=df.copy()
        data = df.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns, page_current=0, page_size=1, page_action='custom', editable=False,
        
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        
        style_table={'overflowX':'scroll',
                     'maxHeight':'300px'},
        style_header={'backgroundColor':'white'},)



@callback(
    Output('df-describe-plot', 'src'),
    Input('button-3','n_clicks'),
)
def update_graph(n):
    if n:
        df1 = df.copy() 
        desc = df1.describe()
        fig,ax=plt.subplots(1,1, figsize=(10, 5))



#create a subplot without frame
        plot = plt.subplot(111, frame_on=False)

#remove axis
        plot.xaxis.set_visible(False) 
        plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
        table(plot, desc,loc='upper right') 

        out_url = fig_to_uri(fig) 

        return out_url
    else:
        None
            


