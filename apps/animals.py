# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df_animal = commonmodules.df_animal
navbar = commonmodules.get_header()
footer = commonmodules.get_footer2()

selector_type = get_selector('type_user_selector_animal', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector_animal', "Вибір регіонів", commonmodules.regionlst, True, True)
selector_animal = get_selector('animal_selector_animal', "Вид тварини", commonmodules.animallst, True, True)
selector_gender = get_selector('genderanimal_selector_animal', "Стать", commonmodules.genderanimallst, True, False)


layout = html.Div([navbar,
                dbc.Card(
                        dbc.CardBody([
                            dbc.Row(dbc.Card(dbc.CardBody([selector_type, selector_region, selector_animal, selector_gender], className="row row-cols-auto mb-4 gap-3"))),
                            html.Br(),
                            dbc.Row(id='dash_tab_animal', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col([dbc.Button("Завантажити Excel", id="btn_xlsx_animal", className="dia-excel"),
                                     dcc.Download(id="download-xlsx-animal")], className="excelCol")],),
                        ]), color='light'
                    ),
                   footer
                ])


@callback(Output('dash_tab_animal', 'children'),
          [Input('type_user_selector_animal', 'value'),
           Input('region_selector_animal', 'value'),
           Input('animal_selector_animal', 'value'),
           Input('genderanimal_selector_animal', 'value')],
          )
def store_data(typ, regionsel, animal, gender):
    condType = " " if typ is None or typ == "" else "and `LegalForm` == @typ"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and (`Region` in (@regionsel))"
    condanimal = " " if animal is None or animal == "" or animal == [] else "and (`Name` in (@animal))"
    condgender = " " if gender is None or gender == "" or gender == [] else "and (`AnimalGender` in (@gender))"
    filter_data = df_animal.query(f"(`LegalForm` !=-1) {condType} {condRegion} {condanimal} {condgender}")

    return get_table(filter_data,'table-filtering-animal')


@callback(
    Output("download-xlsx-animal", "data"),
    Input("btn_xlsx_animal", "n_clicks"),
    State("table-filtering-animal", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, table_data):
    import datetime
    now = datetime.datetime.now()
    df = pd.DataFrame.from_dict(table_data)
    if len(df) > 0:
        return dcc.send_data_frame(df.to_excel, f"Animal data {now.strftime('%Y-%m-%d_%H%M%S')}.xlsx",
                                   sheet_name="Sheet_1", index=False)
