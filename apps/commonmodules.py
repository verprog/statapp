from dash import dcc,html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Import necessary libraries
import geojson
import json
import plotly.express as px
import plotly.offline as plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash.dash_table.Format import Format, Scheme, Trim
import datetime


# pd.options.display.float_format = '{:,.2f}'.format


now = datetime.datetime.now()
last_day = (now - datetime.timedelta(1))

# Укажите путь к вашему CSV-файлу
csv_file_map = 'apps/data/base_result.csv'
csv_file_prof = 'apps/data/UsersView.csv'
csv_file_land = 'apps/data/LandData.csv'
csv_file_animal = 'apps/data/AnimalData.csv'
csv_file_prog = 'apps/data/ProgramsData.csv'
csv_file_recip = 'apps/data/RecipientDate.csv'

# Прочитайте CSV-файл и создайте DataFrame
dfu = pd.read_csv(csv_file_map)
df_prof = pd.read_csv(csv_file_prof)
df_prof['Group1LandParcelArea'].replace(np.nan,0, regex=True, inplace=True)
df_land = pd.read_csv(csv_file_land)
df_animal = pd.read_csv(csv_file_animal)
df_prog = pd.read_csv(csv_file_prog)
df_profile = pd.read_csv(csv_file_recip)


# using dictionary to convert specific columns
convert_dict_map = {
                    'region': str,
                    'legalform': str,
                    'area': int,
                    'animal': float,
                    'giftamount': int,
                    'cntuser': float,
                    }
convert_dict_prof = {
                    'Region': str,
                    'LegalForm': str,
                    'Group1LandParcelArea': int,
                    'Gender': str,
                    'KindName': str,
                    }
convert_dict_land = {
                    'Region': str,
                    'LegalForm': str,
                    'PropRight': str,
                    'Purpose': str,
                    'Area': float,
                    'Subject': int,
                    }
dfu = dfu.astype(convert_dict_map)
df_prof = df_prof.astype(convert_dict_prof)
df_land = df_land.astype(convert_dict_land)
dfu.rename(columns={'registrationdate': 'Дата реєстрації',
                            'region': 'Регіон',
                            'legalform': 'Тип особи',
                            'area': 'Площа, га.',
                            'animal': 'Кіл-сть тварин',
                            'giftamount': 'Надано підтримки, грн',
                            'cntuser': 'Кількість користувачів',}, inplace=True)

df_prof.rename(columns={'RegistrationDate': 'Дата реєстрації',
                            'KindName': 'КВЕД',
                            'Id': 'Користувач',
                            'Region': 'Регіон',
                            'LegalForm': 'Тип особи',
                            'Gender': 'Стать',
                            'Group1LandParcelArea': 'Площа, га.',}, inplace=True)

df_land.rename(columns={'PropRight': 'Тип речового права',
                            'Purpose': 'КВЕД',
                            'Region': 'Регіон',
                            'LegalForm': 'Тип особи',
                            'Area': 'Площа, га.',
                            'Subject': "Суб'єкти",}, inplace=True)

df_animal.rename(columns={ 'LegalForm': 'Тип особи',
                            'Region': 'Регіон',
                            'Name': 'Вид тварини',
                            'SexName': 'Назва',
                            'AnimalGender': 'Стать',
                            'animal': "Кіл-ть",}, inplace=True)

df_prog.rename(columns={ 'CreateAt': 'Дата подачі заявки',
                            'LegalForm': 'Тип особи',
                            'Region': 'Регіон',
                            'TypeProgram': 'Тип програми',
                            'NameProgram': 'Назва програми',
                            'organization': 'Надавач підтримки',
                            'TotalAmount': 'Бюджет програми',
                            'DesiredAmount': 'Запросили суму',
                            'ProvidedAmount': 'Отримана сума',
                            'LandParcelCount': 'Площа землі у заявці',
                            'AnimalCount': 'Кількість тварин у заявці',}, inplace=True)

df_profile[['NameProgram','TypeProgram','LegalForm','Id','Region','District','CreateAt',
'organization','DesiredAmount','ProvidedAmount','Area','LandParcelCount','QuantityAnimal','AnimalCount']]
df_profile.rename(columns={'NameProgram': 'Назва програми',
                        'TypeProgram': 'Тип програми',
                        'LegalForm': 'Тип особи',
                        'Id': "Користувач",
                        'Region': 'Регіон',
                        'District': 'Район',
                        'CreateAt': 'Дата подачі заявки',
                        'organization': 'Надавач підтримки',
                        'DesiredAmount': 'Запросили суму',
                        'ProvidedAmount': 'Отримана сума',
                        'Area': "Загальна площа землі",
                        'LandParcelCount': 'Площа землі у заявці',
                        'QuantityAnimal': "Загальна кількість тварин",
                        'AnimalCount': 'Кількість тварин у заявці',}, inplace=True)


