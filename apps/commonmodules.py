# from dash import dcc,html
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Import necessary libraries
# import geojson
from plotly.subplots import make_subplots
import json
import plotly.express as px
# import plotly.offline as plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table, dash
# import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash.dash_table.Format import Format, Scheme, Trim
from dash_iconify import DashIconify
import datetime
# pd.options.display.float_format = '{:,.2f}'.format


def get_app_assets(name):
    res = f"/assets/{name}"
    return res

def get_animal_gender(row):
    if row['SexName'] in ['Свинка', 'Коза', 'Ярка', 'Телиця', 'Вівцематка', 'Кобила', 'Корова', 'Свиноматка', 'Свинка (товарна)',
'Вівцематка', 'Кобила','Коза','Корова','Свинка','Свинка (товарна)','Свиноматка','Свиноматка (товарна)','Телиця','Ярка']:
        return 'Самиці'
    elif row['SexName'] in ['Цапи, козлики', 'Жеребець', 'Бугаєць,бугай', 'Кнур, кнурець', 'Барани, баранчики','Жеребець','Кнур, кнурець','Кнур, кнурець ',
'Кнур, кнурець (товарна)','Барани, баранчики','Бугаєць,бугай','Валухи','Мерин','Цапи, козлики']:
        return 'Самці'
    else:
        return 'Не опізнано'


now = datetime.datetime.now()
last_day = (now - datetime.timedelta(1))


csv_file_map = 'apps/data/base_result.parquet.gzip'
csv_file_prof = 'apps/data/UsersView.parquet.gzip'
csv_file_land = 'apps/data/LandData.parquet.gzip'
csv_file_animal = 'apps/data/AnimalData.parquet.gzip'
csv_file_prog = 'apps/data/ProgramsData.parquet.gzip'
csv_file_recip = 'apps/data/RecipientDate.parquet.gzip'

type_program = ['Пряме субсидування з Державного Бюджету','Надання грантів в рамках міжнародної фінансової допомоги','Підтримка фермерських господарств та інших виробників сільськогосподарської продукції']
# Прочитайте CSV-файл и создайте DataFrame
dfu = pd.read_parquet(csv_file_map)
df_prof = pd.read_parquet(csv_file_prof)
df_land = pd.read_parquet(csv_file_land)
df_animal = pd.read_parquet(csv_file_animal)
df_animal['AnimalGender'] = df_animal.apply(get_animal_gender, axis=1)
df_prog = pd.read_parquet(csv_file_prog).query('`TypeProgram` in (@type_program)')
df_profile = pd.read_parquet(csv_file_recip).query('`TypeProgram` in (@type_program)')

