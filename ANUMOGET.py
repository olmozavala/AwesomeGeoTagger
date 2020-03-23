from config.MainConfig import get_config
from config.params import ANUMOGET, DataCols
from layout.body import get_layout
from proc import get_map, get_dates_dropdown

from inout.reader import read_all_files, match_files_dates, read_ts_db
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

# https://dash.plot.ly/interactive-graphing
# https://plot.ly/python-api-reference/

COLORS = ['r', 'g', 'b', 'y']
date_format = '%Y-%m-%d'
date_format_ext = '%Y-%m-%dT%H:%M:%S'

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

config = get_config()
input_folder = config[ANUMOGET.input_folder]
ts_db_file_name = config[ANUMOGET.ts_db_file_name]
output_folder = config[ANUMOGET.output_folder]


print("Reading data....")
files = np.array(read_all_files(input_folder))
files.sort()

# TODO restrict to BBOX, so that we only get the TS on the area of interest
BBOX = [4, -123.5, 38.5, -75]
temp_db = read_ts_db(ts_db_file_name, BBOX)

# Shuffle dates
# Match dates to files
# http://www.meteo.unican.es/wiki/cordexwrf/OutputVariables
db = match_files_dates(files, temp_db)

app = get_layout('Awesome NUmerical MOdel Tagger (ANUMOGET)', db)

@app.callback(
    [Output('id-map-u', 'figure'),
     Output('id-map-v', 'figure'),
     Output('id-map-mag', 'figure'),
     Output('id-map-psfc', 'figure'),
     Output('text_area', 'value')],
    [Input('dropdown', 'value'),
     Input('id-map-mag', 'selectedData'),
     Input('id-map-psfc', 'selectedData'),
     Input('id-map-u', 'selectedData'),
     Input('id-map-v', 'selectedData'),
     ],
    [State('id-map-mag', 'figure'),
     State('id-map-psfc', 'figure'),
     State('id-map-u', 'figure'),
     State('id-map-v', 'figure'),
     ])
def display_map(drop_value, selected_area_map1, selected_area_map2, selected_area_map3, selected_area_map4,
                    map_state_map1, map_state_map2, map_state_map3, map_state_map4):
    if not(drop_value is None or drop_value == ''):
        np_selected_area = np.array([selected_area_map1, selected_area_map2, selected_area_map3, selected_area_map4])
        np_state = np.array([map_state_map1, map_state_map2, map_state_map3, map_state_map4])
        selection = [x is None for x in np_selected_area]
        all_none = np.all(selection)
        if not(all_none):
            selected_area = np_selected_area[np.logical_not(selection)][0]
        else:
            selected_area = None

        # Updating zoom and center
        if not (all_none):
            map_state = np_state[np.logical_not(selection)][0]
            center_dash = map_state['layout']['mapbox']['center']
            center = [center_dash['lon'], center_dash['lat']]
            zoom = map_state['layout']['mapbox']['zoom']
        else:
            center = [-94, 24]
            zoom = 3

        print(F'CENTER: {center}    ZOOOM: {zoom}')
        map_fig_u, lats_lons = get_map(drop_value, selected_area, db, 'Q2', center=center, zoom=zoom)
        map_fig_v, lats_lons = get_map(drop_value, selected_area, db, 'RAINC', center=center, zoom=zoom)
        map_fig_mag, lats_lons = get_map(drop_value, selected_area, db, 'UV-MAG', center=center, zoom=zoom)
        map_fig_psfc, lats_lons = get_map(drop_value, selected_area, db, 'PSFC', center=center, zoom=zoom)
        if all_none:
            return map_fig_u, map_fig_v, map_fig_mag, map_fig_psfc, 'Please make a selection'
        else:
            return map_fig_u, map_fig_v, map_fig_mag, map_fig_psfc, lats_lons

@app.callback(
    [Output('dropdown', 'options'),
    Output('dropdown', 'value')],
    [Input('button', 'n_clicks')],
    [State('text_area', 'value')],
     )
def save_label(n_clicks, lats_lons):
    # READ/UPDATE DATABASE
    dropdown_options = get_dates_dropdown(db)
    value = dropdown_options[0]['value']
    return dropdown_options, value


if __name__ == '__main__':
    # app.run_server(debug=False, port=8053, host='132.248.8.98:8053')
    app.run_server(debug=True, port=8051)
    # app.run_server(debug=False, port=8053, host='146.201.212.214')
