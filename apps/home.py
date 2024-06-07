# Import necessary libraries
import geojson
import json
import locale
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker, df_prog
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()
dfu = commonmodules.dfu
mapIndicator = commonmodules.mapIndicator
selector_period = get_datepicker('date_picker')
selector_type = get_selector('type_user_selector', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector', "Вибір регіонів", commonmodules.regionlst, True, True)

print(df_prog.columns)
# Data TOP ratio

df_prog['Region'] = df_prog['Region'].astype(str).str.replace('ОБЛАСТЬ', '')
df_prog['iyear'] = pd.DatetimeIndex(df_prog['CreateAt']).year
df_top = df_prog.groupby(['iyear','Region']).agg({'DesiredAmount': 'sum','ProvidedAmount': 'sum'}).reset_index()

def drawFigure(pdf,p_x,p_y, pname):
    return dcc.Graph(
                    figure=px.bar(
                        data_frame=pdf, x=p_x, y=p_y, title=pname, orientation='h',
                    ).update_layout(
                        # plot_bgcolor='rgba(0, 0, 0, 0)',
                        # paper_bgcolor='rgba(0, 0, 0, 0)',
                        xaxis=dict(title=None  # Убираем подпись оси X
                                    # categoryorder='array',
                                    # categoryarray=None,
                        ),
                        yaxis=dict(title=None  # Убираем подпись оси Y
                        )
                    ),
                    config={
                        'displayModeBar': False
                    }
                )


card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}


def drawText(pdata, pvalue):
    return dbc.Col([dbc.Card([dbc.CardHeader(pdata, className="hederCard"),
                               dbc.CardBody([html.Div([html.H3(f"{pvalue:,.0f}".replace(',', ' ')), ], style={'textAlign': 'center'}, className="bodyCard")])],
                    style={'min-width': '167px', 'min-height': '115px'}
                    ),],className="col")


mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()
figPie = commonmodules.get_fig_pieheatmap()
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()
# dbc.Row(
#                         dbc.Stack(
#                             [card for _ in range(3)],
#                             direction='horizontal'
#                         )
tooltip = dbc.Tooltip(
            "Приклад відображення "
            "підсказок при наведені та обьект",
            target="foolbody",
        )


layout = html.Div([navbar,
                dbc.Card(
                      dbc.CardBody([
                          dbc.Row(dbc.Col(
                              dbc.Card(
                                  [dbc.CardHeader('Мапа регіонів України',
                                                  style={'textAlign': 'center',"font-family": "e-ukraine-heading"}),
                                    dbc.CardBody(dcc.Graph(id='choropleth_map', figure=fig
                                                           ,config={'scrollZoom': False, 'displayModeBar': False}
                                                           ,style={'width': '100%', 'height': 'auto', 'margin': 'auto'}),
                                                 style={'max-height': '400px',
                                                         'width': '100%',
                                                         'height': 'auto',
                                                         'overflow': 'hidden',
                                                         'text-align': 'center'})
                                   ],)
                              # ,className="flex-row flex-wrap"
                          )
                          ),
                          html.Br(),
                          dbc.Row([drawText(i[0], i[1]) for i in mapIndicator.values], className="flex-row flex-wrap"),
                     html.Br(),
                      dbc.Row([
                          dbc.Col(dbc.Card([dbc.CardHeader('ТОП областей надання\отримання підтримки',
                                                           style={'textAlign': 'center',
                                                                  "font-family": "e-ukraine-heading"}),
                                            dbc.CardBody([
                                                dcc.RadioItems(id='radio_items',
                                                               # labelStyle={"display": "inline-block"},
                                                               options=[
                                                                   {'label': 'TOP 5 наданю', 'value': 1},
                                                                   {'label': 'TOP 5 запрошено', 'value': 2}],
                                                               value=1,
                                                               style={'text-align': 'center', 'color': 'black'}, inline=True, className='gap-3'),
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
                                dbc.Col(dbc.Card([dbc.CardHeader('Профіль користувача ДАР',style={'textAlign': 'center',"font-family": "e-ukraine-heading"}),
                                                  dbc.CardBody(dcc.Graph(id="graphPie", figure=figPie,
                                                            config={'displayModeBar': False}),)]
                                                 ,),className='colMapGraf'),], className="mb-4 row"),
                                html.Br(),
                                dbc.Row(dbc.Card(dbc.CardBody([selector_period, selector_type, selector_region],
                                                              className="row row-cols-auto mb-4 gap-3"))),
                                html.Br(),
                                dbc.Row(id='dash_tab_map', align='center'),
                                html.Br(),
                                dbc.Row(
                                    [dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx", className="dia-excel"),
                                              dcc.Download(id="download-xlsx-map")], className="excelCol")]),
                      ]), color='light',style={'background-color': '#e7f5f5'}, id='foolbody' ),
                    footer,tooltip],)



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
            # text=dfbar['value'],
            text=[f'{x:,.0f}'.replace(',', ' ') for x in dfbar['value']],
            texttemplate=dfbar['region'].astype(str) + ': ' + '%{text}' + ' грн',
            textposition='auto',
            marker=dict(color='#7AD3C9' if radio_items == 1 else '#75C67D'),
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



@callback(Output('dash_tab_map', 'children'),
          [Input("date_picker", "start_date"),
           Input("date_picker", "end_date"),
           Input('type_user_selector', 'value'),
           Input('region_selector', 'value')],
          )
def store_data(start_date, end_date, typ, regionsel):
    begin = start_date
    end = end_date
    condType = " " if typ is None or typ == "" else "and `legalform` in (@typ)"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and `region` in (@regionsel)"
    filter_data = dfu.query(f"(`registrationdate`>=@begin and `registrationdate`<=@end) {condType} {condRegion}")

    return get_table(filter_data,'table-sorting-filtering')

@callback(
    Output("download-xlsx-map", "data"),
    Input("btn_xlsx", "n_clicks"),
    State("table-sorting-filtering", "data"),
    prevent_initial_call=True,
)
def func(n_clicks,table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df)>0:
        return dcc.send_data_frame(df.to_excel, f"Map data {now.strftime('%Y-%m-%d_%H%M%S') }.xlsx", sheet_name="Sheet_1", index=False)

