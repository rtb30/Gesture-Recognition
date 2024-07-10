# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from preprocData import rolling, gaussian, savgol, detrend
from fileSave import saveto_csv, saveto_h5_3Dmatrix, saveto_h5_gest_EPC_sep, saveto_h5_4Dmatrix
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
from rdp import rdp

# this function formats the original data exported from the ItemTest program
# made by IMPINJ. The output of this function returns a dataframe list
# which contains RSSI & phase data based on EPC and iteration for 1 gesture
def format(inputs, outputs, flags, length, h5_name, labels):
    # init empty lists
    data = []
    EPC_sep = []
    RSSI_min = []
    data_new = []
    EPC_count_list = []

    #init empty dictionary
    mapping = {}
    
    # load csv file into dataframe and change header row (deleted everything before)
    for input in inputs:
        data.append(pd.read_csv(input, header = 2))

    for i in range(len(data)):
        # change dataframe headers to correct column and select wanted data
        data[i] = data[i].iloc[0:, [0,1,4,7]]

        # rename columns
        data[i].rename(columns={'// Timestamp' : 'Timestamp'},     inplace = True)
        data[i].rename(columns={' RSSI'        : 'RSSI'},          inplace = True)
        data[i].rename(columns={' PhaseAngle'  : 'PhaseAngle'},    inplace = True)
        data[i].rename(columns={' EPC'         : 'EPC'},           inplace = True)

        # parse timestamp data and create new column to have comparable time values
        data[i]['Timestamp'] = pd.to_datetime(data[i]['Timestamp'])
        first_timestamp = data[i]['Timestamp'].iloc[0]
        data[i]['TimeElapsed'] = data[i]['Timestamp'] - first_timestamp

        # separate time elapsed into seconds and milliseconds, then combine the numbers
        data[i]['seconds'] = data[i]['TimeElapsed'].dt.seconds
        data[i]['milliseconds'] = data[i]['TimeElapsed'].dt.microseconds // 1000
        data[i]['TimeValue'] = data[i]['seconds'] + data[i]['milliseconds'] / 1000
        data[i]['TimeValue'] = data[i]['TimeValue'].round(4) # round to 4 decimal places

        # move timevalue column over
        data[i]['Timestamp'] = data[i]['TimeValue']
        data[i].rename(columns={'Timestamp': 'TimeValue'}, inplace=True)

        # remove excess time columns, good place to print data
        data[i] = data[i].iloc[0:, [0,1,2,3]]

        # correctly change RSSI column to numbers
        if(data[i]['RSSI'].dtype != 'int64'):
            # replace commas, negative signs, then change to float64s
            data[i]['RSSI'] = data[i]['RSSI'].str.replace(',' , '.', regex = False)
            data[i]['RSSI'] = data[i]['RSSI'].str.replace(r'[^\d.-]', '-', regex = True)
            data[i]['RSSI'] = pd.to_numeric(data[i]['RSSI'], errors='coerce')

        # replace commas, change to float64s, and round
        data[i]['PhaseAngle'] = data[i]['PhaseAngle'].str.replace(',' , '.', regex = False)
        data[i]['PhaseAngle'] = pd.to_numeric(data[i]['PhaseAngle'])
        data[i]['PhaseAngle'] = data[i]['PhaseAngle'].round(4)
        
        # create list of numerical values for tag count
        EPC_count_list.append(data[i]['EPC'].nunique())
        '''
        mapping = {'A10000000000000000000000': 1, 'A20000000000000000000000': 2}
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)

        # create another data set with separate EPC values
        EPC_sep.append(data[i][data[i]['EPC'] == 1])
        EPC_sep.append(data[i][data[i]['EPC'] == 2])
        '''

    # find the maximum amount of tags used
    EPC_count = max(EPC_count_list)
    #print('there are a max of ',EPC_count, ' tags used in this dataset')

    # replace EPC with numeric values
    for i in range(EPC_count):
        mapping[f'A{i + 1}0000000000000000000000'] = (i + 1)

    #print(mapping)

    # create another data set with separate numercial EPC values
    for i in range(len(data)):
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)
        EPC_sep.append(data[i][data[i]['EPC'] == 1])
        EPC_sep.append(data[i][data[i]['EPC'] == 2])
        
    
    for i in range(len(EPC_sep)):
        if(EPC_sep[i].empty == False):
        # normalize all RSSI data by EPC
            RSSI_min.append(min(EPC_sep[i]['RSSI']))
            EPC_sep[i]['RSSI'] = EPC_sep[i]['RSSI'] / RSSI_min[i]

            # unwrap all phase data by EPC
            EPC_sep[i]['PhaseAngle'] = np.unwrap(EPC_sep[i]['PhaseAngle'])
            EPC_sep[i] = EPC_sep[i].reset_index(drop = True)

        else:
            RSSI_min.append(1)
        #print(EPC_sep[i])

    # filtering functions for non-periodic phase data of quantities around 20
    EPC_sep = savgol(EPC_sep)
    EPC_sep = gaussian(EPC_sep)

    # find the maximum length of data in all EPC dataframes
    # we can technically set this to whatever we want
    if(length[2] == 1):
        length[1] = max(len(EPC) for EPC in EPC_sep)

    # ensure all data is the same length using an RDP algorithm and/or interpolation
    if length[0]:
        for i in range(len(EPC_sep)):
            if(EPC_sep[i].shape[0] > 1):
                EPC_sep[i] = interpolate_data(EPC_sep[i], length[1])
            else:
                EPC_sep[i] = pad_data_zeros(EPC_sep[i], length[1])
                #print(EPC_sep[i])

    # concatenate separated EPC data into singular dataframe sorted chronologically again
    for i in range(len(data)):
        EPC_gesture_list = []
        for j in range(EPC_count):
            EPC_gesture_list.append(EPC_sep[i * EPC_count + j])
        
        data_new.append(pd.concat(EPC_gesture_list, ignore_index = False))

        # this makes the HDF5 file more confusing but here for notation
        #data_new[i] = data_new[i].sort_values(by = 'TimeValue')
        #data_new[i] = data_new[i].reset_index(drop = True) 

    print('-------------- FINISHED FORMATTING & FILTERING --------------\n')

    # use data to save as csv which will return and save unchanged data to h5
    if flags[0] == 1:
        saveto_csv(data_new, outputs)
    if flags[1] == 1:
        #saveto_h5_3Dmatrix(data_new, h5_name) # 3D matrix
        #saveto_h5_gest_EPC_sep(data_new, h5_name) # each dataset is separated by gesture & EPC
        saveto_h5_4Dmatrix(EPC_sep, h5_name, labels, EPC_count) # 4D matrix

    return EPC_sep

