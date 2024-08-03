# import
import os
from fileManage import get_gesture_folders
import shutil

def copy_files(gesture_directory, destination_directory):
    # walks through directory tree to pull out csv file paths
    for root, _, files in os.walk(gesture_directory):
        for file in files:
            if file.endswith('.csv'):
                src_file_path = os.path.join(root, file)

            # copy the file to the destination directory
            shutil.copy2(src_file_path, destination_directory)

def combine_participants(participant_directories, combined_directory): 
    all_gesture_paths = []
    participant_count = len(participant_directories)

    combined_gesture_directories = get_gesture_folders(combined_directory)
    
    for i in range(participant_count):
        all_gesture_paths.append(get_gesture_folders(participant_directories[i]))

    for i in range(participant_count):
        for j in range(len(all_gesture_paths[0])):
            copy_files(all_gesture_paths[i][j], combined_gesture_directories[j])
        #print(f'Just copied {len(all_gesture_paths[0])} gestures for participant {i+1}')
    
    print('----------- FINISHED COMBINING TRAINING DATA ------------\n')
        
def get_participants():
    participant_directories = ['Data/REV7/1 Stephan Sigg/SS 3m',
                               'Data/REV7/2 Sahar Golipoor/SG 3m',
                               'Data/REV7/3 Noemi Ippolito/NI 3m',
                               'Data/REV7/4 Giorgio Micaletto/GM 3m',
                               'Data/REV7/5 Ying Liu/YL 3m',
                               'Data/REV7/7 Ines Mesquita/IM 3m',
                               'Data/REV7/8 Maxwell Sun/3m',
                               'Data/REV7/9 Niilo Heimonen/NH 3m',
                               'Data/REV7/10 Justin Han/JH 3m',
                               'Data/REV7/11 Mevlude Alizade/MA 3m',
                               'Data/REV7/12 Simeona Hein/SH 3m']
    
    return participant_directories