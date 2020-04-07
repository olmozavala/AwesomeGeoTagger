import xarray as xr
from os.path import join
import numpy as np
import os


def all_to_rad(arr):
    return [np.deg2rad(x) for x in arr]

def combine_currents_winds(U_c, V_c, U_w, V_w, LAT, w_perc, rot_matrix_nh, rot_matrix_sh):
    """
    This function is in charge of combining currents and winds into a single field.
    The curreent U_combined = U + .025*winds*deflection
    :param U_c:
    :param V_c:
    :param U_w:
    :param V_w:
    :param LAT:
    :param w_perc:
    :param rot_matrix_nh:
    :param rot_matrix_sh:
    :return:
    """
    U_c, V_c, U_w, V_w = [x.values[0] for x in [U_c, V_c, U_w, V_w]]
    # =========== Rotating by an angle =========
    north_hem = LAT < 0
    south_hem = LAT >= 0
    U_flat = U_w.flatten()
    V_flat = V_w.flatten()
    temp_wind_rot = np.zeros((len(LAT),2))
    temp_wind_rot[north_hem,:] = np.dot(np.array([U_flat[north_hem], V_flat[north_hem]]).T, rot_matrix_nh)
    temp_wind_rot[south_hem,:] = np.dot(np.array([U_flat[south_hem], V_flat[south_hem]]).T, rot_matrix_sh)
    U_wnew = temp_wind_rot[:,0].reshape(U_w.shape)
    V_wnew = temp_wind_rot[:,1].reshape(V_w.shape)
    # xi = 2060
    # yi = 1406
    # print(F"Original {V_w[xi, yi]} {V_wnew[xi,yi]}")
    # =========== Reducing wind component ========
    U_c = U_c + U_wnew*w_perc
    V_c = V_c + V_wnew*w_perc
    return np.expand_dims(U_c, axis=0), np.expand_dims(V_c, axis=0)

def save_file(file_name,  vars, coords, output_folder):
    ds = xr.open_dataset(file_name, decode_times=False)
    keep_vars = {var_name: (coords, ds[var_name][:].values) for var_name in vars}
    coords = {var_name: ds[var_name] for var_name in coords}
    ds = xr.Dataset(keep_vars, coords)
    ds.to_netcdf(join(output_folder, F"{os.path.basename(file_name)}.nc"))

def main():
    # Home
    input_folder = "/home/data/ECMWF/WRF_Kraken_Old_Model_Reanalisis/a2012/salidas"
    output_folder = join(input_folder, "reduced")
    normal_input_files = ["wrfout_c1h_d01_2012-08-07_00:00:00.2012"]
    coords_input_file = "wrfout_c15d_d01_2012-01-01_00:00:00.2012"

    if not (os.path.exists(output_folder)):
        os.makedirs(output_folder)


    coords = ['Time', 'south_north', 'west_east']

    vars = ['XLAT', 'XLONG']
    coords_file = join(input_folder, coords_input_file)
    save_file(coords_file, vars, coords, output_folder)

    all_files = [join(input_folder, x) for x in normal_input_files]
    for c_file in all_files:
        # ------- Saving the 1h files
        vars = ['Q2', 'RAINC', 'U10', 'V10', 'PSFC', 'SST']
        save_file(c_file, vars, coords, output_folder)
        # This is merging and reducing (PROPERLY DONE)
        # # ------- Getting desired variables -------
        # xr_ds = xr.open_dataset(c_file, decode_times=False)
        # keep_vars = {var_name: (("time", "lat", "lon"), xr_ds[var_name][:].values) for var_name in vars}
        #
        # # ------- Getting desired coordinates -------
        # xr_coords_ds = xr.open_dataset(join(input_folder,coords_input_file), decode_times=False)
        # lat = xr_coords_ds["XLAT"][0,:,0].values
        # lon = xr_coords_ds["XLONG"][0,0,:].values
        #
        # ds = xr.Dataset(
        #     keep_vars,
        #     {"time": xr_ds["time"].values,
        #      "lat": lat,
        #      "lon": lon}
        # )
        # ds.to_netcdf(join(output_folder, F"{os.path.basename(c_file)}.nc"))


if __name__ == "__main__":
    main()
