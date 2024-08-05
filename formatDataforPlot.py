# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
from smoothData import rolling, gaussian, savgol, detrend
from interpData import RDP_interpolate, interpolate_data, pad_data_zeros
from normalizeData import (RSSI_normalize_EPC, RSSI_normalize_train, phase_normalize_train, 
                           phase_scale_train, phase_standardize_train, phase_log_transform_train, 
                           phase_quantile_transform_train)
from augmentData import add_constant_offset, sub_constant_offset, add_gaussian_noise, add_offset_and_noise

# this function formats the original data exported from the ItemTest program
# made by IMPINJ. The output of this function returns a dataframe list
# which contains RSSI & phase data based on EPC and iteration for 1 gesture
def format(inputs, length):

    ############################### FUNCTION VARIABLES ###############################
    # init empty lists
    data = []
    EPC_sep = []
    data_new = []
    EPC_count_list = []
    RSSI_val = []
    phase_val = []

    #init empty dictionary
    mapping = {}
    
    ############################### DATA PREFORMATTING ###############################
    # load csv file into dataframe and change header row (deleted everything before)
    for input in inputs:
        #print(f'Trying to read csv file: {input}')
        data.append(pd.read_csv(input, header = 2))
        
    for i in range(len(data)):
        # change which columns are needed and remove spaces
        data[i] = data[i].iloc[0:, [0,1,4,7]]
        data[i].columns = data[i].columns.str.strip()

        # rename timestamp column
        data[i].rename(columns={'// Timestamp' : 'Timestamp'},     inplace = True)

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
        #print(f'gesture number {i+1} has {EPC_count_list[i]} tags, file name {inputs[i]}')

    # find the maximum amount of tags used
    EPC_count = max(EPC_count_list)
    #EPC_count = 4
    print(f'--------------------- DATA HAS {EPC_count} TAGS ------------------')

    # replace EPC with numeric values
    for i in range(EPC_count):
        mapping[f'A{i + 1}0000000000000000000000'] = (i + 1)

    # create another data set with separate numercial EPC values
    for i in range(len(data)):
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)

        for j in range(1, EPC_count + 1):
            EPC_sep.append(data[i][data[i]['EPC'] == j])

    #for i in range(len(data)):
    #    print(f'This is data set {i}:')
    #    print(data[i], '\n')

    #for i in range(len(EPC_sep)):
    #    print('EPC data set:')
    #    print(EPC_sep[i], '\n')
    
    #################################### NORMALIZE DATA ####################################
    # RSSI normalization options
    EPC_sep, RSSI_val = RSSI_normalize_train(EPC_sep, 1, RSSI_val)
    #EPC_sep, RSSI_min = RSSI_normalize_EPC(EPC_sep, EPC_count, data_flag[0])

    # phase normalization options
    EPC_sep = phase_log_transform_train(EPC_sep)
    EPC_sep, phase_val = phase_normalize_train(EPC_sep, 1, phase_val)
    #EPC_sep, phase_val = phase_standardize_train(EPC_sep, 1, phase_val)
    #EPC_sep, phase_val = phase_scale_train(EPC_sep, 1, phase_val)
    #EPC_sep, phase_val = phase_quantile_transform_train(EPC_sep, 1, phase_val)
    
    print(f'--------------------- NORMALIZED DATA ------------------')
    #for i in range(len(EPC_sep)):
    #    if i <= 24:
    #        print('EPC data set:')
    #        print(EPC_sep[i], '\n')
    
    ############################# SMOOTH AND INTERPOLATE DATA #############################
    # filtering functions for non-periodic phase data of quantities around 20
    EPC_sep = savgol(EPC_sep)
    EPC_sep = gaussian(EPC_sep)

    # find the maximum length of data in all EPC dataframes
    # we can technically set this to whatever we want
    if(length[2] == 1):
        length[1] = max(len(EPC) for EPC in EPC_sep)

    # define interpolation type
    method = 'linear'

    print(f'--------------------- SMOOTHED & INTERPOLATED DATA ------------------')
    # ensure all data is the same length using an RDP algorithm and/or interpolation
    if length[0]:
        for i in range(len(EPC_sep)):
            if(EPC_sep[i].shape[0] > 1):
                #EPC_sep[i] = RDP_interpolate(EPC_sep[i], length[1], method, 0.5)
                EPC_sep[i] = interpolate_data(EPC_sep[i], length[1], method)
            else:
                EPC_sep[i] = pad_data_zeros(EPC_sep[i], length[1], i, EPC_count)

            #if i <= 24:
            #    print('EPC data set:')
            #    print(EPC_sep[i], '\n')

    ################################## CONCATENATE EPC DATA #################################
    # concatenate separated EPC data into singular dataframe sorted chronologically again
    for i in range(len(data)):
        EPC_gesture_list = []
        for j in range(EPC_count):
            EPC_gesture_list.append(EPC_sep[i * EPC_count + j])
        
        data_new.append(pd.concat(EPC_gesture_list, ignore_index = False))
        #print(f'This is new data set {i}:')
        #print(data_new[i])
    
    #################################### AUGMENT EPC DATA ###################################
    # create augmented list and add in augmented dataframes
    #offset_df_add = [add_constant_offset(df) for df in EPC_sep]
    #offset_df_sub = [sub_constant_offset(df) for df in EPC_sep]
    #augmented_df = [add_offset_and_noise(df) for df in EPC_sep]

    # concatenate all dataframes and labels togther
    #EPC_sep = EPC_sep + offset_df_add + offset_df_sub
    #labels = labels + labels + labels

    # count how many times each tag appears per gesture
    #tag_counter(data_new, EPC_count, labels)

    return EPC_sep, data_new

def tag_counter(data_new, EPC_count, labels):
    count = 0
    sum = 0
    for j in range(1, EPC_count + 1):
        print(f'Finding A{j} tags')
        for i in range(len(data_new)):
            sum = sum + data_new[i]['EPC'].value_counts().get(j, 0)
    
            count = count + 1
    
            if(count == 20):
                print(f'{labels[i]} has a total of {sum} tags')
                count = 0
                sum = 0
        print()

    for i in range(len(data_new)):
            num_EPC = data_new[i]['EPC'].value_counts().get(4, 0)
            print(f'{labels[i]} has {num_EPC} A1 tags')