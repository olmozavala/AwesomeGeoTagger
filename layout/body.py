import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np

from proc import get_dates_dropdown
# https://dash.plotly.com/external-resources

def get_row_map( map_types, fields):
    tot_rows = np.amax([len(x) for x in fields])
    print(tot_rows)
    all_rows = []
    for c_row in np.arange(tot_rows):
        cols = []
        for i, map_type in enumerate(map_types):
            if len(fields[i]) > c_row:
                field = fields[i][c_row]
                cols.append(
                    dbc.Col([
                        dcc.Graph(
                            id=F"id-map-{map_type}-{field}",
                            figure={}
                        ),
                    ], width=4))
            else:
                cols.append(
                    dbc.Col([], width=4))
        all_rows.append(dbc.Row(cols))
    return dbc.Row(dbc.Col(all_rows, width=12, id='map_container'))

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
                    dbc.DropdownMenuItem("Maria Elena Osorio Tai", href="http://132.248.139.119/~tai/", external_link=True),
                    dbc.DropdownMenuItem("Jorge Eduardo Velasco Zavala", href="https://github.com/jorgeev/", external_link=True),
                    dbc.DropdownMenuItem("Raul De La Rosa", href="", external_link=True),
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
                html.H4('Select the tropical storm:')
            ], width=2),
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=get_dates_dropdown(db),
                    value=get_dates_dropdown(db)[0]['value']
                ),
            ], width=4),
            dbc.Col([
                dbc.Textarea(
                    id='text_area',
                    value='Make a selection with the Lasso tool'
                )
            ], width=4),
            dbc.Col([
                dbc.Button('Save', id='button')
            ], width=2)
        ], className='justify-content-center'),
        # Global information
        get_row_map(['goes', 'ecmwf', 'unam'],
                    [['c4','c6'], ['pres', 'sfc'], ['mag', 'psfc', 'u', 'v']]),
        ], fluid=True)

    # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
    # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                    assets_folder='css')
    app.scripts.config.serve_locally = False
    app.layout = html.Div([navbar, body])

    return app


