# import functions
from formatData import format
from fileManage import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants
import sys

# this function is to reformat and save a .h5 file for set of gestures
def main(combined_directory, root_dir):

    ############################ SET FLAGS ##########################
    h5_flag = 1         # determines if h5 files are saved
    length = [1, 20, 0] # [interp flag, length, max length flag]
    norm_flag = 1

    #################### COMPLETE TRAINING DATA #####################
    # clear the combined data directory and HDF5 folder
    if 'Combined Data' not in combined_directory:
        print('\n*********************************************************************')
        print('* The destination directory is not the allocated combined directory *')
        print('*********************************************************************\n')
        sys.exit(1)

    clear_directory('Combined Data/3m', '*.csv')
    clear_folder('HDF5_formatted', '*.h5')

    # find all wanted participants to be apart of training data
    # and store in the combined directory
    participant_directories = get_participants()
    combine_participants(participant_directories, combined_directory)
    csv_path_combined, comb_labels = get_csv_all(combined_directory)

    # define h5 file name and data normalization values
    h5_name = 'ply_data_train'
    RSSI_val = []
    phase_val = []

    # format data
    RSSI_val, phase_val = format(csv_path_combined, h5_flag, length, h5_name, 
                                 comb_labels, norm_flag, RSSI_val, phase_val)

    ###################### COMPLETE TESTING DATA #####################
    # get all csv files from testing participant directory
    csv_path, labels = get_csv_all(root_dir)

    # define h5 file name and turn off normalization
    h5_name = 'ply_data_test'
    norm_flag = 0

    # format data
    format(csv_path, h5_flag, length, h5_name, 
           labels, norm_flag, RSSI_val, phase_val)

if __name__ == '__main__':
    #declare root dir that contains subfolders for each gesture & set combine flag
    combined_directory = 'Combined Data/3m'

    # declare root dir that contains subfolders for each gesture for test participant
    root_dir = 'Data/REV7/6 Rick Brophy/RB 3m'

    main(combined_directory, root_dir)

################################ TO DO ################################
# 2. remove data if there is less than a certain amount of reads
# 3. look into better smoothing / filtering techniques
    # savgol
    # gaussian
    # jittering?
    # others?
# 4. is all formatting doing what we expect?
# 5. what other augmentation techniques are there? do i know if the ones im using are working?
# 6. GRAPHICAL ANALYSIS
    # with and without augmentation, find resonable values
    # 
# 7. what contriubuted to high reads
# 8. go thru all code. add comments. see if it can be more efficient
# 9. feature engineering (statistical analysis on combined patterns)
# 9. fix rdp interp
# 10. how to handle empty EPCs? - augmentation can add shifts and noise to zeros

################################ RETRY AFTER ACCURACY = 70% ################################
# 1. interpolation length
# 2. convolution layers
# 3. combined normalization
# 4. all model hyperparameters
    # conv layers
    # batch size
    # learning rate

################################ Questions for lab ################################
# 1. What preprocessing does the model do?
# 2. does it use dropout?
# 3. the model overfits data
# 4. are there other models other than the edge cnn?
# 5. shoukd i be doing cross validation
# 6. can we make a simple nn?