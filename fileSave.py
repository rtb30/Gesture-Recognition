import numpy as np
import h5py

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