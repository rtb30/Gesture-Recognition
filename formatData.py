# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import copy
from smoothData import rolling, gaussian, savgol, detrend
from fileSaveHDF5 import saveto_h5_4Dmatrix
from interpData import RDP_interpolate, interpolate_data, pad_data_zeros
from normalizeData import (RSSI_normalize, RSSI_normalize_EPC, phase_normalize, 
                           phase_normalize_EPC, phase_standardize, phase_scale,
                           standardize_robust)
from transformData import (phase_log_transform, phase_quantile_transform, phase_robust_scaler,
                           phase_power_transform, phase_log_transform_shift)
from augmentData import add_constant_offset, sub_constant_offset, add_gaussian_noise, add_offset_and_noise

# this function formats the original data exported from the ItemTest program
# made by IMPINJ. The output of this function returns a dataframe list
# which contains RSSI & phase data based on EPC and iteration for 1 gesture
def format(inputs, h5_flag, length, h5_name, labels, norm_flag, RSSI_val, phase_val, phase_val_tx):

    ############################### FUNCTION VARIABLES ###############################
    # init empty lists
    data = []
    EPC_sep = []
    data_new = []
    EPC_count_list = []

    #init empty dictionary to store EPC values
    mapping = {}
    
    ############################### DATA PREFORMATTING ###############################
    # load csv file into dataframe and change header row (deletes everything before)
    for input in inputs:
        #print(f'Trying to read csv file: {input}')
        data.append(pd.read_csv(input, header = 2))
        
    for i in range(len(data)):
        # change which columns are needed and remove spaces
        data[i] = data[i].iloc[0:, [0,1,4,7]]
        data[i].columns = data[i].columns.str.strip()

        # rename timestamp column
        data[i].rename(columns={'// Timestamp' : 'Timestamp'}, inplace = True)

        # parse timestamp data and create new column to have comparable time values
        data[i]['Timestamp'] = pd.to_datetime(data[i]['Timestamp'])
        first_timestamp = data[i]['Timestamp'].iloc[0]
        data[i]['Timestamp'] = (data[i]['Timestamp'] - first_timestamp).dt.total_seconds()
        data[i].rename(columns={'Timestamp': 'TimeValue'}, inplace=True)

        # correctly change RSSI column to numbers
        if(data[i]['RSSI'].dtype != 'int64'):
            # replace commas, negative signs, then change to float64s
            data[i]['RSSI'] = data[i]['RSSI'].str.replace(',' , '.', regex = False)
            data[i]['RSSI'] = data[i]['RSSI'].str.replace(r'[^\d.-]', '-', regex = True)
            data[i]['RSSI'] = pd.to_numeric(data[i]['RSSI'], errors='coerce')

        # replace commas and change to float64s
        data[i]['PhaseAngle'] = data[i]['PhaseAngle'].str.replace(',' , '.', regex = False)
        data[i]['PhaseAngle'] = pd.to_numeric(data[i]['PhaseAngle'])
        
        # create list of numerical values for tag count
        EPC_count_list.append(data[i]['EPC'].nunique())

    # find the maximum amount of tags used
    EPC_count = max(EPC_count_list)
    #EPC_count = 4

    # replace EPC with numeric values
    #for i in range(EPC_count):
    #    mapping[f'A{i + 1}0000000000000000000000'] = (i + 1)

    mapping = {'A10000000000000000000000': 1,
               'A20000000000000000000000': 2,
               'A30000000000000000000000': 3,
               'A40000000000000000000000': 4,
               'A60000000000000000000000': 5,
               'A70000000000000000000000': 6,
               'A80000000000000000000000': 7,
               'A90000000000000000000000': 8}

    EPC_count = len(mapping)
    
    # create another data set with separate numercial EPC values
    for i in range(len(data)):
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)

        for j in range(1, EPC_count + 1):
            EPC_sep.append(data[i][data[i]['EPC'] == j])

            # empty dataframes under a certain length
            #if(len(EPC_sep[-1]) <= 5):
            #    EPC_sep[-1] = EPC_sep[-1].iloc[0:0]
    
    if(norm_flag == 1):   
        print(f'---------------------- TRAINING DATA --------------------')                              
        print(f'Tags: {EPC_count}')
    else:
        print(f'---------------------- TESTING DATA ---------------------')                              
        print(f'Tags: {EPC_count}')

    #for i in range(len(data)):
    #    print(f'This is data set {i}:')
    #    print(data[i], '\n')

    #for i in range(len(EPC_sep)):
    #    print('EPC data set:')
    #    print(EPC_sep[i], '\n')
    
    #################################### NORMALIZE DATA ####################################
    # normalize RSSI based on preferences
    # if data is highly skewed:     use log transformations
    # if data is slightly skewed:   use power transformations
    if(norm_flag == 1):
        # RSSI normalization options
        EPC_sep, RSSI_val = RSSI_normalize(EPC_sep, norm_flag, RSSI_val)
        #EPC_sep, RSSI_val = standardize_robust(EPC_sep, norm_flag, phase_val, 'RSSI')
        #EPC_sep, RSSI_val = RSSI_normalize_EPC(EPC_sep, EPC_count, norm_flag, phase_val)

        # phase transformation options 
        #EPC_sep = phase_log_transform(EPC_sep)
        #EPC_sep, phase_val = phase_quantile_transform(EPC_sep, norm_flag, phase_val, 'normal')
        #EPC_sep, phase_val_tx = phase_robust_scaler(EPC_sep, norm_flag, phase_val_tx)
        EPC_sep, phase_val_tx = phase_power_transform(EPC_sep, norm_flag, phase_val_tx)
        #EPC_sep, phase_val = phase_log_transform_shift(EPC_sep, norm_flag, phase_val)

        # phase normalization options
        #EPC_sep, phase_val = phase_normalize(EPC_sep, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_normalize_EPC(EPC_sep, EPC_count, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_standardize(EPC_sep, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_scale(EPC_sep, norm_flag, phase_val)
        EPC_sep, phase_val = standardize_robust(EPC_sep, norm_flag, phase_val, 'PhaseAngle')
        
        print('Normalized')

    else:
        # RSSI normalization options
        EPC_sep, RSSI_val = RSSI_normalize(EPC_sep, norm_flag, RSSI_val)
        #EPC_sep, RSSI_val = standardize_robust(EPC_sep, norm_flag, RSSI_val, 'RSSI')
        #EPC_sep, RSSI_val = RSSI_normalize_EPC(EPC_sep, EPC_count, norm_flag, phase_val)

        # phase transformation options
        #EPC_sep = phase_log_transform(EPC_sep)
        #EPC_sep, phase_val = phase_quantile_transform(EPC_sep, norm_flag, phase_val, 'normal')
        #EPC_sep, phase_val_tx = phase_robust_scaler(EPC_sep, norm_flag, phase_val_tx)
        EPC_sep, phase_val_tx = phase_power_transform(EPC_sep, norm_flag, phase_val_tx)
        #EPC_sep, phase_val = phase_log_transform_shift(EPC_sep, norm_flag, phase_val)

        # phase normalization options
        #EPC_sep, phase_val = phase_normalize(EPC_sep, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_normalize_EPC(EPC_sep, EPC_count, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_standardize(EPC_sep, norm_flag, phase_val)
        #EPC_sep, phase_val = phase_scale(EPC_sep, norm_flag, phase_val)
        EPC_sep, phase_val = standardize_robust(EPC_sep, norm_flag, phase_val, 'PhaseAngle')

        print('Normalized')

    #for i in range(len(EPC_sep)):
    #    print('EPC data set:')
    #    print(EPC_sep[i], '\n')
    
    ############################# SMOOTH AND INTERPOLATE DATA #############################
    # smoothing functions for non-periodic phase data of quantities around 20
    EPC_sep, savgol_flag = savgol(EPC_sep)
    if savgol_flag == 1:
        print('Savgol filter applied')
        
    EPC_sep, g_flag = gaussian(EPC_sep)
    if g_flag == 1:
        print('Gaussian filter applied')

    # define interpolation type (linear, cubic)
    method = 'linear'
    print('Interpolation type: ', method)

    # ensure all data is the same length using an RDP algorithm and/or interpolation
    if length[0]:
        for i in range(len(EPC_sep)):
            if(EPC_sep[i].shape[0] > 1):
                #EPC_sep[i] = RDP_interpolate(EPC_sep[i], length[1], method, 0.5)
                EPC_sep[i] = interpolate_data(EPC_sep[i], length[1], method)
            else:
                EPC_sep[i] = pad_data_zeros(EPC_sep[i], length[1], i, EPC_count)

            # print('EPC data set:')
            # print(EPC_sep[i], '\n')

    ################################## CONCATENATE EPC DATA #################################
    # concatenate separated EPC data into singular dataframe sorted chronologically again
    #for i in range(len(data)):
    #    EPC_gesture_list = []
    #    for j in range(EPC_count):
    #        EPC_gesture_list.append(EPC_sep[i * EPC_count + j])
        
    #    data_new.append(pd.concat(EPC_gesture_list, ignore_index = False))
        #print(f'This is new data set {i}:')
        #print(data_new[i])
    
    #################################### AUGMENT EPC DATA ###################################
    if(norm_flag == 1):
        # create augmented list and add in augmented dataframes
        #aug_EPC = copy.deepcopy(EPC_sep)
        #aug_EPC = [add_gaussian_noise(df, RSSI_std=0.05, phase_std=0.25) for df in aug_EPC] # great for normal RSSI and no phase normalization
