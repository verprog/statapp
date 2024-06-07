# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df_profile = commonmodules.df_profile
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

selector_date_flow = get_datepicker('date_picker_profile')
selector_provider = get_selector('provider_selector_profile', "Надавач підтримки", commonmodules.providerstp, True, False)
selector_typepro = get_selector('typepro_selector_profile', "Тип програми", commonmodules.typeprolstp, True, True)
selector_typesup = get_selector('typesup_selector_profile', "Назва програми", commonmodules.typesuplstp, True, False)


layout = html.Div([navbar,
                dbc.Card(
                        dbc.CardBody([
                            dbc.Row(dbc.Card(dbc.CardBody([selector_date_flow, selector_provider, selector_typepro, selector_typesup], className="row row-cols-auto mb-4 gap-3"))),
                            html.Br(),
                            dbc.Row(id='dash_tab_profile', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx_profile", className="dia-excel"),
                                     dcc.Download(id="download-xlsx-profile")], className="excelCol")],),
                        ]), color='light'
                    ),
                   footer
                ]
                )


@callback(Output('dash_tab_profile', 'children'),
          [Input("date_picker_profile", "start_date"),
           Input("date_picker_profile", "end_date"),
           Input('provider_selector_profile', 'value'),
           Input('typepro_selector_profile', 'value'),
           Input('typesup_selector_profile', 'value')],
          )
def store_data(start_date, end_date, provider, typepro, typesup):
    dfreestr = pd.read_parquet('apps/data/registerpayments.parquet.gzip')
    dfreestr = dfreestr[['Назва організації','Назва програми','Тип програми','Назва етапу','Номер етапу','Обсяг','ProgramAmountUnitOfMeasure',
    'Дата відправлення реєстру','Статус','Область','Район','Населений пункт','Реєстраційний номер заявки','Дата рєстрації заявки',
    'Реєстраційний номер','Дата реєстрації','Тип особи','Обсяг підтримки']]
    # dfreestr.rename(columns={k: k.replace(' ', '_') for k in dfreestr.columns if k.count(' ') > 0}, inplace=True)

    begin = start_date
    end = end_date
    # condprovider = " " if provider is None or provider == "" or provider == [] else "and (`organization` in (@provider))"
    # condtypepro = " " if typepro is None or typepro == "" or typepro == [] else "and (`TypeProgram` in (@typepro))"
    # condtypesup = " " if typesup is None or typesup == "" or typesup == [] else "and (`NameProgram` in (@typesup))"
    # filter_data = df_profile.query(f"(`CreateAt`>=@begin and `CreateAt`<=@end) {condprovider} {condtypepro} {condtypesup}")
    #
    # return get_table(filter_data,'table-filtering-profile')
    condprovider = " " if provider is None or provider == "" or provider == [] else "and (`Назва організації` in (@provider))"
    condtypepro = " " if typepro is None or typepro == "" or typepro == [] else "and (`Тип програми` in (@typepro))"
    condtypesup = " " if typesup is None or typesup == "" or typesup == [] else "and (`Назва програми` in (@typesup))"
    filter_data = dfreestr.query(f"(`Дата відправлення реєстру`>=@begin and `Дата відправлення реєстру`<=@end) {condprovider} {condtypepro} {condtypesup}")

    return get_table(filter_data,'table-filtering-profile')


@callback(
    Output("download-xlsx-profile", "data"),
    Input("btn_xlsx_profile", "n_clicks"),
    State("table-filtering-profile", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df) > 0:
        return dcc.send_data_frame(df.to_excel, f"Register payments data {now.strftime('%Y-%m-%d_%H%M%S')}.xlsx",
                                   sheet_name="Sheet_1", index=False)
