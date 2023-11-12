# Import necessary libraries
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
from apps import commonmodules
from apps.commonmodules import get_table, get_selector, get_datepicker, get_rangearea
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Data
df = px.data.iris()

def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                )
            ])
        ),
    ])


def drawText(pdata,pvalue):
    return html.Div([dbc.Card([dbc.CardHeader(pdata, style={'textAlign': 'center'}),dbc.CardBody([html.Div([html.H2(f"{pvalue:,.0f}"),], style={'textAlign': 'center'})])]
                              ),])

df_prof = commonmodules.df_prof
mapIndicator = commonmodules.mapIndicator
fig = commonmodules.get_map()

selector_period = get_datepicker('date_picker_prof')
selector_type = get_selector('type_user_selector_prof', "Вибір особи", commonmodules.typelst, True, False)
selector_region = get_selector('region_selector_prof', "Вибір регіонів", commonmodules.regionlst, True, True)
selector_area = get_selector('area_selector_prof', "Вибір площі", commonmodules.arealst, False, False)
selector_gender = get_selector('gender_selector_prof', "Стать", commonmodules.genderlst, False, False)


layout = html.Div([
                dbc.Card(
                        dbc.CardBody([dbc.Row([ dbc.Col([drawText(i[0],i[1])], width=3) for i in mapIndicator.values], align='center'),
                            html.Br(),
                            dbc.Row(dbc.Card(dbc.CardBody([selector_period, selector_type, selector_region, selector_area, selector_gender], className="row row-cols-auto mb-4"))),
                            html.Br(),
                            dbc.Row([dbc.Col([drawFigure()], width=6),dbc.Col([dbc.Card(
                            dbc.CardBody(dcc.Graph(id='choropleth_map',figure=fig,config={'scrollZoom': False})))], width=6),], align='center'),
                            html.Br(),
                            dbc.Row(id='dash_tab_prof', align='center'),
                            html.Br(),
                            dbc.Row([dbc.Col(width=10),
                                     dbc.Col([dbc.Button("Download Excel", id="btn_xlsx_prof"),
                                     dcc.Download(id="download-xlsx-prof")], width=2)], align='center'),
                        ]), color='light'
                    )
                ])


@callback(Output('region_selector_prof', 'value'),
          [Input('choropleth_map', 'selectedData')],
          )
def store_data(selectedData):
    if selectedData is None:
        val = ''
        return val
    else:
        listlocation = [str(i['location']).upper() for i in selectedData['points']]
        return listlocation


@callback(Output('dash_tab_prof', 'children'),
          [Input("date_picker_prof", "start_date"),
           Input("date_picker_prof", "end_date"),
           Input('type_user_selector_prof', 'value'),
           Input('area_selector_prof', 'value'),
           Input('gender_selector_prof', 'value'),

           Input('region_selector_prof', 'value'),
           Input('choropleth_map', 'selectedData')],
          )
def store_data(start_date, end_date, typ, area, gender, regionsel, select):
    print(regionsel)
    begin, end = start_date, end_date
    rangeStr = get_rangearea(area)['start']
    rangeEnd = get_rangearea(area)['end']
    # listlocation = [str(i['location']).upper() for i in select['points']]
    condArea = " " if area is None or area == "" else "and (`Площа, га.`>=@rangeStr and `Площа, га.`<@rangeEnd)"
    condGen = " " if gender is None or gender == "" or gender == '-1' else "and `Стать` == @gender"
    condType = " " if typ is None or typ == "" else "and `Тип особи` == @typ"
    condRegion = " " if regionsel is None or regionsel == "" or regionsel == [] else "and Регіон == @regionsel"
    filter_data = df_prof.query(f"(`Дата реєстрації`>=@begin and `Дата реєстрації`<=@end) {condType} {condRegion} {condArea} {condGen}")

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
