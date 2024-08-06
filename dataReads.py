# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
from fileManage import get_csv_all

# this function formats the original data exported from the ItemTest program
# made by IMPINJ. The output of this function returns a dataframe list
# which contains RSSI & phase data based on EPC and iteration for 1 gesture
def format_data(inputs, labels, saveMe):

    ############################### FUNCTION VARIABLES ###############################
    # init empty lists
    data = []
    EPC_sep = []
    data_new = []
    EPC_count_list = []

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
        #print(f'gesture number {i+1} has {EPC_count_list[i]} tags, file name {inputs[i]}')

    # find the maximum amount of tags used
    EPC_count = max(EPC_count_list)
    #EPC_count = 4

    # replace EPC with numeric values
    #for i in range(EPC_count):
    #    mapping[f'A{i + 1}0000000000000000000000'] = (i + 1)

    EPC_count = 8
    mapping = {'A10000000000000000000000': 1,
               'A20000000000000000000000': 2,
               'A30000000000000000000000': 3,
               'A40000000000000000000000': 4,
               'A60000000000000000000000': 5,
               'A70000000000000000000000': 6,
               'A80000000000000000000000': 7,
               'A90000000000000000000000': 8}

    # create another data set with separate numercial EPC values
    for i in range(len(data)):
        data[i]['EPC'] = data[i]['EPC'].replace(mapping)

        for j in range(1, EPC_count + 1):
            EPC_sep.append(data[i][data[i]['EPC'] == j])
            
            if((j == 1 or j == 2) and labels[i] == 'gesture1'):
                EPC_sep[-1] = EPC_sep[-1].iloc[0:0]
                
            if(j == 7 and (labels[i] == 'gesture1' or labels[i] == 'gesture2' or labels[i] == 'gesture3'
                           or labels[i] == 'gesture4' or labels[i] == 'gesture5' or labels[i] == 'gesture6'
                           or labels[i] == 'gesture7' or labels[i] == 'gesture8' or labels[i] == 'gesture9')):
                EPC_sep[-1] = EPC_sep[-1].iloc[0:0]

    #for i in range(len(data)):
    #    print(f'This is data set {i}:')
    #    print(data[i], '\n')

    #for i in range(len(EPC_sep)):
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

    # count how many times each tag appears per gesture
    tag_counter(data_new, EPC_count, labels, saveMe, EPC_sep)

def tag_counter(data_new, EPC_count, labels, saveMe, EPC_sep):
    count = 0
    sum = 0
    cols = []
    data_len = len(data_new)

    sum_dict = {i: 0 for i in range(1, EPC_count + 1)}
    count_dict = {i: 0 for i in range(1, EPC_count + 1)}
    label_dict = {i: 0 for i in range(1, 21)}

    for i in range(1, 22):
        label_dict[i] = (f'gesture{i}')

    cols.append('EPC')
    for i in range(1, 22):
        cols.append(f'gesture{i}')

    df = pd.DataFrame(columns = cols)

    for i in range(EPC_count):
        df.loc[i, 'EPC'] = f'A{i+1}'

    for j in range(1, EPC_count + 1):
        print(f'Finding A{j} tags')
        for i in range(len(data_new)):
            sum = sum + data_new[i]['EPC'].value_counts().get(j, 0)
    
            count = count + 1
    
            if(count == 15):
                df.loc[j-1, labels[i]] = sum
                print(f'{labels[i]} has a total of {sum} tags')

                count = 0
                sum = 0

        k = 0
        print()


    '''
    for EPC_df in EPC_sep:
        if not EPC_df.empty:
            EPC_value = EPC_df['EPC'].iloc[0]
            #print(f'Finding A{EPC_value} tags')
            sum_dict[EPC_value] += EPC_df['EPC'].value_counts().get(EPC_value, 0)
            count_dict[EPC_value] += 1

    print(sum_dict)

    for i in range(data_len):
        for j in range(1, EPC_count + 1):
            df.loc[j-1, labels[i]] = sum_dict[j]
    '''

    df.to_csv(saveMe, index = False)

def main():
    # declare root dir that contains subfolders for each gesture for test participant
    root_dir = 'Data/REV7/12 Simeona Hein/SH 3m'
    saveMe = 'dataReads/12 SH.csv'

    # get all csv files from testing participant directory
    csv_path, labels = get_csv_all(root_dir)

    # format data
    format_data(csv_path, labels, saveMe)

if __name__ == '__main__':
    main()