formatnum0 = dict(specifier=',.2f', locale=dict(separate_4digits=False))
columnsdict=\
[dict(id='registrationdate', name='Дата реєстрації'),
dict(id='RegistrationDate', name='Дата реєстрації'),
dict(id='RegistrationDate', name='Дата реєстрації'),
dict(id='catottg_region', name='Катоттг Область'),
dict(id='region', name='Регіон'),
dict(id='Region', name='Регіон'),
dict(id='catottg_district', name='Катоттг Район'),
dict(id='District', name='Район'),
dict(id='catottg_community', name='Катоттг Тер.Громада'),
dict(id='Community', name='Тариторіальна громада'),
dict(id='CreateAt', name='Дата подачі заявки'),
dict(id='TypeProgram', name='Тип програми'),
dict(id='NameProgram', name='Назва програми'),
dict(id='organization', name='Надавач підтримки'),
dict(id='legalform', name='Тип особи'),
dict(id='LegalForm', name='Тип особи'),
dict(id='KindName', name='КВЕД'),
dict(id='Purpose', name='КВЕД'),
dict(id='Id', name='Користувач'),
dict(id='Gender', name='Стать'),
dict(id='Group1LandParcelArea', name='Площа, га.', type='numeric', format=formatnum0),
dict(id='PropRight', name='Тип речового права'),
dict(id='Name', name='Вид тварини'),
dict(id='SexName', name='Назва'),
dict(id='AnimalGender', name='Стать'),
dict(id='TotalAmount', name='Бюджет програми', type='numeric', format=formatnum0),
dict(id='DesiredAmount', name='Запросили суму', type='numeric', format=formatnum0),
dict(id='ProvidedAmount', name='Отримана сума', type='numeric', format=formatnum0),
dict(id='giftamount', name='Надано підтримки, грн', type='numeric', format=formatnum0),
dict(id='cntuser', name='Кількість користувачів', type='numeric', format=formatnum0),
dict(id='area', name='Площа, га.', type='numeric', format=formatnum0),
dict(id='Area', name='Загальна площа землі', type='numeric', format=formatnum0),
dict(id='LandParcelCount', name='Площа землі у заявці', type='numeric', format=formatnum0),
dict(id='animal', name='Кіл-сть тварин', type='numeric', format=formatnum0),
dict(id='Animal', name='Кіл-сть тварин', type='numeric', format=formatnum0),
dict(id='AnimalCount', name='Кількість тварин у заявці', type='numeric', format=formatnum0),
dict(id='QuantityAnimal', name='Загальна кількість тварин', type='numeric', format=formatnum0),
dict(id='Subject', name='Субєкти', type='numeric', format=formatnum0),
dict(id='Назва організації', name='Назва організації'),
dict(id='Назва програми', name='Назва програми'),
dict(id='Тип програми', name='Тип програми'),
dict(id='Назва етапу', name='Назва етапу'),
dict(id='Номер етапу', name='Номер етапу'),
dict(id='Обсяг', name='Обсяг'),
dict(id='ProgramAmountUnitOfMeasure', name='Одиниці виміру допомоги'),
dict(id='Дата відправлення реєстру', name='Дата відправлення реєстру'),
dict(id='Сформував', name='Сформував'),
dict(id='Статус', name='Статус'),
dict(id='Область', name='Область'),
dict(id='Район', name='Район'),
dict(id='Населений пункт', name='Населений пункт'),
dict(id='Реєстраційний номер заявки', name='Реєстраційний номер заявки'),
dict(id='Дата рєстрації заявки', name='Дата рєстрації заявки'),
dict(id='Реєстраційний номер', name='Реєстраційний номер'),
dict(id='Дата реєстрації', name='Дата реєстрації'),
dict(id='Назва або ПІБ сільгосвиробника', name='Назва або ПІБ сільгосвиробника'),
dict(id='Тип особи', name='Тип особи'),
dict(id='Податковий номер', name='Податковий номер'),
dict(id='IBAN рахунку для виплат', name='IBAN рахунку для виплат'),
dict(id='Обсяг підтримки', name='Обсяг підтримки')]

df_profile[['NameProgram','TypeProgram','LegalForm','Id','Region','District','CreateAt',
'organization','DesiredAmount','ProvidedAmount','Area','LandParcelCount','QuantityAnimal','AnimalCount']]

df_prof = df_prof[['registrationdate','catottg_region','Region','catottg_district','District','LegalForm', 'Id', 'Gender', 'KindName', 'Group1LandParcelArea','DrfoCode']]
mapcolumn = {'area': 'Площа, га.', 'animal': 'Кількість тварин', 'giftamount': 'Надано підтримки, грн',
               'cntuser': 'Кількість кадастрових номерів'}

mapData_pre = dfu[['area', 'animal', 'giftamount', 'cntuser']]
mapData = mapData_pre.rename(columns=mapcolumn)

mapIndicator = pd.DataFrame(mapData.sum(axis=0, skipna=True)).reset_index()
mapIndicator.rename(columns={'index': 'DATA', 0: 'VALUE'}, inplace=True)

