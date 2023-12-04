import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback
from apps import landbank, animals, supportflows, recipients, home, baseresult, profile,  commonmodules

app = dash.Dash(assets_folder='assets',
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Статистика ДАР',
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
    suppress_callback_exceptions=True
)
app._favicon = 'assets/favicon.ico'

server = app.server

# app.config.suppress_callback_exceptions = True
sidebar = commonmodules.get_sidebar()

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content],
                      style={'background-color': '#e2ecf4',
                             "min-height": "100vh",
                             "font-size": "12px"}
                      )

@app.callback(Output("page-content", "children"),
        [Input("url", "pathname")])
        # Output("id_header", "brand")
def render_page_content(pathname):
    nm = "Статистика ДАР"
    if pathname == "/base":
        return baseresult.layout #, f"{nm} - Основні результати"
    elif pathname == "/profile":
        return profile.layout #, f"{nm} - Профіль користувача"
    elif pathname == "/land":
        return landbank.layout #, f"{nm} - Земельний банк"
    elif pathname == "/animals":
        return animals.layout #, f"{nm} - Тварини"
    elif pathname == "/supportflows":
        return supportflows.layout #, f"{nm} - Аналіз напрямів підтримки"
    elif pathname == "/recipients":
        return recipients.layout #, f"{nm} - Перелік отримувачів"
    elif pathname == "/":
        return home.layout #, f"{nm}"
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
