# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df_land = commonmodules.df_land

navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

selector_type = get_selector('type_user_selector_land', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector_land', "Вибір регіонів", commonmodules.regionlst, True, True)
selector_kved = get_selector('kved_selector_land', "КВЕД", commonmodules.kvedlandlst, True, True)
selector_right = get_selector('right_selector_land', "Тип речового права", commonmodules.rightlst, True, False)


layout = html.Div([navbar,
                dbc.Card(
                        dbc.CardBody([
                            dbc.Row(dbc.Card(dbc.CardBody([selector_type, selector_region, selector_right, selector_kved], className="row row-cols-auto mb-4 gap-3"))),
                            html.Br(),
                            dbc.Row(id='dash_tab_land', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col(width=10),
                                     dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx_land", className="dia-button"),
                                     dcc.Download(id="download-xlsx-land")], width=2)], align='center'),
                        ]), color='light'
                    ),
                   footer
                ])


@callback(Output('dash_tab_land', 'children'),
          [Input('type_user_selector_land', 'value'),
           Input('region_selector_land', 'value'),
           Input('right_selector_land', 'value'),
           Input('kved_selector_land', 'value')],
          )
def store_data(typ, regionsel, right, kved):
    condType = " " if typ is None or typ == "" else "and `LegalForm` == @typ"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and (`Region` in (@regionsel))"
    condright = " " if right is None or right == "" or right == [] else "and (`PropRight` in (@right))"
    condkved = " " if kved is None or kved == "" or kved == [] else "and (`Purpose` in (@kved))"
    filter_data = df_land.query(f"(`LegalForm` !=-1) {condType} {condRegion} {condright} {condkved}")
    return get_table(filter_data,'table-filtering-land')


@callback(
    Output("download-xlsx-land", "data"),
    Input("btn_xlsx_land", "n_clicks"),
    State("table-filtering-land", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df) > 0:
        return dcc.send_data_frame(df.to_excel, f"Land data {now.strftime('%Y-%m-%d_%H%M%S')}.xlsx",
                                   sheet_name="Sheet_1", index=False)
