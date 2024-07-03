# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from preprocData import rolling, gaussian, savgol, detrend
from fileSave import saveto_csv, saveto_h5

# this function formats the original data exported from the ItemTest program
# made by IMPINJ. The output of this function returns a dataframe list
# which contains RSSI & phase data based on EPC and iteration for 1 gesture
def format(inputs, outputs, phase, RSSI, csv_flag, h5_flag):
    # define empty lists
    data = []
    EPC_sep = []
    RSSI_min = []
    data_new = []
    
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
        if(data[i][RSSI].dtype != 'int64'):
            # replace commas, negative signs, then change to float64s
            data[i][RSSI] = data[i][RSSI].str.replace(',' , '.', regex = False)
            data[i][RSSI] = data[i][RSSI].str.replace(r'[^\d.-]', '-', regex = True)
            data[i][RSSI] = pd.to_numeric(data[i][RSSI], errors='coerce')

        # replace commas, change to float64s, and round
        data[i][phase] = data[i][phase].str.replace(',' , '.', regex = False)
        data[i][phase] = pd.to_numeric(data[i][phase])
        data[i][phase] = data[i][phase].round(4)

        # replace EPC with numeric values
        mapping = {'A10000000000000000000000': 1, 'A20000000000000000000000': 2}
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)

        # create another data set with separate EPC values
        EPC_sep.append(data[i][data[i]['EPC'] == 1])
        EPC_sep.append(data[i][data[i]['EPC'] == 2])

    for i in range(len(EPC_sep)):
        # normalize all RSSI data by EPC
        RSSI_min.append(min(EPC_sep[i][RSSI]))
        EPC_sep[i][RSSI] = EPC_sep[i][RSSI] / RSSI_min[i]

        # unwrap all phase data by EPC
        EPC_sep[i][phase] = np.unwrap(EPC_sep[i][phase])

    # filtering functions for non-periodic phase data of quantities around 20
    EPC_sep = savgol(EPC_sep, phase)
    EPC_sep = gaussian(EPC_sep, phase)

    # for loop to concatenate the EPC separated date into singular dataframe
    for i in range(len(data)):
        j = 2*i
        data_new.append(pd.concat([EPC_sep[j], EPC_sep[j + 1]], ignore_index = True))

    # use data to save as csv which will return and save unchanged data to h5
    if csv_flag == 1:
        saveto_csv(data_new, outputs)
    if h5_flag == 1:
        saveto_h5(data_new)
    
    print('-------------- FINISHED FORMATTING & FILTERING --------------\n')

    return EPC_sep