#
        #aug_EPC2 = copy.deepcopy(EPC_sep)
        #aug_EPC2 = [add_offset_and_noise(df, RSSI_offset=0, phase_offset=1, RSSI_std=0.05, phase_std=0.25) for df in aug_EPC2]
#
        #aug_EPC3 = copy.deepcopy(EPC_sep)
        #aug_EPC3 = [add_gaussian_noise(df, RSSI_std=0.075, phase_std=0.5) for df in aug_EPC3]

        #offset_df_add = [add_constant_offset(df, RSSI_offset=0, phase_offset=1) for df in EPC_sep]
        #offset_df_sub = [sub_constant_offset(df, RSSI_offset=0, phase_offset=1) for df in EPC_sep]
        #augmented_df1 = [add_gaussian_noise(df, RSSI_std=0.05, phase_std=0.25) for df in EPC_sep]
        #augmented_df2 = [add_gaussian_noise(df, RSSI_std=0.1, phase_std=0.5) for df in EPC_sep]
        #augmented_df3 = [add_gaussian_noise(df, RSSI_std=0.15, phase_std=0.75) for df in EPC_sep]

        # concatenate all dataframes and labels togther
        #EPC_sep = EPC_sep + offset_df_add + offset_df_sub
        #EPC_sep += aug_EPC + aug_EPC2 + aug_EPC3
        #labels += labels + labels + labels

        #print('Augmented')
        print('Filtered and Interpolated')
        
    else:
        print('Filtered and Interpolated')

    # use data to save as csv which will return and save unchanged data to h5
    if h5_flag == 1:
        saveto_h5_4Dmatrix(EPC_sep, h5_name, labels, EPC_count, norm_flag) # 4D matrix

    if (norm_flag == 1):
        return RSSI_val, phase_val, phase_val_tx