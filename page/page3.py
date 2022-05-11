from dash import Dash, dcc, html, Input, Output, callback
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sklearn.svm import SVR



models = {'Regression': linear_model.LinearRegression,
          'Decision Tree': tree.DecisionTreeRegressor,
          'k-NN': neighbors.KNeighborsRegressor}


layout = html.Div([

    html.H2('Machine Learning Section', style={'text-align': 'center'}),

    
    html.H4("Predicting restaurant's revenue"),
    html.P("Select model:"),
    dcc.Dropdown(
        id='dropdown',
        options=["Regression", "Decision Tree", "k-NN"],
        value='Decision Tree',
        clearable=False
    ),
    dcc.Graph(id="graph"),

    html.H4("3D Visualization of Linear SVM"),

  

    html.Div([



dcc.Graph(id="graph2"),

    ],className="row flex-display")
])


@callback(
    Output("graph", "figure"), 
    Input('dropdown', "value"))
def train_and_display(name):
    df = px.data.tips() # replace with your own data source
    X = df.total_bill.values[:, None]
    X_train, X_test, y_train, y_test = train_test_split(
        X, df.tip, random_state=42)

    model = models[name]()
    model.fit(X_train, y_train)

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = go.Figure([
        go.Scatter(x=X_train.squeeze(), y=y_train, 
                   name='train', mode='markers'),
        go.Scatter(x=X_test.squeeze(), y=y_test, 
                   name='test', mode='markers'),
        go.Scatter(x=x_range, y=y_range, 
                   name='prediction')
    ])
    return fig

@callback(
    Output("graph2", "figure"), 
    Input('dropdown', "value"))

def graph(name):
    mesh_size = .02
    margin = 0

    df = px.data.iris()

    X = df[['sepal_width', 'sepal_length']]
    y = df['petal_width']

    # Condition the model on sepal width and length, predict the petal width
    model = SVR(C=1.)
    model.fit(X, y)

    # Create a mesh grid on which we will run our model
    x_min, x_max = X.sepal_width.min() - margin, X.sepal_width.max() + margin
    y_min, y_max = X.sepal_length.min() - margin, X.sepal_length.max() + margin
    xrange = np.arange(x_min, x_max, mesh_size)
    yrange = np.arange(y_min, y_max, mesh_size)
    xx, yy = np.meshgrid(xrange, yrange)

    # Run model
    pred = model.predict(np.c_[xx.ravel(), yy.ravel()])
    pred = pred.reshape(xx.shape)

    # Generate the plot
    fig = px.scatter_3d(df, x='sepal_width', y='sepal_length', z='petal_width')
    fig.update_traces(marker=dict(size=5))
    fig.add_traces(go.Surface(x=xrange, y=yrange, z=pred, name='pred_surface'))
    return fig

