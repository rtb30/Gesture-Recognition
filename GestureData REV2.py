# import
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt

def Format(input, output, p_col):
    # load csv file into dataframe
    data = pd.read_csv(input, header = 2)

    # change dataframe headers to correct column and select wanted data
    data = data.iloc[0:, [0,1,4,7]]

    # rename columns
    data.rename(columns={'// Timestamp': 'Timestamp'}, inplace=True)
    data.rename(columns={' RSSI': 'RSSI'}, inplace=True)
    data.rename(columns={' PhaseAngle': 'PhaseAngle'}, inplace = True)
    #print(data)
    
    # parse timestamp data and create new  inplace=True)
    data.rename(columns={' EPC': 'EPC'}, inplace=True)
    #print("\n\n")column to have comparable time values
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    first_timestamp = data['Timestamp'].iloc[0]
    data['TimeElapsed'] = data['Timestamp'] - first_timestamp

    data['seconds'] = data['TimeElapsed'].dt.seconds
    data['milliseconds'] = data['TimeElapsed'].dt.microseconds // 1000
    data['TimeValue'] = data['seconds'] + data['milliseconds'] / 1000
    data['TimeValue'] = data['TimeValue'].round(4)

    # remove excess time columns and print data with comparable time values
    data = data.iloc[0:, [0,1,2,3,7]]
    #print("\n\nParsed Time Data:")
    #print(data)

    # change all commas to periods
    ## MUST CHECK IF DATA EVEN HAS A COMMA TO REPLACE: IT GETS STUCK IFN NOT ##
    data['RSSI'] = data['RSSI'].str.replace(',' , '.', regex = False)
    data[p_col] = data[p_col].str.replace(',' , '.', regex = False)

    # ensure only numeric data is kept
    data['RSSI'] = data['RSSI'].str.replace(r'[^\d.-]', '-', regex = True)

    # two ways of changing data types
    #data['RSSI'] = data['RSSI'].astype(float)
    #data[p_col] = data[p_col].astype(float)
    data['RSSI'] = pd.to_numeric(data['RSSI'], errors='coerce')
    data[p_col] = pd.to_numeric(data[p_col])
    data[p_col] = data[p_col].round(4)

    # print data now correct data types
    #print('\n\nNumerical Data')
    #print(data)

    # store dataframe in new csv file, and omit index numbers
    data.to_csv(output, index = False)

def plot3csv(input1, input2, input3, p_col, title):
    # read in formatted data into dataframe
    graph1 = pd.read_csv(input1)
    graph2 = pd.read_csv(input2)
    graph3 = pd.read_csv(input3)

    # separate into 2 different dataframes based on EPC for each test
    EPC1_1 = graph1[graph1['EPC'] == 'A10000000000000000000000']
    EPC2_1 = graph1[graph1['EPC'] == 'A20000000000000000000000'] # test 1 done
    EPC1_2 = graph2[graph2['EPC'] == 'A10000000000000000000000']
    EPC2_2 = graph2[graph2['EPC'] == 'A20000000000000000000000'] # test 2 done
    EPC1_3 = graph3[graph3['EPC'] == 'A10000000000000000000000']
    EPC2_3 = graph3[graph3['EPC'] == 'A20000000000000000000000'] # test 3 done

    # unwrap the phase data for each test
    EPC1_1[p_col] = np.unwrap(EPC1_1[p_col])
    EPC2_1[p_col] = np.unwrap(EPC2_1[p_col]) # test 1 done
    EPC1_2[p_col] = np.unwrap(EPC1_2[p_col])
    EPC2_2[p_col] = np.unwrap(EPC2_2[p_col]) # test 2 done
    EPC1_3[p_col] = np.unwrap(EPC1_3[p_col])
    EPC2_3[p_col] = np.unwrap(EPC2_3[p_col]) # test 3 done

    # PLOTTING
    # create figure of 2x2 subplot region
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # subplot 1: top left
    axs[0, 0].plot(EPC1_1['TimeValue'], EPC1_1[p_col], marker = 'o', linestyle = '-', label = '1')
    axs[0, 0].plot(EPC1_2['TimeValue'], EPC1_2[p_col], marker = 'o', linestyle = '-', label = '2')
    axs[0, 0].plot(EPC1_3['TimeValue'], EPC1_3[p_col], marker = 'o', linestyle = '-', label = '3')
    axs[0, 0].set_ylabel('Phase Diff (rads)')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_title('A1 Phase vs. Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # subplot 2: top right
    axs[0, 1].plot(EPC1_1['TimeValue'], EPC1_1['RSSI'], marker = 'o', linestyle = '-', label = '1')
    axs[0, 1].plot(EPC1_2['TimeValue'], EPC1_2['RSSI'], marker = 'o', linestyle = '-', label = '2')
    axs[0, 1].plot(EPC1_3['TimeValue'], EPC1_3['RSSI'], marker = 'o', linestyle = '-', label = '3')
    axs[0, 1].set_ylabel('RSSI (dBm)')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_title('A1 RSSI vs. Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # subplot 3: bot left
    axs[1, 0].plot(EPC2_1['TimeValue'], EPC2_1[p_col], marker = 'o', linestyle = '-', label = '1')
    axs[1, 0].plot(EPC2_2['TimeValue'], EPC2_2[p_col], marker = 'o', linestyle = '-', label = '2')
    axs[1, 0].plot(EPC2_3['TimeValue'], EPC2_3[p_col], marker = 'o', linestyle = '-', label = '3')
    axs[1, 0].set_ylabel('Phase Diff (dBm)')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_title('A2 Phase vs. Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # subplot 4: bot right
    axs[1, 1].plot(EPC2_1['TimeValue'], EPC2_1['RSSI'], marker = 'o', linestyle = '-', label = '1')
    axs[1, 1].plot(EPC2_2['TimeValue'], EPC2_2['RSSI'], marker = 'o', linestyle = '-', label = '2')
    axs[1, 1].plot(EPC2_3['TimeValue'], EPC2_3['RSSI'], marker = 'o', linestyle = '-', label = '3')
    axs[1, 1].set_ylabel('RSSI (dBm)')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_title('A2 RSSI vs. Time')
    axs[1, 1].legend()
    axs[1, 1].grid(True)


    #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.4, wspace=0.4)
    fig.suptitle(title, fontsize=16)
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.tight_layout()

    # dpi                   : resolution
    # bbox_inches = 'tight' : ensures it saves all components of figure
    fig.savefig(f'Graphs/REV3 3m/{title}.png', dpi=300, bbox_inches='tight')

    # show the figure
    #plt.show()

# define main file names for changing
input1 = 'Data/REV3 3m/1 Lat Raise/1_2s_2_2024-06-19_14-39-01.csv'
input2 = 'Data/REV3 3m/1 Lat Raise/1_2s_2_2024-06-19_14-39-15.csv'
input3 = 'Data/REV3 3m/1 Lat Raise/1_2s_2_2024-06-19_14-39-30.csv'
title = '1: Lateral Raise Gesture - REV3 3m Data'

# define output csv locations
output1 = 'NewData1.csv'
output2 = 'NewData2.csv'
output3 = 'NewData3.csv'

# other variables
p_col = 'PhaseAngle'

# call the reformatting function
Format(input1, output1, p_col)
Format(input2, output2, p_col)
Format(input3, output3, p_col)

# plot all 3 csvs on 4 subplots
plot3csv(output1, output2, output3, p_col, title)

print("-------------------- FINISHED --------------------\n\n")