# import functions
from formatData import format
from fileNames import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants

# this function is to reformat and save a .h5 file for set of gestures
def main(root_dir, combined_directory, combine_flag):
    ############### delete exsiting folders and combine participant data ################
    if(combine_flag == 1):
        clear_folder('HDF5_formatted', '*.h5')
        clear_directory('Combined Data/1.5m', '*.csv')
        participant_directories = get_participants()
        #combine_participants(participant_directories, combined_directory)

    ############ get csv_path from root directory and labels for all gestures ############
    csv_path, labels = get_csv_all(root_dir)

    ##################################### h5 variables ###################################
    h5_flag = 0
    h5_name = 'ply_data_train'

    ################### length: [interp flag, length, max length flag] ###################
    length = [1, 20, 0]

    ################ format and filter all data and write to .csvs & .h5 #################
    format(csv_path, h5_flag, length, h5_name, labels)

if __name__ == '__main__':
    # declare root dir that contains subfolders for each gesture & set combine flag
    root_dir = 'Combined Data/3m'

    combined_directory = 'Combined Data/3m'
    combine_flag = 1

    main(root_dir, combined_directory, combine_flag)

# TO DO
# 1. fix normalization with RSSI (by EPC and by entire set)
# 2. repeat normalization but with phase
# 3. remove A5 from all data
# 4. try interpolating with a cubic function instead of linear
# 5. try interpolating at different places instead of linear.
# 6. remove data if there is less than a certain amount of reads?????
# 7. finish recording general patterns, can we remove any single handed gestures?
    # if rssi and phase doesnt change much, set all to 0
        # ^for single handed gestures^
# 8. did desk height have to do with high reads? what did?
# 9. look into better smoothing / filtering techniques
    # savgol
    # gaussian
    # jittering?
    # others?
# 10. have giorgio help with fitting data
# 11. more efficient script