# this function is to simplify dataframe by using the Ramer-Douglas-Peucker algorithm and then interpolating
# the data to the fixed length. If the length is smaller than the target length, the function sends the 
# data to be interpolated
def RDP_interpolate(data, target_length):
    # convert to numpy array for processing
    data_array = data.values

    if len(data) > target_length:
        # apply RDP to reduce points while preserving shape
        # lower the epsilon, more preservation of data
        simplified_data = rdp(data_array, epsilon = 0.5)

        # interpolate the simplified data to the target length
        interpolated_data =  interpolate_data(simplified_data, target_length)
    
    else:
        # interpolate data if length is smaller than target
        interpolated_data = interpolate_data(data, target_length)

    # convert and return as dataframe
    interpolated_df = pd.DataFrame(interpolated_data, columns = data.columns)
    return interpolated_df

# this function is to interpolate data to a specific length
def interpolate_data(data, target_length):
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

    # iterate over the each column to linear interpolate in rows near the indices of the evenly spaced array values
    for i in range(data.shape[1]):
        # ensure data is only numeric
        # convert to numpy array for processing
        data_array = data.values
        column_data = data_array[:, i].astype(float)

        # interpolate and return
        f = interp1d(x_original, column_data, kind='linear', fill_value="extrapolate")
        #f = CubicSpline(x_original, data[:, i], extrapolate=True)
        interpolated_data[:, i] = f(x_target)
        
    # convert and return as dataframe
    interpolated_df = pd.DataFrame(interpolated_data, columns = data.columns)
    return interpolated_df
    # return interpolated_data

def pad_data_zeros(EPC_sep, max_length):

    padding = np.zeros((max_length - len(EPC_sep), EPC_sep.shape[1]))
    padded_data = np.vstack((EPC_sep, padding))

    padded_dataframe = pd.DataFrame(padded_data, columns = EPC_sep.columns)

    return padded_dataframe