df_prof = df_prof[['Дата реєстрації','Стать', 'Користувач', 'Тип особи', 'Регіон', 'КВЕД', 'Площа, га.']]

mapData = dfu[['Площа, га.', 'Кіл-сть тварин', 'Надано підтримки, грн', 'Кількість користувачів']]
mapIndicator = pd.DataFrame(mapData.sum(axis=0, skipna=True)).reset_index()
mapIndicator.rename(columns={'index': 'DATA', 0: 'VALUE'}, inplace=True)

typelst = [x for x in dfu['Тип особи'].sort_values().unique()]
regionlst = [x.upper() for x in dfu['Регіон'].sort_values().unique()]
kvedlst = [x for x in df_prof['КВЕД'].sort_values().unique()]
kvedlandlst = [x for x in df_land['КВЕД'].sort_values().unique()]
rightlst = [x for x in df_land['Тип речового права'].sort_values().unique()]
animallst = [x for x in df_animal['Вид тварини'].sort_values().unique()]
genderanimallst = [x for x in df_animal['Стать'].sort_values().unique()]
typeprolst = [x for x in df_prog['Тип програми'].sort_values().unique()]
typesuplst = [x for x in df_prog['Назва програми'].sort_values().unique()]
typeprolstp = [x for x in df_profile['Тип програми'].sort_values().unique()]
typesuplstp = [x for x in df_profile['Назва програми'].sort_values().unique()]
providerstp = [x for x in df_profile['Надавач підтримки'].sort_values().unique()]

arealst =[
           {'label': 'Всі дані', 'value': -1},
           {'label': 'до 5 га', 'value': 1},
           {'label': 'від 5 до 120 га', 'value': 2},
           {'label': 'від 120 до 500 га', 'value': 3},
           {'label': 'від 500 до 1000 га', 'value': 4},
           {'label': 'понад 1000 га', 'value': 5},
            ]
genderlst = [
           {'label': 'Всі гендери', 'value': '-1'},
           {'label': 'Чоловіча', 'value': 'Чоловіча'},
           {'label': 'Жіноча', 'value': 'Жіноча'},
            ]

def get_selector(idname, plholder, optionvalue,clerablebool, multibool):
    selector = html.Div([
        dcc.Dropdown(
            id=idname,
            placeholder=plholder,
            options=optionvalue,
            value='',
            clearable=clerablebool,
            multi=multibool
        )
    ], style={'min-width': '20em', 'padding-top': '3px'})
    return selector

def get_datepicker(idname):
    datepicker_period = dcc.DatePickerRange(
                          id=idname,
                          first_day_of_week=1,
                          day_size=50,
                          min_date_allowed=datetime.date(2010, 1, 1),
                          max_date_allowed=last_day.date(),
                          initial_visible_month=last_day.date(),
                          start_date=last_day.replace(day=1).replace(month=1).date(),
                          end_date=last_day.date(),
                          display_format='DD.MM.YYYY',
                            style={'max-height': '25px', 'padding-top': '3px'}
                      )
    return datepicker_period


def get_table(dataframe, idname):
    format_table = dict(page_current=0,
                        page_size=20,
                        sort_action='native',
                        style_table={'overflowX': 'auto'},
                        # style_cell={'textAlign': 'left'},
                        style_header={'border': '1px solid black', 'textAlign': 'center', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {
                                'if': {
                                    'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
                                },
                                'textAlign': 'left'
                            },
                            {
                                'if': {
                                    'column_type': 'numeric'  # 'text' | 'any' | 'datetime' | 'numeric'
                                },
                                'textAlign': 'right',
                                'format': Format(precision=4, scheme=Scheme.fixed, trim=Trim.yes)
                            },

                            {
                                'if': {
                                    'state': 'active'  # 'active' | 'selected'
                                },
                                'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                                'border': '1px solid rgb(0, 116, 217)'
                            }
                        ]
                        )
    data = dataframe.to_dict('records')
    columns = [{"name": i, "id": i, } for i in dataframe.columns]
    return dash_table.DataTable(data=data, columns=columns, id=idname, **format_table)

