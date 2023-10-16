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
from dash import Dash, dcc, html, Output, Input, State, callback, no_update, dash_table
import dash_ag_grid as dag
from dash.dash_table.Format import Format, Scheme, Trim

# Укажите путь к вашему CSV-файлу
csv_file_path = 'apps/data/base_result.csv'
# Прочитайте CSV-файл и создайте DataFrame
dfu = pd.read_csv(csv_file_path)
dfu.rename(columns={'registrationdate': 'Дата реєстрації',
                            'region': 'Регіон',
                            'legalform': 'Тип особи',
                            'area': 'Площа, га.',
                            'animal': 'Кіл-сть тварин',
                            'giftamount': 'Надано підтримки, грн',
                            'cntuser': 'Кількість користувачів'}, inplace=True)

mapData = dfu[['Площа, га.', 'Кіл-сть тварин', 'Надано підтримки, грн', 'Кількість користувачів']]
mapIndicator = pd.DataFrame(mapData.sum(axis=0, skipna=True)).reset_index()
mapIndicator.rename(columns={'index': 'DATA', 0: 'VALUE'}, inplace=True)

selector_type = html.Div([
    dcc.Dropdown(
        id='type_user_selector',
        options=[x for x in dfu['Тип особи'].unique()],
        value='',
        clearable=True,
        # multi=True
    )
], style={'width': '15em'})


selector_region = html.Div([
    dcc.Dropdown(
        id='region_selector',
        options=[x.upper() for x in dfu['Регіон'].sort_values().unique()],
        value='',
        clearable=True,
        multi=True
    )
], style={'min-width': '20em'})


def get_table(dataframe):
    format_table = dict(page_current=0,
                        page_size=10,
                        sort_action='native',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left'},
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
    columns = [{"name": i, "id": i, } for i in (dataframe.columns)]
    return dash_table.DataTable(data=data, columns=columns, id='table-sorting-filtering', **format_table)



def get_header():
    # navbar = html.Div([
    #
    #     html.Div([
    #         html.H1(
    #             'Шапка сторінки з показниками програм')
    #     ], className="twelve columns padded"),
    #
    # ], className="row gs-header gs-text-header")
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Про ДАР", href="https://www.dar.gov.ua/about-dar")),
            dbc.NavItem(dbc.NavLink("Новини", href="https://www.dar.gov.ua/news")),
            dbc.NavItem(dbc.NavLink("Корисне", href="https://www.dar.gov.ua/useful")),
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
            dbc.NavItem(dbc.NavLink("Увійти до кабінету", href="http://reg.dar.gov.ua")),
        ],
        brand="Статистика ДАР",
        brand_href="#",
        # dark=True,
        className="bg-opacity-75 p-2 m-1 mx-auto bg-light text-dark fw-bold border rounded"
    )
    return navbar

def get_menu():
    menu = html.Div([

        dcc.Link('Home   ', href='/', className="p-2 text-dark"),
        dcc.Link('Line Chart   ', href='/linechart', className="p-2 text-dark"),
        dcc.Link('Bar Chart   ', href='/barchart', className="p-2 text-dark"),
        dcc.Link('Scatterplot    ', href='/scatterplot', className="p-2 text-dark"),

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

                    dbc.NavLink([html.I(className="fas fa-layer-group me-2"), html.Span("Основні результати"), ],
                                href="/map",
                                active="exact",
                                ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-clipboard-user me-2"), html.Span("Профіль користувача")],
                        href="/",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-earth-europe me-2"),html.Span("Земельний банк"),],
                        href="/projects",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fa-solid fa-cow me-2"),html.Span("Тварини"),],
                        href="/animals",
                        active="exact",
                    ),
                    dbc.NavLink([html.I(className="fas fa-solid fa-microscope me-2"),html.Span("Аналіз напрямів підтримки"),],
                        href="/supportareas",
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

    hovertemp = '<i>Територія:</i> %{customdata[0]}<br><i>Şehir Statüsü:</i> %{customdata[1]}<br>'
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
    return fig


