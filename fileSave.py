import pandas as pd
import numpy as np
import h5py

def saveto_csv(data_new, outputs):
    # store dataframe in new csv file, and omit index numbers
    for i in range(len(data_new)):
        data_new[i].to_csv(outputs[i], index = False)

    print('\n------------------ ' + str(len(data_new)) + ' .csv files were saved -----------------\n')

def saveto_h5(data_new):
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
    with h5py.File('HDF5_formatted/train_data.h5', 'w') as h5f:
        h5f.create_dataset('data', data = data_array)
        h5f.create_dataset('label', data = label_array)

    print('-------------------- .h5 file was saved --------------------\n')