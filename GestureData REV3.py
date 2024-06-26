# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
import h5py

def Format(inputs, outputs, phase, RSSI, h5_files):
    # define empty variables 
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

    for i in range(len(data)):
        data_new.append(pd.concat([EPC_sep[i], EPC_sep[i + 1]], ignore_index = True))

        # store dataframe in new csv file, and omit index numbers
        data_new[i].to_csv(outputs[i], index = False)

        # store dataframe in new .h5 file, key designates title, and mode 'w' ensures exisiting file is overwritten
        data_new[i].to_hdf(h5_files[i], key = 'data', mode = 'w')

    print("\n-------------------- FINISHED FORMATTING --------------------\n")

    return EPC_sep
            
def plot_2D(phase, RSSI, title, EPC_sep):
    # create figure of 2x2 subplot region
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # subplot 1: top left
    axs[0, 0].plot(EPC_sep[0]['TimeValue'], EPC_sep[0][phase], marker = 'o', linestyle = '-', label = '1')
    axs[0, 0].plot(EPC_sep[2]['TimeValue'], EPC_sep[2][phase], marker = 'o', linestyle = '-', label = '2')
    axs[0, 0].plot(EPC_sep[4]['TimeValue'], EPC_sep[4][phase], marker = 'o', linestyle = '-', label = '3')
    axs[0, 0].set_ylabel('Phase Diff (rads)')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_xlim(left=0)
    axs[0, 0].set_title('A1 Phase vs. Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # subplot 2: top right
    axs[0, 1].plot(EPC_sep[0]['TimeValue'], EPC_sep[0][RSSI], marker = 'o', linestyle = '-', label = '1')
    axs[0, 1].plot(EPC_sep[2]['TimeValue'], EPC_sep[2][RSSI], marker = 'o', linestyle = '-', label = '2')
    axs[0, 1].plot(EPC_sep[4]['TimeValue'], EPC_sep[4][RSSI], marker = 'o', linestyle = '-', label = '3')
    axs[0, 1].set_ylabel('RSSI (Normalized)')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_xlim(left=0)
    axs[0, 1].set_title('A1 RSSI vs. Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # subplot 3: bot left
    axs[1, 0].plot(EPC_sep[1]['TimeValue'], EPC_sep[1][phase], marker = 'o', linestyle = '-', label = '1')
    axs[1, 0].plot(EPC_sep[3]['TimeValue'], EPC_sep[3][phase], marker = 'o', linestyle = '-', label = '2')
    axs[1, 0].plot(EPC_sep[5]['TimeValue'], EPC_sep[5][phase], marker = 'o', linestyle = '-', label = '3')
    axs[1, 0].set_ylabel('Phase Diff (rads)')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_xlim(left=0)
    axs[1, 0].set_title('A2 Phase vs. Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # subplot 4: bot right
    axs[1, 1].plot(EPC_sep[1]['TimeValue'], EPC_sep[1][RSSI], marker = 'o', linestyle = '-', label = '1')
    axs[1, 1].plot(EPC_sep[3]['TimeValue'], EPC_sep[3][RSSI], marker = 'o', linestyle = '-', label = '2')
    axs[1, 1].plot(EPC_sep[5]['TimeValue'], EPC_sep[5][RSSI], marker = 'o', linestyle = '-', label = '3')
    axs[1, 1].set_ylabel('RSSI (Normalized)')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_xlim(left=0)
    axs[1, 1].set_title('A2 RSSI vs. Time')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.4, wspace=0.4)
    fig.suptitle(title, fontsize=16)
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.tight_layout()

    # dpi                   : resolution
    # bbox_inches = 'tight' : ensures it saves all components of figure
    #fig.savefig(f'Graphs/REV3 3m/{title}.png', dpi=300, bbox_inches='tight')

    # show the figure
    plt.show()

    print("\n-------------------- FINISHED PLOTTING --------------------\n")

# have a function that does this maybe?
input1 = 'Data/REV3 3m/6 Lat to Front/6_2s_2_2024-06-19_14-45-00.csv'
input2 = 'Data/REV3 3m/6 Lat to Front/6_2s_2_2024-06-19_14-45-14.csv'
input3 = 'Data/REV3 3m/6 Lat to Front/6_2s_2_2024-06-19_14-45-28.csv'
inputs = [input1, input2, input3]

# define output csv locations
# have a function to automate?
output1 = 'Formatted1.csv'
output2 = 'Formatted2.csv'
output3 = 'Formatted3.csv'
csv_formatted = [output1, output2, output3]

h5_1 = 'Formatted1.h5'
h5_2 = 'Formatted2.h5'
h5_3 = 'Formatted3.h5'
h5_files = [h5_1, h5_2, h5_3]

# other variables
# do i want this?
phase = 'PhaseAngle'
RSSI = 'RSSI'
title = '1: Lateral Raise Gesture - REV3 3m Data'

# call the reformatting function
# automate this?
EPC_sep = Format(inputs, csv_formatted, phase, RSSI, h5_files)

# plot all 3 csvs on 4 subplots
#plot_2D(phase, RSSI, title, EPC_sep)