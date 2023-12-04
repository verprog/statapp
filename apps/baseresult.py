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


navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()
dfu = commonmodules.dfu
mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()
selector_period = get_datepicker('date_picker')
selector_type = get_selector('type_user_selector', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector', "Вибір регіонів", commonmodules.regionlst, True, True)

layout = html.Div([navbar,
                   dbc.Card(
                            dbc.CardBody([
                                dbc.Row(dbc.Card(dbc.CardBody([selector_period, selector_type, selector_region],
                                                              className="row row-cols-auto mb-4 gap-3"))),
                                html.Br(),
                                dbc.Row(id='dash_tab_map', align='center'),
                                html.Br(),
                                dbc.Row([dbc.Col(width=10),
                                         dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx", className="dia-button"),
                                         dcc.Download(id="download-xlsx-map")], width=2)], align='center'),
                            ]), color='light'
                        ),
                    footer
                    ])



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
