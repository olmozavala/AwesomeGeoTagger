import xarray as xr
import colorcet as cc
import datashader.transfer_functions as tf
from config.params import DataCols, FileType
import numpy as np
import os
from datetime import date, datetime

date_format_ext = '%Y-%m-%dT%H:%M:%S'

def fill_data_and_fig(center_storm, selection, img, coordinates, center, zoom, title, storm_name):

    data = [
        dict(
            lat=[center_storm[0]],
            lon=[center_storm[1]],
            text=['text'],
            type="scattermapbox",
            # type="choroplethmapbox",
            # type="densitymapbox",
            customdata=['custom'],
            # https://plot.ly/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
            # https://plotly.com/python/reference/#scattermapbox
            # fill="none", # none, toself, (only toself is working
            marker=dict(
                color='red'
            ),
            # hovertemplate='Station: %{text} <extra></extra>'
            hovertemplate = F'{storm_name}'
    )
    ]

    lats_lons = ''
    if not(selection is None):
        all_locs = selection['lassoPoints']['mapbox']
        lats = [x[1] for x in all_locs]
        lons = [x[0] for x in all_locs]
        # To 'circle' the lines
        lats.append(all_locs[0][1])
        lons.append(all_locs[0][0])
        # print(F'lats: {lats}, \n lons: {lons}')
        lats_lons = '\n'.join(F'{x[0]},{x[1]}' for x in all_locs)
        data.append(
        dict(
            lat=lats,
            lon=lons,
            text=['text'],
            type="scattermapbox",
            mode='lines',
            # https://plotly.com/python/scattermapbox/
            # fill="none", # none, toself, (only toself is working
            marker=dict(
                color='black'
                ),
            )
        )

    figure = dict(
        data=data,
        layout=dict(
            # https://plotly.com/python/reference/#layout-mapbox
            mapbox=dict(
                layers=[{
                    "sourcetype": "image",
                    "source": img,
                    "coordinates": coordinates,
                    "type": "raster",
                    "below": "traces"
                }],
                center=dict(
                    lat=center[1], lon=center[0]
                ),
                # bearing=30, # Rotated angle
                # https://plotly.com/javascript/mapbox-layers/
                # https://plotly.com/python/reference/#layout-mapbox-style
                style='stamen-terrain',
                # open-street-map, white-bg, carto-positron, carto-darkmatter,
                # stamen-terrain, stamen-toner, stamen-watercolor
                pitch=0,
                zoom=zoom,
            ),
            autosize=True,
            title=title,
            margin=dict(
                l=10, r=10, t=30, b=20
            )
        ))

    return figure, lats_lons


def get_ecmwf_map(id, selection, db, field, center = [-94, 24], zoom=3):
    """
    This function will generate the proper dash map with the selected
    date and, if the user has already draw something, it will add the points.
    :param selected_file:
    :param selection:
    :return:
    """
    # print(selection)
    selected_files = db.loc[id][DataCols.ecmwf_file.value]
    if selected_files != '':
        selected_files = np.array(selected_files)

        # Here we need to add the other fields like U10, V10 and decide which file to read
        field_type = FileType.twod
        if field in ['u10', 'v10', 't2m', 'msl', 'sp']:
            field_type = FileType.twod
            file_var = 'sfc'
        if field in ['u', 'v', 'd', 'pv', 'vo']:
            field_type = FileType.threed
            file_var = 'pres'

        selected_file = selected_files[[x.find(file_var) != -1 for x in selected_files]][0]

        xr_ds = xr.open_dataset(selected_file, decode_times=False)
        # print(agg.data_vars.values())
        # # agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
        LAT = xr_ds.latitude.values
        LON = xr_ds.longitude.values
        coordinates = [[LON[0], LAT[0]],
                       [LON[-1], LAT[0]],
                       [LON[-1], LAT[-1]],
                       [LON[0], LAT[-1]]]

        # TODO here we need to decide the closest hour
        cdate_ts = db.loc[id]['time']
        start_date_str = os.path.basename(selected_file).split('_')[0].split('-')
        start_date = datetime(int(start_date_str[0]), int(start_date_str[1]), int(start_date_str[2]))
        time_diff = cdate_ts - start_date
        dd = time_diff.days
        t = int(4 * dd + (cdate_ts.hour/6)) # We increase the number of days in difference

        # img = tf.shade(xr_ds[field][:,:], cmap=cc.m_rainbow, alpha=100).to_pil()
        # img = tf.shade(xr_ds[field][:,:], cmap=cc.colorwheel, alpha=180).to_pil()
        # img = tf.shade(xr_ds[field][:,:], cmap=cc.rainbow, alpha=180).to_pil()
        cmap = cc.CET_D13
        if field_type == FileType.twod:
            img = tf.shade(xr_ds[field][t,:,:], cmap=cmap, alpha=180).to_pil()
        elif field_type == FileType.threed:
            img = tf.shade(xr_ds[field][t,20,:,:], cmap=cmap, alpha=180).to_pil()

        center_storm = [db.loc[id]['lat'], db.loc[id]['lon']]
        # title = F'ECMWF {field} {os.path.basename(selected_file)}  File Index:{t}'
        title = F'ECMWF {field}'
        return fill_data_and_fig(center_storm, selection, img, coordinates, center, zoom,
                                 title, db.loc[id]['name'])
    else:
     return dict(), []


