# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df_flows = commonmodules.df_prog
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

selector_date_flow = get_datepicker('date_picker_flow')
selector_type = get_selector('type_user_selector_flows', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector_flows', "Вибір регіонів", commonmodules.regionlst, True, True)
selector_typepro = get_selector('typepro_selector_flows', "Тип програми", commonmodules.typeprolst, True, True)
selector_typesup = get_selector('typesup_selector_flows', "Назва програми", commonmodules.typesuplst, True, False)


layout = html.Div([navbar,
                dbc.Card(
                        dbc.CardBody([
                            dbc.Row(dbc.Card(dbc.CardBody([selector_date_flow, selector_type, selector_region, selector_typepro, selector_typesup], className="row row-cols-auto mb-4 gap-3"))),
                            html.Br(),
                            dbc.Row(id='dash_tab_flows', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col(width=10),
                                     dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx_flows", className="dia-excel"),
                                     dcc.Download(id="download-xlsx-flows")], width=2)], align='center'),
                        ]), color='light'
                    ),footer
                ])


@callback(Output('dash_tab_flows', 'children'),
          [Input("date_picker_flow", "start_date"),
           Input("date_picker_flow", "end_date"),
           Input('type_user_selector_flows', 'value'),
           Input('region_selector_flows', 'value'),
           Input('typepro_selector_flows', 'value'),
           Input('typesup_selector_flows', 'value')],
          )
def store_data(start_date, end_date, typ, regionsel, typepro, typesup):
    begin = start_date
    end = end_date
    condType = " " if typ is None or typ == "" else "and `LegalForm` == @typ"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and (`Region` in (@regionsel))"
    condtypepro = " " if typepro is None or typepro == "" or typepro == [] else "and (`TypeProgram` in (@typepro))"
    condtypesup = " " if typesup is None or typesup == "" or typesup == [] else "and (`NameProgram` in (@typesup))"
    filter_data = df_flows.query(f"(`CreateAt`>=@begin and `CreateAt`<=@end) {condType} {condRegion} {condtypepro} {condtypesup}")

    return get_table(filter_data,'table-filtering-flows')


@callback(
    Output("download-xlsx-flows", "data"),
    Input("btn_xlsx_flows", "n_clicks"),
    State("table-filtering-flows", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df) > 0:
        return dcc.send_data_frame(df.to_excel, f"Flows data {now.strftime('%Y-%m-%d_%H%M%S')}.xlsx",
                                   sheet_name="Sheet_1", index=False)
