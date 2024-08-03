# import functions
from formatData import format
from fileManage import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants

# this function is to reformat and save a .h5 file for set of gestures
def main(combined_directory, root_dir):

    ############################ SET FLAGS ##########################
    h5_flag = 1         # determines if h5 files are saved
    length = [1, 20, 0] # [interp flag, length, max length flag]
    data_flag = [1, 1]

    #################### COMPLETE TRAINING DATA #####################
    # clear the combined data directory and HDF5 folder
    clear_directory('Combined Data/3m', '*.csv')
    clear_folder('HDF5_formatted', '*.h5')

    # find all wanted participants to be apart of training data
    # and store in the combined directory
    participant_directories = get_participants()
    combine_participants(participant_directories, combined_directory)
    csv_path_combined, labels_combined = get_csv_all(combined_directory)

    # define h5 file name 
    h5_name = 'ply_data_train'

    # format data
    train_normalization = format(csv_path_combined, h5_flag, length, h5_name, labels_combined, data_flag)

    ###################### COMPLETE TESTING DATA #####################
    # get all csv files from testing participant directory
    csv_path, labels = get_csv_all(root_dir)

    # define h5 file name
    h5_name = 'ply_data_test'

    # format data
    format(csv_path, h5_flag, length, h5_name, labels, train_normalization)

if __name__ == '__main__':
    #declare root dir that contains subfolders for each gesture & set combine flag
    combined_directory = 'Combined Data/3m'

    # declare root dir that contains subfolders for each gesture for test participant
    root_dir = 'Data/REV7/6 Rick Brophy/RB 3m'

    main(combined_directory, root_dir)

# TO DO
# 1. what other augmentation techniques are there? do i know if the ones im using are working?
# 4. fix data normalization by EPC
# 5. fix rdp interp
# 6. remove data if there is less than a certain amount of reads?????
# 7. finish recording general patterns, can we remove any gestures?
    # if rssi and phase doesnt change much, set all to 0
        # ^for single handed gestures^
# 8. did desk height have to do with high reads? what did?
# 9. look into better smoothing / filtering techniques
    # savgol
    # gaussian
    # jittering?
    # others?
# 10. are the batches generated randomly?

# RETRY AFTER ACCURACY = 70%
# 1. interpolation length
# 2. convolution layers
# 3. model preprocessing