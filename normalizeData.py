# import
import numpy as np

# this function normalizes the RSSI data based on the absolute minimum RSSI value
def RSSI_normalize_train(EPC_sep, RSSI_min_list, RSSI_flag):
    # find absolute min of RSSI
    if(RSSI_flag == 1):
        RSSI_min = min(RSSI_min_list)
    else:
        RSSI_min = RSSI_flag
    
    for i in range(len(EPC_sep)):
        # normalize all RSSI data
        EPC_sep[i]['RSSI'] = EPC_sep[i]['RSSI'] / RSSI_min

        # unwrap all phase data by EPC, can set an argument 'discont' to custom threshold
        EPC_sep[i]['PhaseAngle'] = np.unwrap(EPC_sep[i]['PhaseAngle'])

        # reset the index and drop the old index, not sure why i need this?
        EPC_sep[i] = EPC_sep[i].reset_index(drop = True)

    return EPC_sep, RSSI_min

# this function normalizes the RSSI data based on the minimum RSSI value per EPC
def RSSI_normalize_EPC(EPC_sep, EPC_count, RSSI_flag):

    if(RSSI_flag == 1):
        # create empty lists to store min RSSI data
        RSSI_min_list = []
        RSSI_min_tag_list = []

        # find min RSSI by EPC from all gestures and repetitions
        for j in range(1, EPC_count + 1):
            for i in range(len(EPC_sep)):
                if (EPC_sep[i].empty == False):
                    if(EPC_sep[i]['EPC'].iloc[0] == j):
                        #print(f'this is EPC data that only contains EPC{j}')
                        #print(EPC_sep[i])
                        RSSI_min_list.append(min(EPC_sep[i]['RSSI']))
                        #print(f'the RSSI min in this set is {RSSI_min_list[-1]}\n')
                        #print(RSSI_min_list)
            RSSI_min_tag_list.append(min(RSSI_min_list))
            RSSI_min_list = []

    else:
        RSSI_min_tag_list = RSSI_flag

    for j in range(1, EPC_count + 1):
        for i in range(len(EPC_sep)):
            if(EPC_sep[i]['EPC'].iloc[0] == j):
                EPC_sep[i]['RSSI'] = EPC_sep[i]['RSSI'] / RSSI_min_tag_list[j-1]

            # unwrap all phase data by EPC, can set an argument 'discont' to custom threshold
            EPC_sep[i]['PhaseAngle'] = np.unwrap(EPC_sep[i]['PhaseAngle'])

            # reset the index and drop the old index, not sure why i need this?
            EPC_sep[i] = EPC_sep[i].reset_index(drop = True)

    return EPC_sep, RSSI_min_tag_list

# this function normalizes the phase data based on the absolute max phase value
def phase_normalize_train(EPC_sep, phase_flag):

    if(phase_flag == 1):
        phase_max_list = []
        for i in range(len(EPC_sep)):
            if (EPC_sep[i].empty == False):
                phase_max_list.append(max(EPC_sep[i]['PhaseAngle']))

        phase_max = max(phase_max_list)

    else:
        phase_max = phase_flag
    
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = EPC_sep[i]['PhaseAngle'] / phase_max

    return EPC_sep, phase_max