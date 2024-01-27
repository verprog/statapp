# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker, get_rangearea
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df_prof = commonmodules.df_prof
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

selector_period = get_datepicker('date_picker_prof')
selector_type = get_selector('type_user_selector_prof', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector_prof', "Вибір регіонів", commonmodules.regionlst, True, True)
selector_kved = get_selector('kved_selector_prof', "КВЕД", commonmodules.kvedlst, True, True)
selector_area = get_selector('area_selector_prof', "Вибір площі", commonmodules.arealst, False, False)
selector_gender = get_selector('gender_selector_prof', "Стать", commonmodules.genderlst, False, False)


layout = html.Div([navbar,
                dbc.Card(
                        dbc.CardBody([
                            dbc.Row(dbc.Card(dbc.CardBody([selector_period, selector_type, selector_region, selector_area, selector_gender, selector_kved], className="row row-cols-auto mb-4 gap-3"))),
                            html.Br(),
                            dbc.Row(id='dash_tab_prof', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx_prof", className="dia-excel"),
                                     dcc.Download(id="download-xlsx-prof")])], className="excelCol"),
                        ]), color='light'
                    ),
                footer
                ])


@callback(Output('dash_tab_prof', 'children'),
          [Input("date_picker_prof", "start_date"),
           Input("date_picker_prof", "end_date"),
           Input('type_user_selector_prof', 'value'),
           Input('area_selector_prof', 'value'),
           Input('gender_selector_prof', 'value'),
           Input('region_selector_prof', 'value')],
          )
def store_data(start_date, end_date, typ, area, gender, regionsel):
    begin, end = start_date, end_date
    areamin,areamax = get_rangearea(area)['start'],get_rangearea(area)['end']
    condArea = " " if area is None or area == "" else "and (`Group1LandParcelArea`>=@areamin and `Group1LandParcelArea`<@areamax)"
    condGen = " " if gender is None or gender == "" or gender == '-1' else "and `Gender` in (@gender)"
    condType = " " if typ is None or typ == "" else "and `LegalForm` in (@typ)"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and `Region` in (@regionsel)"
    filter_data = df_prof.query(f"(`RegistrationDate`>=@begin and `RegistrationDate`<=@end) {condType} {condRegion} {condArea} {condGen}")

    return get_table(filter_data,'table-filtering-prof')


@callback(
    Output("download-xlsx-prof", "data"),
    Input("btn_xlsx_prof", "n_clicks"),
    State("table-filtering-prof", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df) > 0:
        return dcc.send_data_frame(df.to_excel, f"Profile user {now.strftime('%Y-%m-%d_%H%M%S')}.xlsx",
                                   sheet_name="Sheet_1", index=False)
