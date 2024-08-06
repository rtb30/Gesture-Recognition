# import
import numpy as np
from scipy.stats import median_abs_deviation

# this function normalizes RSSI data by EPC
def RSSI_normalize_EPC(EPC_sep, EPC_count, RSSI_flag, RSSI_val):
    if RSSI_flag == 1:
        # initialize dictionaries to store min & max RSSI values by EPC 
        # stores giant numbers to be replaced after the first iteration
        RSSI_min_dict = {i: float('inf') for i in range(1, EPC_count + 1)}
        RSSI_max_dict = {i: float('-inf') for i in range(1, EPC_count + 1)}
        
        # iterate and find min & max RSSI by EPC
        for df in EPC_sep:
            if not df.empty:
                EPC_value = df['EPC'].iloc[0]
                RSSI_min_dict[EPC_value] = min(RSSI_min_dict[EPC_value], df['RSSI'].min())
                RSSI_max_dict[EPC_value] = max(RSSI_max_dict[EPC_value], df['RSSI'].max())
        
        #print(RSSI_min_dict)
        #print(RSSI_max_dict)
        # store min and max values for each EPC
        RSSI_min_list = [RSSI_min_dict[i] for i in range(1, EPC_count + 1)]
        RSSI_max_list = [RSSI_max_dict[i] for i in range(1, EPC_count + 1)]
        RSSI_val.append(RSSI_min_list)
        RSSI_val.append(RSSI_max_list)

    # normalize the RSSI data in each dataframe
    for df in EPC_sep:
        if not df.empty:
            EPC_value = df['EPC'].iloc[0]
            min_val = RSSI_val[0][EPC_value - 1]
            max_val = RSSI_val[1][EPC_value - 1]
            df['RSSI'] = (df['RSSI'] - min_val) / (max_val - min_val)
        
        # Unwrap all phase data
        df['PhaseAngle'] = np.unwrap(df['PhaseAngle'])
        
        # Reset the index and drop the old index
        df.reset_index(drop=True, inplace=True)

    return EPC_sep, RSSI_val

# this function normalizes the RSSI data based on the absolute minimum RSSI value
def RSSI_normalize(EPC_sep, RSSI_flag, RSSI_val):
    # find absolute min of RSSI
    if(RSSI_flag == 1):
        RSSI_min_list = []
        RSSI_max_list = []
        for i in range(len(EPC_sep)):
            if (EPC_sep[i].empty == False):
                RSSI_min_list.append(min(EPC_sep[i]['RSSI']))
                RSSI_max_list.append(max(EPC_sep[i]['RSSI']))

        RSSI_val.append(min(RSSI_min_list))
        RSSI_val.append(max(RSSI_max_list))
    
    for i in range(len(EPC_sep)):
        # normalize all RSSI data
        EPC_sep[i]['RSSI'] = (EPC_sep[i]['RSSI'] - RSSI_val[0]) / (RSSI_val[1] - RSSI_val[0])

        # unwrap all phase data by EPC, can set an argument 'discont' to custom threshold
        EPC_sep[i]['PhaseAngle'] = np.unwrap(EPC_sep[i]['PhaseAngle'])

        # reset the index and drop the old index
        EPC_sep[i] = EPC_sep[i].reset_index(drop = True)

    return EPC_sep, RSSI_val

# this function normalizes the phase data based on the absolute max phase value
def phase_normalize(EPC_sep, phase_flag, phase_val):
    # find absolute min and max phase angle after unwrapping
    if(phase_flag == 1):
        phase_min_list = []
        phase_max_list = []
        for i in range(len(EPC_sep)):
            if (EPC_sep[i].empty == False):
                phase_min_list.append(min(EPC_sep[i]['PhaseAngle']))
                phase_max_list.append(max(EPC_sep[i]['PhaseAngle']))

        phase_val.append(min(phase_min_list))
        phase_val.append(max(phase_max_list))
    
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = (EPC_sep[i]['PhaseAngle'] - phase_val[0]) / (phase_val[1] - phase_val[0])

    return EPC_sep, phase_val

