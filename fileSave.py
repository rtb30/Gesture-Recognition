import numpy as np
import h5py

def saveto_csv(data_new, outputs):
    # store dataframe in new csv file, and omit index numbers
    for i in range(len(data_new)):
        data_new[i].to_csv(outputs[i], index = False)

    print('------------------ ' + str(len(data_new)) + ' .csv files were saved -----------------\n')

# this function is to take a list of all the dataframes and create an HDF5 file. The output is:
# 2 datasets - Data and Label
# Data is a 3D matrix with (gestures, datapoints, and the 4 columns of data)
def saveto_h5_3Dmatrix(data_new, h5_name):
    # create empty lists to store HDF5 data
    data_list = []
    label_list = []

    # for loop to store dataframe data into HDF5 lists
    for i in range(len(data_new)):
        data_list.append(data_new[i][['TimeValue', 'EPC', 'RSSI', 'PhaseAngle']].values)
        label_list.append(i)

    # Determine the maximum length of data arrays
    max_length = max(len(data) for data in data_list)

    # Pad the arrays to ensure uniform length
    padded_data_list = []
    for data in data_list:
        if len(data) < max_length:
            # Pad with zeros or a suitable value
            padding = np.zeros((max_length - len(data), data.shape[1]))
            padded_data = np.vstack((data, padding))
        else:
            padded_data = data

        padded_data_list.append(padded_data)

    # convert lists to arrays to store into HDF5 file
    data_array = np.array(padded_data_list)
    label_array = np.array(label_list)

    # create HDF5 file and datasets (data & label)
    with h5py.File(f'HDF5_formatted/{h5_name}.h5', 'w') as h5f:
        h5f.create_dataset('data', data = data_array)
        h5f.create_dataset('label', data = label_array)

    print('-------------------- .h5 file was saved --------------------\n')

# this function is to take a list of all the dataframes and create an HDF5 file. The output is:
# datasets of each gesture are split by EPC
# each sub dataset are arrays containing RSSI and Phase data
def saveto_h5_gest_EPC_sep(data_new, h5_name):
    # Create empty lists to store HDF5 data
    data_list = []
    gesture_labels = []

    # Iterate over each dataframe in data_new
    for i, df in enumerate(data_new):
        # Extract necessary columns
        time_values = df['TimeValue'].values
        epcs = df['EPC'].values
        rssis = df['RSSI'].values
        phases = df['PhaseAngle'].values
        
        # Collect unique EPCs for this gesture
        unique_epcs = np.unique(epcs)

        # Create a dictionary to store data for each EPC
        gesture_data = {}
        for epc in unique_epcs:
            mask = (epcs == epc)
            epc_data = {
                'RSSI': rssis[mask],
                'Phase': phases[mask]
            }
            gesture_data[epc] = epc_data
        
        # Append the gesture data and label to lists
        data_list.append(gesture_data)
        gesture_labels.append(i)

    # Create HDF5 file and store data
    with h5py.File(f'HDF5_formatted/{h5_name}.h5', 'w') as h5f:
        for i, gesture_data in enumerate(data_list):
            group_name = f'gesture_{i + 1}'  # Group names like 'gesture_1', 'gesture_2', ...
            grp = h5f.create_group(group_name)
            
            # Store data for each EPC within the gesture group
            for epc, epc_data in gesture_data.items():
                grp.create_dataset(f'{epc}/RSSI', data=epc_data['RSSI'])
                grp.create_dataset(f'{epc}/Phase', data=epc_data['Phase'])
        
        # Store gesture labels
        h5f.create_dataset('labels', data=np.array(gesture_labels))

    print('-------------------- .h5 file was saved --------------------\n')

# this function is to take a list of all the dataframes and create an HDF5 file. The output is:
# 2 datasets - Data and Label
# Data is a 4D matrix with (gestures, datapoints, EPC, and the 2 columns of RSSI and Phase data)
def saveto_h5_4Dmatrix(EPC_sep, h5_name, labels, EPC_count):
    # number of gestures, datapoints, & EPC count
    num_gestures = int(len(EPC_sep) / EPC_count)
    num_datapoints = EPC_sep[0].shape[0]
    num_EPC = EPC_count

    # placeholder for the combined data array
    data = np.zeros((num_gestures, num_datapoints, num_EPC, 2))

    # iterate over each pair of DataFrames and populate the data array
    for i in range(num_gestures):
        for j in range(num_EPC):
            # get the DataFrame for the current tag
            df = EPC_sep[i * num_EPC + j]

            # populate the data array
            #data[i, :, j, 0] = df['TimeValue']
            data[i, :, j, 0] = df['RSSI']
            data[i, :, j, 1] = df['PhaseAngle']
            
    # Create the HDF5 file and save the datasets
    with h5py.File(f'HDF5_formatted/{h5_name}.h5', 'w') as f:
        f.create_dataset('data', data = data)

        # define string data type and create dataset
        dt = h5py.string_dtype(encoding = 'utf-8')  
        f.create_dataset('label', data = np.array(labels, dtype = dt))
        #f.create_dataset('label', data = np.array(labels))

    print('-------------------- .h5 file was saved --------------------\n')