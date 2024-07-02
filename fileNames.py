# import
import os
import glob

def clear_folder(folder_path, ext):
    # Construct the file pattern to match extension in specific folder
    file_pattern = os.path.join(folder_path, ext)
    
    # List all files in the folder
    delete_files = glob.glob(file_pattern)
    
    # Iterate through the list of CSV files and delete each file
    for file in delete_files:
        try:
            os.remove(file)
            print(f'Deleted: {file}')
        except OSError as e:
            print(f"Error: {file} - {e.strerror}")


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
    # delete exsiting output files
    clear_folder('CSV_formatted', '*.csv')
    clear_folder('HDF5_formatted', '*.h5')

    # create empty arrays
    csv_formatted = []
    h5_files = []

    # for loop to iterate over filenames 
    for i in range(len(inputs)):
        csv_formatted.append(f'CSV_formatted/formatted{i + 1}.csv')
        h5_files.append(f'HDF5_formatted/formatted{i + 1}.h5')

    # return both arrays
    return csv_formatted, h5_files