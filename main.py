# import functions
from formatData import format
from fileNames import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants

# this function is to reformat and save a .h5 file for set of gestures
def main(root_dir):
    # delete exsiting output files at designated path
    #clear_folder(str(rev_path), '*.csv')
    #clear_folder('HDF5_formatted', '*.h5')
    clear_directory('Combined Data/3m', '*.csv')

    # combine particpant data
    participant_directories = get_participants()
    combined_directory = 'Combined Data/3m'
    combine_participants(participant_directories, combined_directory)

    # define lists that contain all csv file path, and where the new data will be stored
    csv_path, labels = get_csv_all(root_dir)

    # h5 variables
    h5_flag = 1
    h5_name = 'ply_data_train'

    # length: [interp flag, length, max length flag]
    length = [1, 30, 0]

    # format and filter all data and write to .csvs & .h5
    format(csv_path, h5_flag, length, h5_name, labels)

if __name__ == '__main__':
    # declare root dir that contains subfolders for each gesture
    root_dir = 'Combined Data/3m'
    main(root_dir)

# TO DO
# change how HDF5 files are saved
# more efficienct code
