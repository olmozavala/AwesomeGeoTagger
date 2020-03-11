from config.MainConfig import get_config
from config.params import ANUMOGET, DataCols
from layout.body import get_layout
from proc import get_map, get_dates_dropdown

from inout.reader import read_all_files, match_files_dates
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
output_folder = config[ANUMOGET.output_folder]


print("Reading data....")
files = read_all_files(input_folder)
data = [['10,9','Cat 4', '']]
db = pd.DataFrame(data, columns=[DataCols.center.value, DataCols.category.value, DataCols.netcdf_file.value],
                  index=[datetime(1981, 1, 1, 0, 0, 0)])

# Shuffle dates
# Match dates to files
db_full = match_files_dates(files, db)

app = get_layout('TITLE')


@app.callback(
    [Output('id-map', 'figure'),
     Output('text_area', 'value')],
    [Input('dropdown', 'value'),
     Input('id-map', 'selectedData'),
     ])
def display_figure(selected_file, selected_area):
    map_fig, lats_lons = get_map(selected_file, selected_area)
    if selected_area is None:
        return map_fig, 'Please make a selection'
    else:
        return map_fig, lats_lons

@app.callback(
    [Output('dropdown', 'options'),
     Output('dropdown', 'value')],
    [Input('button', 'n_clicks')],
    [State('text_area', 'value')],
     )
def display_figure(n_clicks, lats_lons):
    # READ/UPDATE DATABASE
    print(lats_lons)
    dropdown_options = get_dates_dropdown(db_full)
    value = dropdown_options[0]['value']
    return dropdown_options, value


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
    # app.run_server(debug=False, port=8053, host='146.201.212.214')
