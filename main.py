# import functions
from formatData import format
from fileNames import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants

# this function is to reformat and save a .h5 file for set of gestures
def main(root_dir, combined_directory, combine_flag):
    ############### delete exsiting folders and combine participant data ################
    if(combine_flag == 1):
        clear_folder('HDF5_formatted', '*.h5')
        clear_directory('Combined Data/3m', '*.csv')
        participant_directories = get_participants()
        combine_participants(participant_directories, combined_directory)

    ############ get csv_path from root directory and labels for all gestures ############
    csv_path, labels = get_csv_all(root_dir)

    ##################################### h5 variables ###################################
    h5_flag = 1
    h5_name = 'ply_data_test'

    ################### length: [interp flag, length, max length flag] ###################
    length = [1, 30, 0]

    ################ format and filter all data and write to .csvs & .h5 #################
    format(csv_path, h5_flag, length, h5_name, labels)

if __name__ == '__main__':
    # declare root dir that contains subfolders for each gesture & set combine flag
    root_dir = 'Combined Data/3m'
    combined_directory = 'Combined Data/3m'
    combine_flag = 0
    main(root_dir, combined_directory, combine_flag)

# TO DO
# more efficienct code
# option to do certain amount of gestures or filter out tags
# have phase start from 0 every single time
# better filtering techniques
    # savgol
    # gaussian
    # interp