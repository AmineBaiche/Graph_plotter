import base64
import datetime
import io
from pydoc import classname

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash_extensions as de


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
                suppress_callback_exceptions=True)
url = "https://global-uploads.webflow.com/5dd3495558fd7f3d1fcb52bc/604633601a00eb7361ff6e5e_Growth.json"
opt = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
app.layout = html.Div([
    html.Div([de.Lottie(options=opt, width="50%", height="10%", url=url)
,
        html.H1("Online Graph Plotter",className="heading centered")
                ],className='box-column'),
                 html.Ul([
        html.Li("Online graph plotter is a graph maker tool that turns your csv or excel file into charts automatically"),
         html.Li("Uplaod your CSV or Excel file, the graph maker will automatically generate your charts"),
          html.Li("You can choose different charts "),
                    html.Li("Don't forget to choose you X axis and Y axis  "),]

        ),
        html.Div([ dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ],style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                'border': '2px dashed #14e4c5',
                
            },),
        # Allow multiple files to be uploaded
        multiple=True,
    ),
    html.Div(id='output-div'),
    html.Div(id='output-datatable')],className="box-column dropzone")
],className='box')


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),sep=None, engine='python')
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))
    else :
        return html.Div([
            'There was an error processing this file.'
        ])

    return  dbc.Row(
            [
                dbc.Col(dbc.Card(
    [
        html.Div(
            [
                dbc.Label("xaxis-data"),
                dcc.Dropdown(
                    id="xaxis-data",
                    options=[{'label':x, 'value':x} for x in df.columns
                    ],
                    value=df.columns[0],
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="yaxis-data",
                     options=[{'label':y, 'value':y} for y in df.columns
                    ],
                     value=df.columns[1],
                ),
            ]
        ),
         dbc.Label("Select your type of graph"),
         dcc.Dropdown(id='graph_type',
                     options=[{'label':"Bar", 'value':"bar"},
                     {'label': 'Line', 'value': "line"},  
                     {'label': 'Area', 'value': "area"},
                     {'label': 'Funnel', 'value': "funnel"},
                     {'label': 'scatter', 'value': "scatter"},
                     {'label': 'Ecdf', 'value': "ecdf"}   
                     ],value="bar"),
        html.P("Choose Color"),
        dcc.Dropdown(id='color',
                     options=[{'label':"Viridis", 'value':"Viridis"},
                     {'label': 'Line', 'value': "line"},  
                     {'label': 'Area', 'value': "area"},
                     {'label': 'Funnel', 'value': "funnel"},
                     {'label': 'Pie', 'value': "pie"},
                     {'label': 'Ecdf', 'value': "ecdf"}
                     ]),
        dbc.Button(id="submit-button", children="Create Graph",className="mb-3"),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

    ],
    body=True,
), md=19)   ],
            align="right",className='xxxx')


# html.Div([
#         html.H5(filename),
#         # html.H6(datetime.datetime.fromtimestamp(date)),
#         html.P("Insert X axis data"),
#         dcc.Dropdown(id='xaxis-data',
#                      options=[{'label':x, 'value':x} for x in df.columns], optionHeight=100),
#         html.P("Insert Y axis data"),
#         dcc.Dropdown(id='yaxis-data',
#                      options=[{'label':x, 'value':x} for x in df.columns], multi=True),
#         html.P("Choose Graph Type"),
#         dcc.Dropdown(id='graph_type',
#                      options=[{'label':"Bar", 'value':"bar"},
#                      {'label': 'Line', 'value': "line"},  
#                      {'label': 'Area', 'value': "area"},
#                      {'label': 'Funnel', 'value': "funnel"},
#                      {'label': 'Pie', 'value': "pie"},
#                      {'label': 'Ecdf', 'value': "ecdf"}   
#                      ]),
#         html.P("Choose Color"),
#         dcc.Dropdown(id='color',
#                      options=[{'label':"Bar", 'value':"bar"},
#                      {'label': 'Line', 'value': "line"},  
#                      {'label': 'Area', 'value': "area"},
#                      {'label': 'Funnel', 'value': "funnel"},
#                      {'label': 'Pie', 'value': "pie"},
#                      {'label': 'Ecdf', 'value': "ecdf"}
#                      ]),
#         dbc.Button(id="submit-button", children="Create Graph",className="mb-3"),
#         html.Hr(),

#         # dash_table.DataTable(
#         #     data=df.to_dict('records'),
#         #     columns=[{'name': i, 'id': i} for i in df.columns],
#         #     page_size=15
#         # ),
#         dcc.Store(id='stored-data', data=df.to_dict('records')),

#         html.Hr(),  # horizontal line

#         # For debugging, display the raw contents provided by the web browser
#         # html.Div('Raw Content'),
#         # html.Pre(contents[0:200] + '...', style={
#         #     'whiteSpace': 'pre-wrap',
#         #     'wordBreak': 'break-all'
#         # })
#     ],className="container")


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'),
              State('graph_type','value'),
              State('color','value'),

)
def make_graphs(n, data, x_data, y_data,type,color):
    
    if n is None:
        return dash.no_update
    else:
        line_fig =  getattr(px, type)(data, x=x_data, y=y_data)
        getattr(px, type)
        # print(line_fig)
        # if type =="line":
        #     line_fig = px.line(data, x=x_data, y=y_data)
        # elif type =="bar":
        #     line_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return   dbc.Col(dcc.Graph(figure=line_fig, config= {'displaylogo': False}),md=18)


if __name__ == '__main__':
    app.run_server(debug=True)