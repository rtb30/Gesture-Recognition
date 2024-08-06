# import functions
from formatDataforPlot import format
from plottingData import plot_2D, plot_3D, plot_2D_new, plot_gesture_data_interactive
from fileManage import get_csv_filenames

# this function is to reformat and plot a gesture
def main(root_dir):

    # define filenames for inputs
    inputs, labels = get_csv_filenames(root_dir)
    
    # length: [interp flag, length]
    length = [1, 15]

    # format all data
    EPC_sep, data_new = format(inputs, length, labels)

    # plot all 3 datasets separated by EPC into 2 graphs (Phase & RSSI)
    #plot_2D_new(title, data_new)

    #plot_gesture_data_interactive(data_new)

    # plot all 3 datasets on a 3D plot (x, y, z) = (RSSI, EPC, phase)
    plot_3D(EPC_sep)

if __name__ == '__main__':
    # define single gesture path and title for plot
    root_dir = 'Combined Data/1.5m/10 Arms Swing'

    main(root_dir)
