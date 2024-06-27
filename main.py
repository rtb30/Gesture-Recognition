# import
from formatData import Format
from plottingData import plot_2D, plot_3D

# have a function that does this maybe?
input1 = 'Data/REV2 1.5m/4 Pull/4_2s_2_2024-06-13_14-56-22.csv'
input2 = 'Data/REV2 1.5m/4 Pull/4_2s_2_2024-06-13_14-56-33.csv'
input3 = 'Data/REV2 1.5m/4 Pull/4_2s_2_2024-06-13_14-56-44.csv'
inputs = [input1, input2, input3]

# define output csv locations
# have a function to automate?
output1 = 'Formatted1.csv'
output2 = 'Formatted2.csv'
output3 = 'Formatted3.csv'
csv_formatted = [output1, output2, output3]

h5_1 = 'Formatted1.h5'
h5_2 = 'Formatted2.h5'
h5_3 = 'Formatted3.h5'
h5_files = [h5_1, h5_2, h5_3]

# other variables
# do i want this?
phase = 'PhaseAngle'
RSSI = 'RSSI'
title = 'G4: Pull - REV2 1.5m'

# call the reformatting function
# automate this?
EPC_sep = Format(inputs, csv_formatted, phase, RSSI, h5_files)

# plot all 3 datasets separated by EPC into 2 graphs (Phase & RSSI)
#plot_2D(phase, RSSI, title, EPC_sep)

# plot all 3 datasets on a 3D plot
plot_3D(phase, RSSI, EPC_sep, title)

# git commands 
# git status
# git add .
# or git add <file path>
# git commit -m "Your message"
# git push origin <branch name> (usually just main)