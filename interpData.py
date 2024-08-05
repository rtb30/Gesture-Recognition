#import 
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
from rdp import rdp
# this function is to simplify dataframe by using the Ramer-Douglas-Peucker algorithm and then interpolating
# the data to the fixed length. If the length is smaller than the target length, the function sends the 
# data to be interpolated
def RDP_interpolate(data, target_length, method, ep = 0.5):
    # convert to numpy array for processing
    data_array = data.values.astype(float)
    print(data_array.shape)

    if len(data) > target_length:
        # apply RDP to reduce points while preserving shape
        # lower the epsilon, more preservation of data
        # convert to dataframe
        simplified_data = rdp(data_array, epsilon = ep)
        simplified_df = pd.DataFrame(simplified_data, columns = data.columns)

        # check if simplified data is too small
        if len(simplified_data) < 2:
            raise ValueError("RDP simplification resulted in too few points to perform interpolation.")

        # interpolate the simplified dataframe to the target length
        interpolated_data =  interpolate_data(simplified_df, target_length, method)
    
    else:
        # interpolate data if length is smaller than target
        interpolated_data = interpolate_data(data, target_length, method)

    # convert and return as dataframe
    interpolated_df = pd.DataFrame(interpolated_data, columns = data.columns)
    return interpolated_df

# this function is to interpolate data to a specific length
def interpolate_data(data, target_length, method):
    # store length in variable
    original_length = len(data)

    # return data if it doesnt need to be interpolated
    if original_length == target_length:
        return data
    
    # evenly spaced arrays of numbers over a specified interval
    x_original = np.linspace(0, 1, original_length)
    x_target = np.linspace(0, 1, target_length)

    # empty array of target_length x data columns (shape[1])
    interpolated_data = np.zeros((target_length, data.shape[1]))

    # ensure data is only numeric
    data_array = data.values.astype(float)

    # iterate over the each column to linear interpolate in rows near the indices of the evenly spaced array values
    for i in range(data.shape[1]):
        # convert to numpy array for processing
        column_data = data_array[:, i]

        # interpolate and return
        if method == 'linear':
            f = interp1d(x_original, column_data, kind = 'linear', fill_value = "extrapolate")
        elif method == 'cubic':
            f = CubicSpline(x_original, column_data, extrapolate = True)
        else:
            raise ValueError(f"Interpolation method '{method}' is not supported.")
        
        # apply the interpolation function to the target x values
        interpolated_data[:, i] = f(x_target)
        
    # convert and return as dataframe
    interpolated_df = pd.DataFrame(interpolated_data, columns = data.columns)
    return interpolated_df

# this function pads zeros when certain dataframes in the EPC_sep list are empty
def pad_data_zeros(EPC_sep, max_length, i, EPC_count):

    padding = np.zeros((max_length - len(EPC_sep), EPC_sep.shape[1]))
    padded_data = np.vstack((EPC_sep, padding))

    padded_dataframe = pd.DataFrame(padded_data, columns = EPC_sep.columns)

    i += 1
    EPC = i % EPC_count
    #print(f'This data frame was empty, i think its from tag {EPC}')
    for j in range(len(padded_dataframe)):
        padded_dataframe['EPC'][j] = EPC

    return padded_dataframe