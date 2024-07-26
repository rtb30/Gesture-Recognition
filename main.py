# import functions
from formatData import format
from fileNames import get_csv_all, clear_folder

# this function is to reformat and save a .h5 file for set of gestures
def main(root_dir):
    # delete exsiting output files at designated path
    #clear_folder(str(rev_path), '*.csv')
    #clear_folder('HDF5_formatted', '*.h5')

    # define lists that contain all csv file path, and where the new data will be stored
    csv_path, labels = get_csv_all(root_dir)

    # h5 variables
    h5_flag = 1
    h5_name = 'ply_data_test'

    # length: [interp flag, length, max length flag]
    length = [1, 20, 0]

    # format and filter all data and write to .csvs & .h5
    format(csv_path, h5_flag, length, h5_name, labels)

if __name__ == '__main__':
    # declare root dir that contains subfolders for each gesture type
    root_dir = 'Data/REV7/2 Sahar Golipoor/SG 1.5m'
    main(root_dir)

# TO DO
# change how HDF5 files are saved
# add a way to combine data from diff participants