def get_header():
    # navbar = html.Div([
    #
    #     html.Div([
    #         html.H1(
    #             'Шапка сторінки з показниками програм')
    #     ], className="twelve columns padded"),
    #
    # ], className="row gs-header gs-text-header")
    navbar = dbc.NavbarSimple(id="id_header",
        children=[
            dbc.NavItem(dbc.NavLink("Про ДАР", href="https://www.dar.gov.ua/about-dar",className="menu_list-link"), className="menu_list-item"),
            dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.NavItem(dbc.NavLink("Новини", href="https://www.dar.gov.ua/news",className="menu_list-link"), className="menu_list-item"),
            dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.NavItem(dbc.NavLink("Корисне", href="https://www.dar.gov.ua/useful",className="menu_list-link"), className="menu_list-item"),
            dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Номери для звязку", header=True),
                    dbc.DropdownMenuItem("044 339 92 15", href="tel:+380443399215"),
                    dbc.DropdownMenuItem("044 224 59 33", href="tel:+380442245933"),
                ],
                nav=True,
                in_navbar=True,
                label="Наші телефони",
            ),
            dbc.Button("Увійти до кабінету", href="http://reg.dar.gov.ua",
                       className="btn_sign js-btn_sign", style={"height": "1cm"}
                       ),
        ],
        brand="Статистика ДАР",
        brand_href="#",
        # dark=True,
        className="bg-opacity-75 p-2 m-1 mx-auto bg-light text-dark fw-bold border rounded"
    )
    return navbar

def get_menu():
    menu = html.Div([

        dcc.Link("Про ДАР", href="https://www.dar.gov.ua/about-dar", target="https://www.dar.gov.ua/about-dar", className="p-2 text-dark"),
        dcc.Link("Новини", href="https://www.dar.gov.ua/news", target="https://www.dar.gov.ua/news", className="p-2 text-dark"),
        dcc.Link("Корисне", href="https://www.dar.gov.ua/useful",target="https://www.dar.gov.ua/useful", className="p-2 text-dark"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Номери для звязку", header=True),
                dbc.DropdownMenuItem("044 339 92 15", href="tel:+380443399215"),
                dbc.DropdownMenuItem("044 224 59 33", href="tel:+380442245933"),
            ],
            nav=True,
            in_navbar=True,
            label="Наші телефони",
        ),
        dbc.Button("Увійти до кабінету", href="http://reg.dar.gov.ua",
                   className="btn_sign js-btn_sign", style={"height": "1cm"}
                   )

    ], className="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm")
    return menu


# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
def get_sidebar():
    sidebar_header = dbc.Row([
                        dbc.Col(html.H3("Панель навігації", className="display-5")),
                        dbc.Col(
                            [
                                html.Button(
                                    # use the Bootstrap navbar-toggler classes to style
                                    html.Span(className="navbar-toggler-icon"),
                                    className="navbar-toggler",
                                    # the navbar-toggler classes don't set color
                                    style={
                                        "color": "rgba(0,0,0,.5)",
                                        "border-color": "rgba(0,0,0,.1)",
                                    },
                                    id="navbar-toggle",
                                ),
                                html.Button(
                                    # use the Bootstrap navbar-toggler classes to style
                                    html.Span(className="navbar-toggler-icon"),
                                    className="navbar-toggler",
                                    # the navbar-toggler classes don't set color
                                    style={
                                        "color": "rgba(0,0,0,.5)",
                                        "border-color": "rgba(0,0,0,.1)",
                                    },
                                    id="sidebar-toggle",
                                ),
                            ],
                            # the column containing the toggle will be only as wide as the
                            # toggle, resulting in the toggle being right aligned
                            width="auto",
                            # vertically align the toggle in the center
                            align="center",
                        ),
                    ]
                )
    sidebar = html.Div(
        [
            sidebar_header,
            # we wrap the horizontal rule and short blurb in a div that can be
            # hidden on a small screen
            html.Div(
                [
                    html.Hr(),
                    html.P(
                        "Виберіть розділ сайту",
                        className="lead",
                    ),
                ],
                id="blurb",
            ),
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavLink("Головна", href="/", active="exact"),
                        dbc.NavLink("Карта України", href="/map", active="exact"),
                        dbc.NavLink("Графіки", href="/linechart", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse",
                navbar=False
            ),
        ],
        id="sidebar",
    )
    return sidebar


