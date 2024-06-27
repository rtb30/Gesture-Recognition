# import functions
from formatData import format
from plottingData import plot_2D, plot_3D
from preprocData import rolling, gaussian, savgol, detrend

# have a function that does this maybe?
input1 = 'Data/REV3 3m/7 Swipe Right/7_2s_2_2024-06-19_14-46-03.csv'
input2 = 'Data/REV3 3m/7 Swipe Right/7_2s_2_2024-06-19_14-46-17.csv'
input3 = 'Data/REV3 3m/7 Swipe Right/7_2s_2_2024-06-19_14-46-32.csv'
inputs = [input1, input2, input3]
title = 'G7: Swipe Right - REV3 3m'

# define output csv locations
# have a function to automate?
output1 = 'Formatted1.csv'
output2 = 'Formatted2.csv'
output3 = 'Formatted3.csv'
csv_formatted = [output1, output2, output3]

# define output h5 locations
h5_1 = 'Formatted1.h5'
h5_2 = 'Formatted2.h5'
h5_3 = 'Formatted3.h5'
h5_files = [h5_1, h5_2, h5_3]

# other variables
# do i want this?
phase = 'PhaseAngle'
RSSI = 'RSSI'


# call the reformatting function
EPC_sep = format(inputs, csv_formatted, phase, RSSI, h5_files)

# call the filtering functions
EPC_sep = savgol(EPC_sep, phase)
EPC_sep = gaussian(EPC_sep, phase)
EPC_sep = rolling(EPC_sep, phase)

# plot all 3 datasets separated by EPC into 2 graphs (Phase & RSSI)
#plot_2D(phase, RSSI, title, EPC_sep)

# plot all 3 datasets on a 3D plot (x, y, z) = (RSSI, EPC, phase)
plot_3D(phase, RSSI, EPC_sep, title)

# git commands 
# git status (dont really need this)
# git add .
# or git add <file path>
# git commit -m "Your message"
# git push origin <branch name> (usually just main)