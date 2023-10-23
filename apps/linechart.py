# import dash_core_components as dcc
# import dash_html_components as html
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
from apps import commonmodules


layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    html.H3('Line Chart'),    
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
])