def get_sidebar2():
    sidebar = html.Div(
        [
            html.Div(
                [
                    html.H2("SAR", style={"color": "white"}),
                    html.H2("statistics", style={"color": "white"})
                ],
                className="sidebar-header",
            ),
            html.Hr(),
            dbc.Nav(
                [

                    dbc.NavLink([html.I(className="fas fa-house me-2"), html.Span("Домашня сторінка"), ],
                                href="/",
                                active="exact",
                                ),
                    dbc.NavLink([html.I(className="fas fa-layer-group me-2"), html.Span("Основні результати"), ],
                                href="/base",
                                active="exact",
                                ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-clipboard-user me-2"), html.Span("Профіль користувача")],
                        href="/profile",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-earth-europe me-2"),html.Span("Земельний банк"),],
                        href="/land",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fa-solid fa-cow me-2"),html.Span("Тварини"),],
                        href="/animals",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-microscope me-2"),html.Span("Аналіз напрямів підтримки"),],
                        href="/supportflows",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fa-solid fa-arrows-down-to-people me-2"),html.Span("Перелік отримувачів"),],
                        href="/recipients",
                        active="exact",
                    ),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="sidebar",
    )
    return sidebar



# Load the data for MAP
with open("apps/data/ukraine.geojson", "r", encoding="utf-8") as f:
    geometry = json.load(f)

from geojson_rewind import rewind
geometry = rewind(geometry, rfc7946=False)

# Завантаження даних про міста
with open("apps/data/cities.geojson", "r", encoding="utf-8") as f:
    cities_geojson_data = json.load(f)

df_sity = pd.DataFrame({
    'lat': [feature['geometry']['coordinates'][0] for feature in cities_geojson_data['features']],
    'lon': [feature['geometry']['coordinates'][1] for feature in cities_geojson_data['features']],
    'location_column': [feature['properties']['name'] for feature in cities_geojson_data['features']],
})

df = pd.DataFrame({
    'code': [i['properties']['name'] for i in geometry['features']],
    'label': [i['properties']['name'] for i in geometry['features']],
    'crude_rate': [ind + 1 for ind, i in enumerate(geometry['features'])],
})

def get_map():
    # Create a choropleth map using Plotly Express
    fig = px.choropleth(df,
                        geojson=geometry,
                        featureidkey='properties.name',
                        locations="code",
                        color="crude_rate",
                        color_continuous_scale="Viridis",
                        hover_name="label",
                        title="GDP per Capita by Country",
                        labels={"crude_rate": "GDP per Capita"},
                        custom_data=[df['label'], df['crude_rate']],
                        # height=750, width=750

                        )

    fig.update_layout(  mapbox=dict(style='light', center=dict(lat=48.3794, lon=31.1656),),
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        showlegend=False,
                        geo_scope="europe",
                        title='variable',
                        uirevision='constant',
                        clickmode='event+select'
                        )

    hovertemp = '<i>Територія:</i> %{customdata[0]}<br><i>Код регіону:</i> %{customdata[1]}<br>'
    fig.update_traces(hovertemplate=hovertemp)
    fig.update_geos(fitbounds="locations", visible=False)
    # # fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(dragmode=False)
    fig.update_layout(mapbox=dict(style='light',zoom=8))
    # Добавьте точки для городов
    # fig.add_scattergeo(lat=df_sity['lon'],
    #                    lon=df_sity['lat'],
    #                    mode='markers+text',
    #                    marker=dict(size=10, color='red'),  # Настройте размер и цвет точек
    #                    text=df_sity['location_column'],  # Используйте названия городов для текста
    #                    textposition='bottom right')  # Расположение текста
    # fig.update_layout(
    #     autosize=False,
    #     width=1000,  # Установите желаемую ширину
    #     height=600,  # Установите желаемую высоту
    # )
    # plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    # fig.update_layout(
    #     autosize=False,
    #     margin=dict(
    #         l=0,
    #         r=0,
    #         b=0,
    #         t=0,
    #         pad=4,
    #         autoexpand=True
    #     ),
    #     # width=800,
    # #     height=400,
    # )
    return fig


def get_rangearea(num=-1):
    d = dict()
    if num == -1:
        area_start = 0
        area_end = 999999999
    elif num == 1:
        area_start = 0
        area_end = 5
    elif num == 2:
        area_start = 5
        area_end = 120
    elif num == 3:
        area_start = 120
        area_end = 500
    elif num == 4:
        area_start = 500
        area_end = 1000
    elif num == 5:
        area_start = 1000
        area_end = 999999999
    else:
        area_start = 0
        area_end = 999999999
    d['start'] = area_start
    d['end'] = area_end
    return d


dbc.DropdownMenu(
    children=[
        dcc.Checklist(
            options={
                '-1': 'Вібрати все',
                '0': ' Очистити',
            },
            value='',
            inline=True
        ),
        dmc.Space(h=30),
        dcc.Checklist(
            options={
                'NYC': 'New York City',
                'MTL': 'Montreal',
                'SF': 'San Francisco'
            },
            value=['MTL']
        ),
    ],
    label="menu",
),