typelst = [x for x in dfu['legalform'].sort_values().unique()]
regionlst = [x.upper() for x in dfu['region'].sort_values().unique()]
kvedlst = [x for x in df_prof['KindName'].sort_values().unique()]
kvedlandlst = [x for x in df_land['Purpose'].sort_values().unique()]
rightlst = [x for x in df_land['PropRight'].sort_values().unique()]
animallst = [x for x in df_animal['Name'].sort_values().unique()]
genderanimallst = [x for x in df_animal['AnimalGender'].sort_values().unique()]
typeprolst = [x for x in df_prog['TypeProgram'].sort_values().unique()]
typesuplst = [x for x in df_prog['NameProgram'].sort_values().unique()]
typeprolstp = [x for x in df_profile['TypeProgram'].sort_values().unique()]
typesuplstp = [x for x in df_profile['NameProgram'].sort_values().unique()]
providerstp = [x for x in df_profile['organization'].sort_values().unique()]

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
            multi=multibool,
            className='data-bs-offset',
            # optionHeight=30
        )
    ], style={'min-width': '20em'}) #, 'padding-top': '3px'
    return selector

def get_datepicker(idname):
    datepicker_period = dcc.DatePickerRange(
                          id=idname,
                          first_day_of_week=1,
                          day_size=50,
                          min_date_allowed=datetime.date(2013, 1, 1),
                          max_date_allowed=last_day.date(),
                          initial_visible_month=last_day.date(),
                          start_date=last_day.replace(month=1).replace(day=1).date(),
                          end_date=last_day.date(),
                          display_format='DD.MM.YYYY',
                          style={'max-height': '25px', 'padding-top': '3px'})
    # datepicker_period = dmc.DateRangePicker(id=idname,
    #                                         firstDayOfWeek=1,
    #                                         minDate=datetime.date(2010, 1, 1),
    #                                         maxDate=last_day.date(),
    #                                         initialMonth=last_day.date(),
    #                                         value=[last_day.replace(day=1).replace(month=1).date(),last_day.date()],
    #                                         # style={"width": 330},
    #                                         locale="uk",
    #                                         )
    return datepicker_period


def get_table(data, idname):
    from dash import Dash
    from dash.html import Br, Div
    from dash.dash_table import DataTable
    from dash.dash_table.Format import Format, Group, Prefix, Scheme, Symbol
    format_table = dict(page_current=0,
                        page_size=20,
                        sort_action='native',
                        virtualization=True,
                        style_table={'overflowX': 'auto'},
                        style_header={"border": "1px solid black",
                                      "textAlign": "center",
                                      "font-family": "e-ukraine-heading",
                                      "font-weight": "700",
                                      "backgroundColor": "#e7eef3",
                                      "border": "1px solid #e7eef3"},#, 'fontWeight': 'bold'
                        style_cell={
                            # "minWidth": "180px",
                            # "width": "180px",
                            "maxWidth": "180px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            'textAlign': 'left',
                            # "maxWidth": 0
                            'font_family': 'e-ukraine',
                            'font_size': '11px',
                            "backgroundColor": "#fdfeff",
                            "border": "1px solid #e7eef3"
                        },
                        # {'textAlign': 'left'},

                        style_data_conditional=[
                            # {
                            #     'if': {
                            #         'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
                            #     },
                            #     'textAlign': 'left'
                            # },
                            {
                                    "if": {"row_index": "odd"},
                                    "backgroundColor": "#f8fbff",
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
    ls = data.columns
    lstcolumns = []
    for i in columnsdict:
        if i['id'] in ls:
            lstcolumns.append(i)

    return DataTable(fill_width=True, columns=lstcolumns, data=data.to_dict('records'), id=idname, **format_table)

def get_header():
    navbar = dbc.NavbarSimple(id="id_header",
        children=[
            dbc.NavItem(dbc.NavLink("Про ДАР", href="https://www.dar.gov.ua/about-dar",target="https://www.dar.gov.ua/about-dar",
                                    ), className="heada",
                        ),
            # dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.NavItem(dbc.NavLink("Новини", href="https://www.dar.gov.ua/news",target="https://www.dar.gov.ua/news",
                                    ), className="text-darck heada",
                        ),
            # dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.NavItem(dbc.NavLink("Корисне", href="https://www.dar.gov.ua/useful",target="https://www.dar.gov.ua/useful",
                                    ), className="text-darck heada",
                        ),
            # dmc.Divider(orientation="vertical", style={"height": 40}),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Номери для звязку", header=True),
                    dbc.DropdownMenuItem("044 339 92 15", href="tel:+380443399215"),
                    dbc.DropdownMenuItem("044 224 59 33", href="tel:+380442245933"),
                ],
                nav=True,
                in_navbar=True,
                label="Наші телефони",
                #style={"font-family": "e-ukraine-heading"}
                className="text-darck heada"
            ),
            dbc.Button("Увійти до кабінету", href="http://reg.dar.gov.ua",target="http://reg.dar.gov.ua",
                       className="dia-button",
                       ),
        ],
        brand=html.A(href="http://dar.gov.ua", target="http://dar.gov.ua", children=[html.Img(src=get_app_assets('logo_IP_SAR2.png'), height="50px")]),
        brand_href="http://dar.gov.ua",
        color='#e2ecf4',
        fluid=True,
        style={'background-color': '#e2ecf4', "color": "black", "font-family": "e-ukraine-heading","margin-top": '-10px',},) #, "margin-top": '-50px'

    return navbar


