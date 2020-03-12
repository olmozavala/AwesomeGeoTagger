import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_layout(title):
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Link", href="#")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Temperature"),
                    dbc.DropdownMenuItem("Salinity"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Velocity"),
                ],
            ),
        ],
        brand=title,
        brand_href="#",
        sticky="top",
    )

    body = dbc.Container([
        # Global information
        dbc.Row([
            dbc.Col([
                html.H1("Awesome NUmerical MOdel Tagger (ANUMOGET)")
                    ], width=12)
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=[],
                    value=''
                ),
                ], width=6)
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="id-map",
                    figure={}
                ),
            ], width=8)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Textarea(
                    id='text_area',
                    value='Please make a selection'
                )
                ], width=10),
            dbc.Col([
                dbc.Button('Save', id='button')
                ], width=2)
            ])
        ], fluid=True)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([navbar, body])

    return app


