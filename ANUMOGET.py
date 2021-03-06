from config.MainConfig import get_config
from config.params import ANUMOGET, DataCols
from layout.body import get_layout
from proc import get_map, get_goes_map, get_dates_dropdown, get_ecmwf_map

from inout.reader import read_all_files, match_files_dates, read_ts_db
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

# https://dash.plot.ly/interactive-graphing
# https://plot.ly/python-api-reference/

config = get_config()
input_folder_re = config[ANUMOGET.input_folder_reanalisis]
input_folder_goes = config[ANUMOGET.input_folder_goes]
input_folder_ecmwf = config[ANUMOGET.input_folder_ecmwf]
ts_db_file_name = config[ANUMOGET.ts_db_file_name]
output_folder = config[ANUMOGET.output_folder]
ip = config[ANUMOGET.ip]
port = config[ANUMOGET.port]

print("Reading data....")
files = read_all_files(input_folder_re, input_folder_goes, input_folder_ecmwf)
# TODO restrict to BBOX, so that we only get the TS on the area of interest
BBOX = [4, -123.5, 38.5, -75]
hurdat_db_all = read_ts_db(ts_db_file_name, BBOX)
# ============= Code to save csv related with the dates =========
# Saving the desired ts
# hurdat_db_all.index.to_csv("/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/hurdat/DomainDates.csv",
#                         index=None)
# np_dates = hurdat_db_all[DataCols.time.value].apply(lambda x: x.strftime('%Y-%M-%d %H:%m:%S')).values
# np.savetxt("/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/hurdat/DomainDates.csv",
#             np_dates.astype(str), delimiter="'", fmt='%s')

# Shuffle dates
# Match dates to files
# http://www.meteo.unican.es/wiki/cordexwrf/OutputVariables
db = match_files_dates(files, hurdat_db_all)
app = get_layout('Awesome NUmerical MOdel Tagger (ANUMOGET)', db)

@app.callback(
    [Output('id-map-ecmwf-pres', 'figure'),
     Output('id-map-ecmwf-sfc', 'figure'),
     Output('id-map-goes-c4', 'figure'),
     Output('id-map-goes-c6', 'figure'),
     Output('id-map-unam-u', 'figure'),
     Output('id-map-unam-v', 'figure'),
     Output('id-map-unam-mag', 'figure'),
     Output('id-map-unam-psfc', 'figure'),
     Output('text_area', 'value')],
    [Input('dropdown', 'value'),
     Input('id-map-ecmwf-pres', 'selectedData'),
     Input('id-map-ecmwf-sfc', 'selectedData'),
     Input('id-map-goes-c4', 'selectedData'),
     Input('id-map-goes-c6', 'selectedData'),
     Input('id-map-unam-mag', 'selectedData'),
     Input('id-map-unam-psfc', 'selectedData'),
     Input('id-map-unam-u', 'selectedData'),
     Input('id-map-unam-v', 'selectedData'),
     ],
    [
    State('id-map-ecmwf-pres', 'figure'),
    State('id-map-ecmwf-sfc', 'figure'),
    State('id-map-goes-c4', 'figure'),
    State('id-map-goes-c6', 'figure'),
    State('id-map-unam-mag', 'figure'),
    State('id-map-unam-psfc', 'figure'),
    State('id-map-unam-u', 'figure'),
    State('id-map-unam-v', 'figure'),
     ])
def display_map(drop_value, selected_area_ecmwf_pres, selected_area_ecmwf_sfc, selected_area_goes4, selected_area_goes6, selected_area_map1, selected_area_map2, selected_area_map3, selected_area_map4,
                            map_state_ecmwf_pres, map_state_ecmwf_sfc, map_state_goes4, map_state_goes6, map_state_map1, map_state_map2, map_state_map3, map_state_map4):
    if not(drop_value is None or drop_value == ''):
        np_selected_area = np.array([selected_area_ecmwf_pres, selected_area_ecmwf_sfc,
                                     selected_area_goes4, selected_area_goes6,
                                     selected_area_map1, selected_area_map2,
                                     selected_area_map3, selected_area_map4])
        np_state = np.array([ map_state_ecmwf_pres,  map_state_ecmwf_sfc,
                             map_state_goes4,  map_state_goes6, map_state_map1,
                             map_state_map2, map_state_map3, map_state_map4])
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
        map_fig_ecmwf_pres, lats_lons = get_ecmwf_map(drop_value, selected_area, db, 'vo', center=center, zoom=zoom)
        map_fig_ecmwf_sfc, lats_lons = get_ecmwf_map(drop_value, selected_area, db, 'msl', center=center, zoom=zoom)
        map_fig_goes4, lats_lons = get_goes_map(drop_value, selected_area, db, 'C04', center=center, zoom=zoom)
        map_fig_goes6, lats_lons = get_goes_map(drop_value, selected_area, db, 'C04', center=center, zoom=zoom)
        map_fig_u, lats_lons = get_map(drop_value, selected_area, db, 'Q2', center=center, zoom=zoom)
        map_fig_v, lats_lons = get_map(drop_value, selected_area, db, 'RAINC', center=center, zoom=zoom)
        map_fig_mag, lats_lons = get_map(drop_value, selected_area, db, 'UV-MAG', center=center, zoom=zoom)
        map_fig_psfc, lats_lons = get_map(drop_value, selected_area, db, 'PSFC', center=center, zoom=zoom)
        if all_none:
            return map_fig_ecmwf_pres, map_fig_ecmwf_sfc, map_fig_goes4, map_fig_goes6, map_fig_u, map_fig_v, map_fig_mag, map_fig_psfc, 'Please make a selection'
        else:
            return map_fig_ecmwf_pres, map_fig_ecmwf_sfc, map_fig_goes4, map_fig_goes6, map_fig_u, map_fig_v, map_fig_mag, map_fig_psfc, lats_lons

@app.callback(
    [Output('dropdown', 'options'),
     Output('dropdown', 'value')],
    [Input('button', 'n_clicks')],
    [State('text_area', 'value')], )
def save_label(n_clicks, lats_lons):
    # READ/UPDATE DATABASE
    dropdown_options = get_dates_dropdown(db)
    value = dropdown_options[0]['value']
    return dropdown_options, value


# @app.callback(
#    [Output('id-map-goes-c4', 'selectedData'),
#     Output('id-map-goes-c6', 'selectedData'),
#     Output('id-map-mag', 'selectedData'),
#     Output('id-map-psfc', 'selectedData'),
#     Output('id-map-u', 'selectedData'),
#     Output('id-map-v', 'selectedData')],
#     [Input('button', 'n_clicks')])
# def clear_selection(n_clicks):

if __name__ == '__main__':
    # app.run_server(debug=False, port=8053, host='132.248.8.98:8053')
    app.run_server(debug=True, port=port, host=ip)
    # app.run_server(debug=False, port=8053, host='146.201.212.214') # COAPS
    # app.run_server(debug=False, port=8051, host='0.0.0.0') # ZION