# this function normalizes phase data EPC
def phase_normalize_EPC(EPC_sep, EPC_count, phase_flag, phase_val):
    if phase_flag == 1:
        # initialize dictionaries to store min & max phase values by EPC 
        # stores giant numbers to be replaced after the first iteration
        phase_min_dict = {i: float('inf') for i in range(1, EPC_count + 1)}
        phase_max_dict = {i: float('-inf') for i in range(1, EPC_count + 1)}
        
        # iterate and find min & max phase by EPC
        for df in EPC_sep:
            if not df.empty:
                EPC_value = df['EPC'].iloc[0]
                phase_min_dict[EPC_value] = min(phase_min_dict[EPC_value], df['PhaseAngle'].min())
                phase_max_dict[EPC_value] = max(phase_max_dict[EPC_value], df['PhaseAngle'].max())
        
        #print(phase_min_dict)
        #print(phase_max_dict)
        # store min and max values for each EPC
        phase_min_list = [phase_min_dict[i] for i in range(1, EPC_count + 1)]
        phase_max_list = [phase_max_dict[i] for i in range(1, EPC_count + 1)]
        phase_val.append(phase_min_list)
        phase_val.append(phase_max_list)

    # normalize the phase data in each dataframe
    for df in EPC_sep:
        if not df.empty:
            EPC_value = df['EPC'].iloc[0]
            min_val = phase_val[0][EPC_value - 1]
            max_val = phase_val[1][EPC_value - 1]
            df['PhaseAngle'] = (df['PhaseAngle'] - min_val) / (max_val - min_val)

    return EPC_sep, phase_val

# this function standardizes the phase values with a mean of 0 and standard deviation of 1
# this can help for data not suited for min-max normalization
def phase_standardize(EPC_sep, phase_flag, phase_val):
    # Calculate mean and standard deviation of unwrapped phase angles
    if phase_flag == 1:
        phase_mean_list = []
        phase_std_list = []
        for i in range(len(EPC_sep)):
            if not EPC_sep[i].empty:
                phase_mean_list.append(np.mean(EPC_sep[i]['PhaseAngle']))
                phase_std_list.append(np.std(EPC_sep[i]['PhaseAngle']))

        # Store the global mean and standard deviation
        phase_val.append(np.mean(phase_mean_list))
        phase_val.append(np.mean(phase_std_list))
    
    # Apply standardization to phase angles
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = (EPC_sep[i]['PhaseAngle'] - phase_val[0]) / phase_val[1]

    return EPC_sep, phase_val

# this function scales the data to a -1 to 1 range (Z-score normalization) instead of a 0 to 1 range (standard normalization)
def phase_scale(EPC_sep, phase_flag, phase_val):
    if phase_flag == 1:
        phase_min_list = []
        phase_max_list = []
        for i in range(len(EPC_sep)):
            if not EPC_sep[i].empty:
                phase_min_list.append(min(EPC_sep[i]['PhaseAngle']))
                phase_max_list.append(max(EPC_sep[i]['PhaseAngle']))

        phase_val.append(min(phase_min_list))
        phase_val.append(max(phase_max_list))
    
    for i in range(len(EPC_sep)):
        # Scale to -1 to 1 range
        EPC_sep[i]['PhaseAngle'] = 2 * (EPC_sep[i]['PhaseAngle'] - phase_val[0]) / (phase_val[1] - phase_val[0]) - 1

    return EPC_sep, phase_val

# Use robust measures of central tendency and dispersion (like median and MAD) to perform Z-score normalization
def standardize_robust(EPC_sep, phase_flag, phase_val, col):
    if phase_flag == 1:
        # Collect phase data from all EPCs
        all_phases = np.concatenate([df[col].values for df in EPC_sep if not df.empty])
        
        # Compute robust statistics
        median = np.median(all_phases)
        mad = median_abs_deviation(all_phases)
        phase_val.append(median)
        phase_val.append(mad)
    
    # Normalize phase data
    for df in EPC_sep:
        if not df.empty:
            df[col] = (df[col] - phase_val[0]) / phase_val[1]
            df.reset_index(drop=True, inplace=True)
    
    return EPC_sep, phase_val