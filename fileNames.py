# import
import os
import glob

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

# this function finds all csv files inside a specified folder from main to
# store the correct full path of each dataset in an array
def get_csv_filenames(folder_path):        
    # use os to list all files in specified folder
    csv_files = os.listdir(folder_path)

    # augment the name to include the full path
    for i in range(len(csv_files)):
        csv_files[i] = folder_path + '/' + csv_files[i]

    # return file names list
    return csv_files

# this function uses the length of inputs to store names of the formatted data
def get_output_filenames(inputs, rev_path):
    # create empty arrays
    csv_formatted = []

    # for loop to iterate over filenames 
    for i in range(len(inputs)):
        csv_formatted.append(str(rev_path) + f'/formatted{i + 1}.csv')

    # return both arrays
    return csv_formatted

# this function creates a list with all the csv files in a directory
def get_csv_all(root_dir):
    # init a dictionary to hold data categorized by gesture
    gesture_data = {}
    # init list to hold all csv_path names
    csv_path = []

    # Read each subfolder (gesture type)
    for gesture_folder in os.listdir(root_dir):
        gesture_path = os.path.join(root_dir, gesture_folder)
        if os.path.isdir(gesture_path):
            gesture = gesture_folder
            gesture_data[gesture] = []

        # Read each CSV file in the gesture subfolder
        for csv_file in os.listdir(gesture_path):
            if csv_file.endswith('.csv'):
                csv_path.append(os.path.join(gesture_path, csv_file))

    return csv_path