def get_menu():
    menu = html.Div([dbc.Col(width=8),
                     dbc.Col([
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
                   className="btn_sign js-btn_sign", #style={"height": "1cm"}
                   )]
                    )
    ], className="d-flex flex-row flex-md-row align-items-center p-3 px-md-4 mb-3 border-bottom shadow-sm",
        style={'background-color': '#e2ecf4', "color": "black"})
    return menu



styl = {
"padding": "7px 20px 6px 8px",
"display": "flex",
"align-items": "center",}

# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
def get_sidebar():
    sidebar_header = dbc.Row([
                        dbc.Col(html.H3("Панель навігації", style={"font-family": "e-ukraine-heading",
                                                                   'font-size': '20px','word-wrap': 'break-word'})),
                        dbc.Col(
                            [
                                html.Button(
                                    # use the Bootstrap navbar-toggler classes to style
                                    html.Span(className="navbar-toggler-icon"),
                                    className="navbar-toggler collapsed",
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
                                    className="navbar-toggler collapsed",
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
            dbc.Collapse(dmc.Menu([
            # dmc.MenuLabel("Application"),
            dmc.MenuDivider(style={"color": "#fff"}),
            dmc.MenuItem("Основні результати", icon=DashIconify(icon="mdi:home"), className="menu-item", href="/", ),
            # dmc.MenuItem("Основні результати", icon=DashIconify(icon="uis:layer-group"), className="menu-item", href="/base",),
            dmc.MenuItem("Профіль користувача", icon=DashIconify(icon="mdi:clipboard-user"), className="menu-item", href="/profile",),
            dmc.MenuItem("Земельний банк", icon=DashIconify(icon="pepicons-pop:earth-europe"), className="menu-item", href="/land",),
            dmc.MenuItem("Тварини", icon=DashIconify(icon="healthicons:animal-cow"), className="menu-item", href="/animals",),
            dmc.MenuItem("Аналіз напрямів підтримки", icon=DashIconify(icon="icon-park-outline:analysis"), className="menu-item", href="/supportflows",),
            dmc.MenuItem("Перелік отримувачів", icon=DashIconify(icon="fa6-solid:arrows-down-to-people"), className="menu-item", href="/recipients",),
            dmc.MenuDivider(),
                        ],
                        style={
                            "font-size": "12px",
                            "font-weight": "300",
                            "line-height": "5px",
                            "cursor": "pointer",
                            "font-family": "e-ukraine",
                            "text-color": "#fff",


                        }
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

                    dbc.NavLink([html.I(className="fa-solid fa-house me-2"), html.Span("Основні результати"), ],
                                href="/",
                                active="exact",
                                ),
                    # dbc.NavLink([html.I(className="fas fa-layer-group me-2"), html.Span("Основні результати"), ],
                    #             href="/base",
                    #             active="exact",
                    #             ),
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
        style={"font-family": "e-ukraine-heading"}
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
    colordict2 = {'Черкаська область': '#E2C89C',
            'Чернігівська область': '#429488',
            'Чернівецька область': '#A7D3AD',
            'Автономна Республіка Крим': '#255a95',
            'Дніпропетровська область': '#507776',
            'Донецька область': '#5A6063',
            'Івано-Франківська область': '#B2B58F',
            'Харківська область': '#2E6B74',
            'Херсонська область': '#4E80AD',
            'Хмельницька область': '#75C67D',
            'Київська область': '#7AD3C9',
            'м. Київ': '#DB9519',
            'Кіровоградська область': '#CCF2D3',
            'Луганська область': '#6AA1A5',
            'Львівська область': '#5E845E',
            'Миколаївська область': '#CADEE5',
            'Одеська область': '#AA906A',
            'Полтавська область': '#4295A5',
            'Рівненська область': '#0A634E',
            'м. Севастополь': '#C6D86E',
            'Сумська область': '#6AB4AC',
            'Тернопільська область': '#659B8D',
            'Закарпатська область': '#939367',
            'Вінницька область': '#71A361',
            'Волинська область': '#1C483F',
            'Запорізька область': '#818F99',
            'Житомирська область': '#A4EAE0',
            }
    fig = px.choropleth(df,
                        geojson=geometry,
                        featureidkey='properties.name',
                        locations="code",
                        color="label",
                        color_discrete_map=colordict2,
                        custom_data=[df['label'], df['crude_rate']],
                        hover_name=None,
                        hover_data=None,
                        fitbounds='geojson',
                        )

    fig.update_layout(  mapbox=dict(style='light',zoom=8 , center=dict(lat=48.3794, lon=31.1656),),
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        showlegend=False,
                        geo_scope="europe",
                        title='variable',
                        uirevision='constant',
                        clickmode='event', #'event+select'
                        coloraxis_showscale=False,
                        dragmode=False
                        )

    # hovertemp = '<i>Територія:</i> %{customdata[0]}<br><i>Код регіону:</i> %{customdata[1]}<br><i>Кіл-ть користувачів:</i> 111111<br><i>Кіл-ть тварин:</i> 3332<br>'
    hovertemp = "<br>".join([
                        "Код регіону:: %{customdata[1]}",
                        "Кіл-ть користувачів: 111111",
                        "Кіл-ть тварин: 3332",
                    ])


    fig.update_traces(hovertemplate=hovertemp)
    fig.update_layout(hovermode="closest")
    fig.update_geos(lonaxis_range=[40, 60], lataxis_range=[5, 10],) # projection_scale=0.5,
    fig.update_geos(fitbounds="locations", visible=False)

    # Добавьте точки для городов
    # fig.add_scattergeo(lat=df_sity['lon'],
    #                    lon=df_sity['lat'],
    #                    hoverinfo='none',
    #                    mode='text', #'markers+text'
    #                    # marker=dict(size=3, color='red'),  # Настройте размер и цвет точек
    #                    text='<b>' + df_sity['location_column'] +'</b>' ,  # Используйте названия городов для текста
    #                    # textposition='bottom right',   # Расположение текста
    #                    textposition='bottom center',   # Расположение текста
    # textposition = 'auto',
    #                    textfont=dict(size=6, color='black'),
    #                    )
    # fig.update_layout(
    #     autosize=True,
    #     width=1500,  # Установите желаемую ширину
    #     # height=800,  # Установите желаемую высоту
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

def get_selector2(idname, plholder, optionvalue,clerablebool, multibool):
    selector = dbc.DropdownMenu(children=[
                                    dcc.Checklist(
                                        options={
                                            '-1': 'Вібрати все',
                                            '0': ' Очистити',
                                        },
                                        value='',
                                        inline=True,
                                        className='gap-3',
                                        id=f'{idname}_all'),
                                    dmc.Space(h=30),
                                    dcc.Checklist(
                                        options=optionvalue,
                                        value='',
                                        className='gap-3',
                                        id=idname
                                    ),
                                ],
                                label=plholder,

                            )
    return selector

def get_size_label(length):
    if length <= 5:
        return '[0-5 га]'
    elif (length > 5 and length <= 120):
        return '[5-120 га]'
    elif (length > 120 and length <= 500):
        return '[120-500 га]'
    elif (length > 500 and length <= 1000):
        return '[500-1000 га]'
    else:
        return '[>1000 га]'

def get_fig_pieheatmap():
    respie = dfu.groupby(['legalform'])['cntuser'].sum().reset_index()

    def sortedx(inputStr):
        order = {'[0-5 га]': 1, '[5-120 га]':2, '[120-500 га]':3, '[500-1000 га]':4, '[>1000 га]':5}
        return order[inputStr]
    dfhot = df_prof
    dfhot['Group1LandParcelArea'].replace(np.nan, 0, regex=True, inplace=True)
    dfhot['Range'] = dfhot['Group1LandParcelArea'].map(get_size_label)
    dfhot['sorted'] = dfhot['Range'].map(sortedx)
    resultdf = dfhot.groupby(['LegalForm', 'Range', 'sorted'])['DrfoCode'].count().reset_index()
    fig = make_subplots(rows=2,specs=[[{"type": "pie"}, ],[{"type": "heatmap"}, ]])
    fig.add_trace(go.Pie(name='', values=respie['cntuser'], labels=respie['legalform'], hole=0.7,
                         hovertemplate="Кіл-ть: %{value}"), 1, 1)
    fig.update_traces(marker=dict(colors=['#4E80AD', '#A4EAE0', '#75C67D']))
    fig.update_traces(textposition='outside',textinfo='percent+label')

    resultdf.sort_values(['LegalForm', 'sorted'], inplace=True)
    fig.add_trace(go.Heatmap(name='', x=resultdf['Range'], y=resultdf['LegalForm'], z=resultdf['DrfoCode'],
                             text=[f'{x:,.0f}'.replace(',', ' ') for x in resultdf['DrfoCode']],
                             texttemplate="%{text}",showlegend=False, showscale=False, colorscale='mint',
                             hoverinfo='none',), 2, 1)

    fig.update_layout(margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ) #go.Margin
    )
    fig.update(layout_showlegend=False)
    return fig


# Footer section
def get_footer():
    footer = html.Footer(
        dbc.Container(
            [
                # dbc.Row([
                #
                #     dbc.Col([html.H1(children=['З питань роботи у ДАР звертайтесь до контакт-центру'],
                #                      className='h5 text-muted'),
                #              html.A("(044) 339-92-15", href="tel:+380443399215", target='_blank',
                #                     style={"color": "white"}),
                #              html.P([
                #                  html.A("(044) 224-59-33", href="tel:+380442245933",
                #                         target='_blank', className="order-1 align-items-end text-white"),
                #                  html.A(' , '),
                #                  html.A("support@dar.gov.ua", href="mailto:support@dar.gov.ua",
                #                         target='_blank', style={"color": "white"},
                #                         className="order-2 align-items-end text-white"),
                #              ]
                #              )],
                #             style={'margin-top': 20},
                #             width=6,
                #             className='d-flex align-items-end flex-column  gap-3')
                # ], className='d-flex',
                #     style={'height': '200px', "color": "white"}),

                dbc.Row(html.P([html.A("З питань роботи у ДАР звертайтесь до контакт-центру: (044) 339-92-15", className='text-white'),
                                html.A("support@dar.gov.ua", href="mailto:support@dar.gov.ua", target='_blank',
                                       className='text-white'), ]),
                        style={'width': '100%','height': '25px', "color": "white"},
                        className='d-inline-flex align-center text-white-50'),
                dbc.Row([
                    dbc.Col([html.Img(src=get_app_assets('trident.png'), style={'display': 'block', 'max-width': '60%','max-height': '60%',}),
                             html.P(children=['Міністерство аграрної політики та продовольства України'],
                                     style={'margin-left': '20', 'padding-left': '10px'}, className='h5'),
                             dmc.Divider(orientation="vertical", style={"height": 70}),
                             html.P(children=['Державний аграрний реєстр 2023. Всі права захищені'],
                                     style={'padding-left': '10px'}, className='h5'),

                             ], width=8, className='d-flex justify-content-start'),

                    dbc.Col([html.Img(src=get_app_assets('DiaLogo_02.png'), style={'display': 'inline-block', 'max-width': '60%','max-height': '60%',}),
                             html.P(
                                 children=['Створено з використанням дизайну Дія diia.gov.ua 2023. Всі права захищені'],
                                 style={'padding-left': '10px'}, className='h5'),
                             ],
                            width=4,
                            className='d-flex justify-content-end')],

                    style={'display': 'inline-block', 'height': '100px', 'padding': '10px', "color": "white"}, className='d-flex border-top'
                ),
            ]
        ),
        className='d-flex',  # fixed-bottom mt-auto position-sticky top-100
        style={
            'max-width': 'none',
            'padding-left': '4vw',
            'padding-right': '4vw',
            'display': 'block',
            'height': '125px',  # Set the fixed height of the footer here */
            # 'line-height': '60px', # Vertically center the text there */
            'background-color': 'black',
            'border-top-style': 'double',
            'border-top-color': '#1866B9',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'margin-top': 15
            , }

    )
    return footer

def get_footer2():
    footer = dbc.Container(children=[
                            # Первая строка
                            dbc.Row(html.P(["З питань роботи у ДАР звертайтесь до контакт-центру: (044) 339-92-15, ",
                                html.A("support@dar.gov.ua", href="mailto:support@dar.gov.ua", target='_blank', className='text-white')],
                                           ), className="footer-first-row"),

                            # Вторая строка
                            dbc.Row([
                                # Колонка 1 , width=3
                                dbc.Col([
                                    html.Img(src=get_app_assets('trident.png'), style={'display': 'inline-block', 'margin-top': '5px', 'max-height': '40px'}),
                                    html.P(children=['Міністерство аграрної політики та продовольства України'], style={'word-wrap': 'break-word','margin-top': '5px', 'padding-left': '5px'}),
                                         dmc.Divider(orientation="vertical", style={"height": '50'}),
                                         html.P(children=['Державний аграрний реєстр 2023. Всі права захищені'], style={'word-wrap': 'break-word','margin-top': '5px', 'padding-left': '5px'})
                                                ],
                                        width=7,
                                        # className='footer-column',
                                        style={'display': 'flex', 'flexDirection': 'row', 'text-align': 'center','overflow': 'hidden',}
                                    ),
                                # dbc.Col(width=4,),
                                # Колонка 2
                                dbc.Col([html.Img(src=get_app_assets('DiaLogo_02.png'), style={'display': 'inline-block', 'margin-top': '5px', 'max-height': '40px',}),
                                                html.P(children=['Створено з використанням дизайну Дія diia.gov.ua 2023. Всі права захищені'],
                                                style={'word-wrap': 'break-word','margin': '5px'}),
                                                ],
                                         width=5,
                                         # className='footer-column',
                                         style={'display': 'flex', 'flexDirection': 'row', 'text-align': 'left'}),
                            ],
                                className='d-flex',
                                style={'display': 'flex', 'border-top': '2px inset','font-size': '10px'}),
                        ],
                        fluid=True,
                        className='footer',
                    )
    return footer