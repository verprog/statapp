# Import necessary libraries
import geojson
import json
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker, df_prog
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Data TOP ratio
# df = px.data.iris()
csv_file_prog = 'apps/data/ProgramsData.csv'
df_prog = pd.read_csv(csv_file_prog)
df_prog['Region'] = df_prog['Region'].str.replace('ОБЛАСТЬ', '')
df_prog['iyear'] = pd.DatetimeIndex(df_prog['CreateAt']).year
df_top = df_prog.groupby(['iyear','Region']).agg({'DesiredAmount': 'sum','ProvidedAmount': 'sum'}).reset_index()

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
    return dbc.Col(dbc.Card([dbc.CardHeader(pdata, className="hederCard"),
                               dbc.CardBody([html.Div([html.H2(f"{pvalue:,.0f}"), ], style={'textAlign': 'center'}, className="bodyCard")])],
                    style={'min-width': '167px', 'min-height': '115px'}
                    ), className="col")


mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()
# dbc.Row(
#                         dbc.Stack(
#                             [card for _ in range(3)],
#                             direction='horizontal'
#                         )
layout = html.Div([navbar,
                dbc.Card(
                      dbc.CardBody([dbc.Row([drawText(i[0], i[1]) for i in mapIndicator.values], className="mb-4"),
                      html.Br(),
                      dbc.Row([
                          dbc.Col(dbc.Card([dbc.CardHeader('ТОП областей надання\отримання підтримки',
                                                           style={'textAlign': 'center',
                                                                  "font-family": "e-ukraine-heading"}),
                                            dbc.CardBody([
                                                dcc.RadioItems(id='radio_items',
                                                               labelStyle={"display": "inline-block"},
                                                               options=[
                                                                   {'label': 'TOP 5 наданю', 'value': 1},
                                                                   {'label': 'TOP 5 запрошено', 'value': 2}],
                                                               value=1,
                                                               style={'text-align': 'center', 'color': 'black'}, className='gap-3'),
                                                dcc.Graph(id='bartop_chart', config={'displayModeBar': False}),
                                                    html.P('Виберіть рік', style={'text-align': 'center', 'color': 'black'}),
                                                    dcc.Slider(id='slider_year',
                                                               included=False,
                                                               updatemode='drag',
                                                               tooltip={'always_visible': True},
                                                               min=2020,
                                                               max=2024,
                                                               step=1,
                                                               value=2023,
                                                               marks={str(yr): str(yr) for yr in range(2020, 2024, 1)},
                                                               ),
                                            ],
                                            )
                                            ],)
                                  ,className='colMapGraf'),
                                dbc.Col(dbc.Card([dbc.CardHeader('Мапа регіонів України',style={'textAlign': 'center',"font-family": "e-ukraine-heading"}),
                                                  dbc.CardBody(dcc.Graph(id='choropleth_map', figure=fig, config={'scrollZoom': False}),)]
                                                 ,),className='colMapGraf'),
                                        ], className="mb-4 row")
                      ]), color='light',
                          style={'background-color': '#e7f5f5'} #,style={'maxHeight': '612px'}, 'display': 'flex', 'flexDirection': 'row'
                    ),
                    footer
                    ]) #,       className="row flex-display"



@callback(Output('bartop_chart', 'figure'),
              [Input('slider_year', 'value')],
              [Input('radio_items', 'value')])
def update_graph(slider_year, radio_items):

    terr1 = df_prog.groupby(['Region', 'iyear'])[['DesiredAmount', 'ProvidedAmount']].sum().reset_index()

    terr2 = terr1[(terr1['iyear'] == slider_year)][['iyear', 'Region', 'DesiredAmount']].sort_values(by = ['DesiredAmount'], ascending = False).nlargest(5, columns = ['DesiredAmount']).reset_index()
    terr3 = terr1[(terr1['iyear'] == slider_year)][['iyear', 'Region', 'ProvidedAmount']].sort_values(by = ['ProvidedAmount'], ascending = False).nlargest(5, columns = ['ProvidedAmount']).reset_index()


    if radio_items == 1:
        dfbar = terr2[['DesiredAmount','Region']]
        dfbar = dfbar.rename(columns={'DesiredAmount':'value','Region':'region'})
    elif radio_items == 2:
        dfbar = terr3[['ProvidedAmount','Region']]
        dfbar = dfbar.rename(columns={'ProvidedAmount':'value','Region':'region'})

    return {
        'data':[go.Bar(
            x=dfbar['value'],
            y=dfbar['region'],
            text=dfbar['value'],
            texttemplate=dfbar['region'].astype(str) + ' ' + ':' + ' ' + '%{text:0s}' + ' ' + 'Грн.',
            textposition='auto',
            marker=dict(color='#007EFF' if radio_items == 1 else '#078331'),
            orientation='h',
            hoverinfo='text',
            width=0.5,
            # hovertext=
            # '<b>Country</b>: ' + terr2['country_txt'].astype(str) + '<br>' +
            # '<b>Year</b>: ' + terr2['iyear'].astype(str) + '<br>' +
            # '<b>Killed</b>: ' + [f'{x:,.0f}' for x in terr2['nkill']] + '<br>'

        )],


        'layout': go.Layout(
            # plot_bgcolor='#F2F2F2',
            # paper_bgcolor='#F2F2F2',
            hovermode='closest',
            height=360,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(title='<b></b>',
                       color='black',
                       showline=False,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       # linewidth=1,
                       ticks='',  # 'outside',
                       tickfont=dict(family='e-ukraine',size=10,color='black')
                       ),

            yaxis=dict(title='<b></b>',
                       autorange='reversed',
                       color='black',
                       showline=False,
                       showgrid=False,
                       showticklabels=False,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(family='e-ukraine',size=10,color='black')
                       ),

            legend={
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
                font=dict(family="e-ukraine",size=12,color='black',
            )
        )

    }