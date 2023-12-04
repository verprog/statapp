# Import necessary libraries
import geojson
import json
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker, df_prog
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Data TOP ratio
# df = px.data.iris()

df_top = df_prog.groupby('Region').agg({
    'DesiredAmount': 'sum',
    'ProvidedAmount': 'sum'
}).reset_index()
df_top['Region'] = df_top['Region'].str.replace('ОБЛАСТЬ', '')
disdf = df_top[['Region','DesiredAmount']].sort_values('DesiredAmount', ascending=True, ignore_index=True)[1:5]
# print(disdf.head(5))
prodf = df_top[['Region','ProvidedAmount']].sort_values('ProvidedAmount', ascending=True, ignore_index=True)[:5]
# print(prodf)
diseredict = {'pdf': disdf,
            'p_x':'DesiredAmount',
            'p_y':'Region',
            'pname':'ТОП 5 запрошеній допомозі'
            }

providedict = {'pdf': prodf,
            'p_x':'ProvidedAmount',
            'p_y':'Region',
            'pname':'ТОП 5 отриманю допомоги'
            }

def drawFigure(pdf,p_x,p_y, pname):
    return dcc.Graph(
                    figure=px.bar(
                        data_frame=pdf, x=p_x, y=p_y,title=pname,orientation='h'
                    ).update_layout(
                        # plot_bgcolor='rgba(0, 0, 0, 0)',
                        # paper_bgcolor='rgba(0, 0, 0, 0)',
                        xaxis=dict(
                            # categoryorder='array',
                            # categoryarray=None,
                            title=None  # Убираем подпись оси X
                        ),
                        yaxis=dict(
                            title=None  # Убираем подпись оси Y
                        )
                    ),
                    config={
                        'displayModeBar': False
                    }
                )


def drawText(pdata, pvalue):
    return html.Div([dbc.Card([dbc.CardHeader(pdata, style={'textAlign': 'center',
                                                            "font-family": "e-ukraine-heading"}),
                               dbc.CardBody([html.Div([html.H2(f"{pvalue:,.0f}"), ], style={'textAlign': 'center'})])]
                              ), ])


mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

layout = html.Div([navbar,
                   dbc.Card(
    dbc.CardBody([dbc.Row([dbc.Col([drawText(i[0], i[1])], width=3) for i in mapIndicator.values], align='center'),
                  html.Br(),
                  dbc.Row([
                            dbc.Col(dbc.Card([dbc.CardHeader('ТОП областей надання\отримання підтримки',style={'textAlign': 'center',"font-family": "e-ukraine-heading"}),
                                              dbc.CardBody(dbc.Row([dbc.Col(drawFigure(**diseredict), width=6),
                                                                    dbc.Col(drawFigure(**providedict), width=6)]))]
                                             ), width=6),
                            dbc.Col(dbc.Card([dbc.CardHeader('Мапа регіонів України',style={'textAlign': 'center',"font-family": "e-ukraine-heading"}),
                                              dbc.CardBody(dcc.Graph(id='choropleth_map', figure=fig, config={'scrollZoom': False}))]
                                             ),width=6),
                                    ], align='center')
                  ]), color='light',
                        style={'background-color': '#e7f5f5'}
                                ),
                    footer
                    ])