def get_goes_map(id, selection, db, field, center = [-94, 24], zoom=3):
    """
    This function will generate the proper dash map with the selected
    date and, if the user has already draw something, it will add the points.
    :param selected_file:
    :param selection:
    :return:
    """
    # print(selection)
    selected_files = db.loc[id][DataCols.goes_file.value]
    if selected_files != '':
        selected_files = np.array(selected_files)
        selected_file = selected_files[[x.find(field) != -1 for x in selected_files]][0]

        xr_ds = xr.open_dataset(selected_file, decode_times=False)
        # print(agg.data_vars.values())
        # # agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
        LAT = xr_ds.lat.values
        LON = xr_ds.lon.values
        coordinates = [[LON[0], LAT[0]],
                       [LON[-1], LAT[0]],
                       [LON[-1], LAT[-1]],
                       [LON[0], LAT[-1]]]

        # img = tf.shade(xr_ds[field][:,:], cmap=cc.m_rainbow, alpha=100).to_pil()
        # img = tf.shade(xr_ds[field][:,:], cmap=cc.colorwheel, alpha=180).to_pil()
        # img = tf.shade(xr_ds[field][:,:], cmap=cc.rainbow, alpha=180).to_pil()
        img = tf.shade(xr_ds[field][:,:], cmap=list(reversed(cc.CET_D1A)), alpha=180).to_pil()
        center_storm = [db.loc[id]['lat'], db.loc[id]['lon']]
        title = F"GOES {field}"
        return fill_data_and_fig(center_storm, selection, img, coordinates, center, zoom, title, db.loc[id]['name'])
    else:
     return dict(), []


def get_map(id, selection, db, field, center = [-94, 24], zoom=3):
    """
    This function will generate the proper dash map with the selected
    date and, if the user has already draw something, it will add the points.
    :param selected_file:
    :param selection:
    :return:
    """
    # print(selection)

    selected_file = db.loc[id][DataCols.netcdf_file.value]
    coords_file = db.loc[id][DataCols.cords_file.value]

    agg = xr.open_dataset(selected_file, decode_times=False)
    # print(agg.data_vars.values())

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

    if field == 'UV-MAG':
        field_values = np.sqrt(agg['U10'].values**2 + agg['V10'].values**2)
    else:
        field_values = agg[field].values
    ds = xr.Dataset(
        {
            "displayed_var": (("time", "lat", "lon"), field_values)
        },
        {"time": agg['Time'].values,
         "lat": cur_xr_ds_coords['XLAT'].values[0,:,0],
         "lon": cur_xr_ds_coords['XLONG'].values[0,0,:],
         },
    )

    hour = int(db.loc[id][DataCols.time.value].strftime('%H'))

    img = tf.shade(ds['displayed_var'][hour,:,:], cmap=cc.rainbow, alpha=150).to_pil()
    title = F'UNAM {field}'
    center_storm = [db.loc[id]['lat'], db.loc[id]['lon']]
    return fill_data_and_fig(center_storm, selection, img, coordinates, center, zoom, title, db.loc[id]['name'])


def get_dates_dropdown(db):
    dropdown_opts = []
    all_index = db.index.values
    for c_index in all_index:
        category = db.loc[c_index][DataCols.category.value]
        c_date = db.loc[c_index][DataCols.time.value].strftime(date_format_ext)
        name = db.loc[c_index]['name']
        lat = db.loc[c_index]['lat']
        lon = db.loc[c_index]['lon']
        dropdown_opts.append({'label': F'{name}   Cat: {category}    Date: {c_date}    Center: {lon}, {lat}',
                              'value': c_index
                              })

    return dropdown_opts
