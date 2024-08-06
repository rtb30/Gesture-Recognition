# import functions
from formatData import format
from fileManage import get_csv_all, clear_folder, clear_directory
from combine import combine_participants, get_participants
import sys

# this function is to reformat and save a .h5 file for set of gestures
def main(combined_directory, root_dir):

    ############################ SET FLAGS ##########################
    h5_flag = 1         # determines if h5 files are saved
    length = [1, 20] # [interp flag, length]
    norm_flag = 1

    #################### COMPLETE TRAINING DATA #####################
    if 'Combined Data' not in combined_directory:
        print('\n*********************************************************************')
        print('* The destination directory is not the allocated combined directory *')
        print('*********************************************************************\n')
        sys.exit(1)

    # clear the combined data directory and HDF5 folder
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
    phase_val_tx = []

    # format data
    RSSI_val, phase_val, phase_val_tx = format(csv_path_combined, h5_flag, length, h5_name, 
                                 comb_labels, norm_flag, RSSI_val, phase_val, phase_val_tx)

    ###################### COMPLETE TESTING DATA #####################
    # get all csv files from testing participant directory
    csv_path, labels = get_csv_all(root_dir)

    # define h5 file name and turn off normalization
    h5_name = 'ply_data_test'
    norm_flag = 0

    # format data
    format(csv_path, h5_flag, length, h5_name, 
           labels, norm_flag, RSSI_val, phase_val, phase_val_tx)

if __name__ == '__main__':
    #declare root dir that contains subfolders for each gesture & set combine flag
    combined_directory = 'Combined Data/3m'

    # declare root dir that contains subfolders for each gesture for test participant
    root_dir = 'Data/REV7/6 Rick Brophy/RB 3m'

    main(combined_directory, root_dir)

################################ SCRIPT TO DO LIST ################################
# 2. graph data to find deletable tags & gestures
    # use best tx & norm technique from above
# 3. look into better smoothing / filtering techniques
    # savgol
    # gaussian
    # exponential moving avg
    # lowess
# 4. feature engineering 
    # temporal      : gesture duration
    # statistical   : mean & variance
# 5. augmentation
    # jittering
    # warping
    # rotation and flipping
# 7. what contriubuted to high reads
# 9. fix rdp interp

################################ MODEL TO DO LIST ################################
# 1. reduce overfitting!!!!!
# 2. Questions
    # What preprocessing does the model do?
    # does it use dropout?
        # removes certain nodes to prevent overfitting
    # are there other models other than the edge cnn?
    # how can i implement validtion sets and cross-validation
        # validation sets   : pre-tune hyperparameters
        #cross-val          : divide dataset into folds to more accurately test the model on unseen data
    # can we make a simple nn?
        # less neurons in conv layers, etc
# 3. Evaluation metrics
    # precision         : accuracy of positive results  (TP / (TP + FP))
    # recall            : find relevant instances       (TP / (TP + FN))
    # F1                : mean of precisions & recall   (2 * (Precision * Recall) / (Precision + Recall))
    # confusion matrix 
