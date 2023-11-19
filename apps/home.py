# Import necessary libraries
import geojson
import json
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Data
df = px.data.iris()


def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                )
            ])
        ),
    ])


def drawText(pdata, pvalue):
    return html.Div([dbc.Card([dbc.CardHeader(pdata, style={'textAlign': 'center'}),
                               dbc.CardBody([html.Div([html.H2(f"{pvalue:,.0f}"), ], style={'textAlign': 'center'})])]
                              ), ])


mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()

layout = html.Div([dbc.Card(
    dbc.CardBody([dbc.Row([dbc.Col([drawText(i[0], i[1])], width=3) for i in mapIndicator.values], align='center'),
                  html.Br(),
                  dbc.Row([dbc.Col([drawFigure()], width=6), dbc.Col([dbc.Card(
                      dbc.CardBody(dcc.Graph(id='choropleth_map', figure=fig, config={'scrollZoom': False})))],
                      width=6), ], align='center')
                  ]), color='light'
)
])
