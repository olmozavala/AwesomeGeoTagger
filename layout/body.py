import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from proc import get_dates_dropdown
# https://dash.plotly.com/external-resources

def get_layout(title, db):
    navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Olmo Zavala Romero", href="https://olmozavala.com/")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Authors",
                children=[
                    dbc.DropdownMenuItem("Olmo Zavala", href="https://olmozavala.com/", external_link=True),
                    # dbc.DropdownMenuItem(divider=True),
                ],
            ),
        ],
        brand=title,
        brand_href="#",
        sticky="top",
    )

    body = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4('Please select the tropical storm:')
            ], width=3),
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=get_dates_dropdown(db),
                    value=get_dates_dropdown(db)[0]['value']
                ),
            ], width=6)
        ],
        className='justify-content-center'
        ),
        # Global information
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="id-map-goes-c4",
                    figure={}
                ),
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    id="id-map-goes-c6",
                    figure={}
                ),
            ], width=6),
        ],
            className="bt-row"
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="id-map-mag",
                    figure={}
                ),
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    id="id-map-psfc",
                    figure={}
                ),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="id-map-u",
                    figure={}
                ),
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    id="id-map-v",
                    figure={}
                ),
            ], width=6)
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

    # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
    # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                    assets_folder='css')
    app.scripts.config.serve_locally = False
    app.layout = html.Div([navbar, body])

    return app


