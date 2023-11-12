# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from apps import commonmodules
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html


layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    html.Br(),
    html.H3('Головна сторінка'),
    html.H3('Опис діючих програм'),
])


# offcanvas = html.Div(
#     [
#         dbc.Button(
#             "Open scrollable offcanvas",
#             id="open-offcanvas-scrollable",
#             n_clicks=0,
#         ),
#         dbc.Offcanvas(
#             html.P("The contents on the main page are now scrollable."),
#             id="offcanvas-scrollable",
#             scrollable=True,
#             title="Scrollable Offcanvas",
#             is_open=False,
#         ),
#     ]
# )


# @app.callback(
#     Output("offcanvas-scrollable", "is_open"),
#     Input("open-offcanvas-scrollable", "n_clicks"),
#     State("offcanvas-scrollable", "is_open"),
# )
# def toggle_offcanvas_scrollable(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open