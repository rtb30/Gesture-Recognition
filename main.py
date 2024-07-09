# import functions
from formatData import format
from plottingData import plot_2D, plot_3D
#from preprocData import rolling, gaussian, savgol, detrend
from fileNames import get_csv_filenames, get_output_filenames, get_csv_all, clear_folder
import os
import pandas as pd

# this function is to reformat and plot a gesture
def main1(folder_path, title):
    # delete exsiting output files at designated path
    clear_folder(str(rev_path), '*.csv')
    #clear_folder('HDF5_formatted', '*.h5')

    # define filenames for inputs and outputs
    inputs = get_csv_filenames(folder_path)
    csv_formatted = get_output_filenames(inputs, rev_path)

    # flags: [csv_flag, h5_flag]
    flags = [1, 0]
    h5_name = ''
    
    # length: [interp flag, length, max length flag]
    length = [0, 0, 0]

    # format all data
    EPC_sep = format(inputs, csv_formatted, flags, length, h5_name)

    # plot all 3 datasets separated by EPC into 2 graphs (Phase & RSSI)
    #plot_2D(title, EPC_sep)

    # plot all 3 datasets on a 3D plot (x, y, z) = (RSSI, EPC, phase)
    plot_3D(EPC_sep, title)

# this function is to reformat and save a .h5 file for set of gestures
def main2(root_dir, rev_path):
    # delete exsiting output files at designated path
    #clear_folder(str(rev_path), '*.csv')
    #clear_folder('HDF5_formatted', '*.h5')

    # define lists that contain all csv file path, and where the new data will be stored
    csv_path = get_csv_all(root_dir)
    csv_formatted_path = get_output_filenames(csv_path, rev_path)

    # flags: [csv_flag, h5_flag]
    flags = [0, 1]
    h5_name = 'train'

    # length: [interp flag, length, max length flag]
    length = [1, 30, 1]

    # format and filter all data and write to .csvs & .h5
    format(csv_path, csv_formatted_path, flags, length, h5_name)

if __name__ == '__main__':
    # define flags for which function to run
    main1_flag = 1
    main2_flag = 0

    if main1_flag == 1:
        # define folder path and title
        folder_path = 'Data/REV3 1.5m/7 Swipe Right'
        title = 'G7: Swipe Right - REV3 1.5m'
        rev_path = 'CSV_formatted/REV3'
        main1(folder_path, title)

    if main2_flag == 1:
        # declare root dir that contains subfolders for each gesture type
        root_dir = 'Data/REV4 1.5m'
        rev_path = 'CSV_formatted/REV4'
        main2(root_dir, rev_path)

# git commands 
# git status (dont really need this)
# git add .
# or git add <file path>
# git commit -m "Your message"
# git push origin <branch name> (usually just main)