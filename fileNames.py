# import
import os

# this functions finds all csv files inside a specified folder from main to
# store the correct full path of each dataset in an array
def get_csv_filenames(folder_path):
    # use os to list all files in specified folder
    csv_files = os.listdir(folder_path)

    # augment the name to include the full path
    for i in range(len(csv_files)):
        csv_files[i] = folder_path + '/' + csv_files[i]

    # return vector of file names
    return csv_files

# this function uses the length of inputs to store names of the formatted data
def get_output_filenames(inputs):
    # create empty arrays
    csv_formatted = []
    h5_files = []

    # for loop to iterate over filenames 
    for i in range(len(inputs)):
        csv_formatted.append(f'Formatted{i + 1}.csv')
        h5_files.append(f'Formatted{i + 1}.h5')

    # return both arrays
    return csv_formatted, h5_files