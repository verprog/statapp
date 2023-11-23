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
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table, dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash.dash_table.Format import Format, Scheme, Trim
import datetime




# pd.options.display.float_format = '{:,.2f}'.format

def get_app_assets(name):
    res = f"/assets/{name}"
    return res

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

formatnum0 = dict(specifier=',.2f', locale=dict(separate_4digits=False))
formatnum2 = dict(specifier=',.2f', locale=dict(separate_4digits=False))
columnsdict=\
[dict(id='registrationdate', name='Дата реєстрації'),
dict(id='RegistrationDate', name='Дата реєстрації'),
dict(id='region', name='Регіон'),
dict(id='Region', name='Регіон'),
dict(id='legalform', name='Тип особи'),
dict(id='LegalForm', name='Тип особи'),
dict(id='area', name='Площа, га.', type='numeric', format=formatnum2),
dict(id='Area', name='Загальна площа землі', type='numeric', format=formatnum2),
dict(id='animal', name='Кіл-сть тварин', type='numeric', format=formatnum0),
dict(id='Animal', name='Кіл-сть тварин', type='numeric', format=formatnum0),
dict(id='giftamount', name='Надано підтримки, грн', type='numeric', format=formatnum2),
dict(id='cntuser', name='Кількість користувачів', type='numeric', format=formatnum0),
dict(id='KindName', name='КВЕД'),
dict(id='Id', name='Користувач'),
dict(id='Gender', name='Стать'),
dict(id='Group1LandParcelArea', name='Площа, га.', type='numeric', format=formatnum2),
dict(id='PropRight', name='Тип речового права'),
dict(id='Purpose', name='КВЕД'),
dict(id='Subject', name='Субєкти', type='numeric', format=formatnum0),
dict(id='Name', name='Вид тварини'),
dict(id='SexName', name='Назва'),
dict(id='AnimalGender', name='Стать'),
dict(id='CreateAt', name='Дата подачі заявки'),
dict(id='TypeProgram', name='Тип програми'),
dict(id='NameProgram', name='Назва програми'),
dict(id='organization', name='Надавач підтримки'),
dict(id='TotalAmount', name='Бюджет програми', type='numeric', format=formatnum2),
dict(id='DesiredAmount', name='Запросили суму', type='numeric', format=formatnum2),
dict(id='ProvidedAmount', name='Отримана сума', type='numeric', format=formatnum2),
dict(id='LandParcelCount', name='Площа землі у заявці', type='numeric', format=formatnum2),
dict(id='AnimalCount', name='Кількість тварин у заявці', type='numeric', format=formatnum0),
dict(id='District', name='Район'),
dict(id='QuantityAnimal', name='Загальна кількість тварин', type='numeric', format=formatnum0),
]

df_profile[['NameProgram','TypeProgram','LegalForm','Id','Region','District','CreateAt',
'organization','DesiredAmount','ProvidedAmount','Area','LandParcelCount','QuantityAnimal','AnimalCount']]

df_prof = df_prof[['RegistrationDate','LegalForm', 'Region', 'Id', 'Gender', 'KindName', 'Group1LandParcelArea']]
mapcolumn = {'area': 'Площа, га.', 'animal': 'Кількість тварин', 'giftamount': 'Надано підтримки, грн',
               'cntuser': 'Кількість кадастрових номерів'}

mapData = dfu[['area', 'animal', 'giftamount', 'cntuser']]
mapData.rename(columns=mapcolumn, inplace=True)

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
            className='data-bs-offset'
        )
    ], style={'min-width': '20em'}) #, 'padding-top': '3px'
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


def get_table(data, idname):
    from dash import Dash
    from dash.html import Br, Div
    from dash.dash_table import DataTable
    from dash.dash_table.Format import Format, Group, Prefix, Scheme, Symbol
    format_table = dict(page_current=0,
                        page_size=20,
                        sort_action='native',
                        style_table={'overflowX': 'auto'},
                        style_header={'border': '1px solid black', 'textAlign': 'center', 'fontWeight': 'bold'},
                        style_cell={
                            # "minWidth": "180px",
                            # "width": "180px",
                            "maxWidth": "180px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            'textAlign': 'left',
                            # "maxWidth": 0
                            'font_family': 'e-Ukraine',
                            'font_size': '14px',
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



# Footer section
def get_footer():
    footer = html.Footer(
        dbc.Container(
            [
                dbc.Row([dbc.Col([
                    dbc.Row(html.H1(children=['Створено за підтримки:'], className='h3')),
                    dbc.Row(html.Img(src=get_app_assets('62f4e23dfe7a4e5f2534ec18_EU_logo_white.png')
                                     , style={'max-width': '18%',
                                              'vertical-align': 'middle',
                                              'display': 'inline-block', }
                                     )
                            )
                ],
                    style={'margin-top': 30},
                    width=6,
                    className='d-flex justify-content-start vstack gap-3'),

                    dbc.Col([html.H1(children=['З питань роботи у ДАР звертайтесь до контакт-центру'],
                                     className='h5 text-muted'),
                             html.A("(044) 339-92-15", href="tel:+380443399215", target='_blank',
                                    style={"color": "white"}),
                             html.P([
                                 html.A("(044) 224-59-33", href="tel:+380442245933",
                                        target='_blank', className="order-1 align-items-end text-white"),
                                 html.A(' , '),
                                 html.A("support@dar.gov.ua", href="mailto:support@dar.gov.ua",
                                        target='_blank', style={"color": "white"},
                                        className="order-2 align-items-end text-white"),
                             ]
                             )],
                            style={'margin-top': 30},
                            width=6,
                            className='d-flex align-items-end flex-column  gap-3')
                ], className='d-flex',
                    style={'height': '400px', "color": "white"}),

                dbc.Row([
                    dbc.Col([html.Img(src=get_app_assets('trident.png')),
                             html.H1(children=['Міністерство аграрної політики та продовольства України'],
                                     style={'margin-left': '20', 'padding-left': '10px'}, className='h5'),
                             dmc.Divider(orientation="vertical", style={"height": 70}),
                             html.H1(children=['Державний аграрний реєстр 2023. Всі права захищені'],
                                     style={'padding-left': '10px'}, className='h5'),

                             ], width=8, className='d-flex justify-content-start'),

                    dbc.Col([html.Img(src=get_app_assets('DiaLogo_02.png'), style={'max-width': '18%'}),
                             html.H1(
                                 children=['Створено з використанням дизайну Дія diia.gov.ua 2023. Всі права захищені'],
                                 style={'padding-left': '10px'}, className='h5'),
                             ],
                            width=4,
                            className='d-flex justify-content-end')],

                    style={'height': '100px', 'padding': '10px', "color": "white"}, className='d-flex border-top'
                ),
                dbc.Row(html.P([html.A("© 2023 All rights reserved. Contact us at: ", className='text-white-50'),
                                html.A("shenenko.av@gmail.com", href="mailto:shenenko.av@gmail.com", target='_blank',
                                       className='text-white-50'), ]),
                        style={'width': '100%','height': '25px', "color": "white"},
                        className='d-inline-flex align-self-center text-white-50')
            ]
        ),
        className='d-flex ',  # fixed-bottom mt-auto position-sticky top-100
        style={
            'max-width': 'none',
            'padding-left': '4vw',
            'padding-right': '4vw',
            'display': 'block',
            'height': '525px',  # Set the fixed height of the footer here */
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
