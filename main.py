# import functions
from formatData import format
from plottingData import plot_2D, plot_3D
#from preprocData import rolling, gaussian, savgol, detrend
from fileNames import get_csv_filenames, get_output_filenames

def main(folder_path, title):
    # define filenames for inputs and outputs
    inputs = get_csv_filenames(folder_path)
    csv_formatted, h5_files = get_output_filenames(inputs)

    # other variables
    phase = 'PhaseAngle'
    RSSI = 'RSSI'

    # format all data
    EPC_sep = format(inputs, csv_formatted, phase, RSSI, h5_files)

    # plot all 3 datasets separated by EPC into 2 graphs (Phase & RSSI)
    #plot_2D(phase, RSSI, title, EPC_sep)

    # plot all 3 datasets on a 3D plot (x, y, z) = (RSSI, EPC, phase)
    plot_3D(phase, RSSI, EPC_sep, title)

if __name__ == '__main__':
    # define folder path and title
    folder_path = 'Data/REV3 1.5m/7 Swipe Right'
    title = 'G7: Swipe Right - REV3 1.5m'
    main (folder_path, title)

# git commands 
# git status (dont really need this)
# git add .
# or git add <file path>
# git commit -m "Your message"
# git push origin <branch name> (usually just main)