import xarray as xr
from colorcet import *
import datashader.transfer_functions as tf
import dash_core_components as dcc
from config.params import DataCols
import pandas as pd

date_format_ext = '%Y-%m-%dT%H:%M:%S'

def get_map(id, selection, db):
    """
    This function will generate the proper dash map with the selected
    date and, if the user has already draw something, it will add the points.
    :param selected_file:
    :param selection:
    :return:
    """
    # print(selection)

    selected_file = db.iloc[id][DataCols.netcdf_file.value]
    coords_file = db.iloc[id][DataCols.cords_file.value]

    agg = xr.open_dataset(selected_file, decode_times=False)
    cur_xr_ds_coords = xr.open_dataset(coords_file, decode_times=False)
    # agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
    LAT = cur_xr_ds_coords.XLAT.values[0, :, 0]
    LON = cur_xr_ds_coords.XLONG.values[0, 0, :]
    # LAT = np.arange(31, 18, -(1/len(LAT)))
    # LONS = np.arange(-74, -99, -(1/len(coords_lon)))
    # Corners of the image, which need to be passed to mapbox
    # coordinates = [[LON[0], LAT[0]],
    #                [LON[-1], LAT[0]],
    #                [LON[-1], LAT[-1]],
    #                [LON[0], LAT[-1]]]
    coordinates = [[LON[0], LAT[-1]],
                   [LON[-1], LAT[-1]],
                   [LON[-1], LAT[0]],
                   [LON[0], LAT[0]]]

    ds = xr.Dataset(
        {
            "SST": (("time", "lat", "lon"), agg['SST'].values.astype(int))
        },
        {"time": agg['Time'].values,
         "lat": cur_xr_ds_coords['XLAT'].values[0,:,0],
         "lon": cur_xr_ds_coords['XLONG'].values[0,0,:],
         },
    )

    hour = int(db.iloc[id][DataCols.time.value].strftime('%H'))

    img = tf.shade(ds['SST'][hour,:,:], cmap=bmy, alpha=150).to_pil()

    center = [24, -94]
    center_storm = [db.iloc[id]['lat'], db.iloc[id]['lon']]
    data = [
        dict(
            lat=[center_storm[0]],
            lon=[center_storm[1]],
            text=['text'],
            type="scattermapbox",
            customdata=['custom'],
            # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
            # fill="none", # none, toself, (only toself is working
            marker=dict(
                color='green'
            ),
            hovertemplate='Station: %{text} <extra></extra>'
        )
    ]

    lats_lons = ''
    if not(selection is None):
        all_locs = selection['lassoPoints']['mapbox']
        lats = [x[1] for x in all_locs]
        lons = [x[0] for x in all_locs]
        # print(F'lats: {lats}, \n lons: {lons}')
        lats_lons = '\n'.join(F'{x[0]},{x[1]}' for x in all_locs)
        data.append(
        dict(
            lat=lats,
            lon=lons,
            text=['text'],
            type="scattermapbox",
            # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
            # fill="none", # none, toself, (only toself is working
            marker=dict(
                color='blue'
                ),
            )
        )

    figure=dict(
        data=data,
        layout=dict(
            mapbox=dict(
                layers=[{
                    "sourcetype":"image",
                    "source": img,
                    "coordinates": coordinates,
                    "below": "traces"
                }],
                center=dict(
                    lat=center[0], lon=center[1]
                ),
                style='carto-darkmatter',
                # open-street-map, white-bg, carto-positron, carto-darkmatter,
                # stamen-terrain, stamen-toner, stamen-watercolor
                pitch=0,
                zoom=3,
            ),
            height=600,
            width=1000,
            autosize=True,
        ))

    return figure, lats_lons

def get_dates_dropdown(db):
    dropdown_opts = []
    all_index = db.index
    for c_index in all_index:
        category = db.loc[c_index][DataCols.category.value]
        c_date = db.iloc[c_index][DataCols.time.value].strftime(date_format_ext)
        name = db.iloc[c_index]['name']
        dropdown_opts.append({'label': F'{name} {category} {c_date}',
                              'value': c_index
                              })

    return dropdown_opts
