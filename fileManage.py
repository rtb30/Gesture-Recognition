# import
import os
import glob
import re

# this function clears a specific file folder
def clear_folder(folder_path, ext):
    # Construct the file pattern to match extension in specific folder
    file_pattern = os.path.join(folder_path, ext)
    
    # List all files in the folder
    delete_files = glob.glob(file_pattern)
    
    # Iterate through the list of CSV files and delete each file
    for file in delete_files:
        try:
            os.remove(file)
            #print(f'Deleted: {file}')
        except OSError as e:
            print(f"Error: {file} - {e.strerror}")

def clear_directory(directory_path, ext):
    for gesture_folder in sorted(os.listdir(directory_path)):
        gesture_path = os.path.join(directory_path, gesture_folder)
        clear_folder(gesture_path, ext)

    print('\n-------------- FINISHED DELETING DIRECTORY --------------\n')

# this function finds all csv files inside a specified folder from main to
# store the correct full path of each dataset in an array
def get_csv_filenames(folder_path):        
    # use os to list all files in specified folder
    all_files = os.listdir(folder_path)
    csv_files = [file for file in all_files if file.endswith('.csv') and file != '.DS_Store']

    # augment the name to include the full path
    for i in range(len(csv_files)):
        csv_files[i] = folder_path + '/' + csv_files[i]
        #if i > 10:
        #    break

    # return file names list
    return csv_files

# this function creates a list with all the csv files in a directory
def get_csv_all(root_dir):
    # init list to hold all csv_path names
    csv_path = []
    labels = []

    for item in os.listdir(root_dir):
        if item == '.DS_Store':
            file_path = os.path.join(root_dir, item)
            os.remove(file_path)
            #print(f'Removed {file_path}')

    # Read each subfolder (gesture type)
    for i, gesture_folder in enumerate(sorted(os.listdir(root_dir), key = numerical_sort)):
        # ignore gesture folders
        #if gesture_folder in ['20 Circle Clockwise', '21 Circle Counterclockwise']:
        #    continue

        # save gesture path per participant
        gesture_path = os.path.join(root_dir, gesture_folder)
        #print(gesture_path)

        # Read each CSV file in the gesture subfolder and create label
        for csv_file in os.listdir(gesture_path):
            if csv_file.endswith('.csv'):
                csv_path.append(os.path.join(gesture_path, csv_file))
                name = f'gesture{i + 1}'
                labels.append(name)

        #if i >= 8:
        #    break

    return csv_path, labels

# this function is to return a list of directory paths of each gesture per 1 participant
# sorted numerically
def get_gesture_folders(participant_directory):
    # create empty list for gesture paths
    gesture_path = []

    # find all the gesture folder per participant and sort them numerically
    for gesture_folder in sorted(os.listdir(participant_directory), key = numerical_sort):
        # ignore folders
        if gesture_folder in ['.DS_Store']:#, '20 Circle Clockwise', '21 Circle Counterclockwise']:
            continue

        # this is a list of all the path names to each gesture per 1 participant
        gesture_path.append(os.path.join(participant_directory, gesture_folder))

    return gesture_path

# the function extracts the numerical part from a string for sorting
def numerical_sort(value):
    # uses a regular expression to find all sequences of digits in the input string value
    # r'\d+'    : raw string containing the regular exp pattern (can be anywhere in string)
    # \d        : any digit
    # +         : will add on any preceding numerical values
    parts = re.findall(r'\d+', value) 

    # finds the first element in the parts array and converts to integer
    # if parts is empty return 0
    return int(parts[0]) if parts else 0