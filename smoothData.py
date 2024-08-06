# import
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter
from scipy.signal import detrend

# rolling mean filter: smooths data by taking a moving average of each point
# window is the size of how many adjacent points are included
# ***** this function deletes window - 1 points from the beginning of a dataframe *****
def rolling(EPC_sep):
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = EPC_sep[i]['PhaseAngle'].rolling(window = 3).mean()
    return EPC_sep

# Gaussian filter: smooths data by applying a Gaussian kernel which gives more weight to the central 
# point and less weight as you traverse out
# signma is the stdv of the kernel, larger sigma, more smoothing
def gaussian(EPC_sep):
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = gaussian_filter1d(EPC_sep[i]['PhaseAngle'], sigma = 1)
    return EPC_sep, 1

# savgol filter: smooths data by using successive subsets of adjacent datapoints with a low-degree
# polynomial by the method of linear least squares
# window_length must be odd and greater than polyorder & amount of data values
def savgol(EPC_sep):
    for i in range(len(EPC_sep)):
        if (EPC_sep[i].shape[0] > 5):
            EPC_sep[i]['PhaseAngle'] = savgol_filter(EPC_sep[i]['PhaseAngle'], window_length = 5, polyorder = 2)
        else:
            pass
    return EPC_sep, 1

# Detrend function: removes any trend components of data
def detrend(EPC_sep):
    for i in range(len(EPC_sep)):
        EPC_sep[i]['PhaseAngle'] = detrend(EPC_sep['PhaseAngle'])
    return EPC_sep