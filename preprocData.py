# import
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter
from scipy.signal import detrend

# rolling mean filter: smooths data by taking a moving average of each point
# window is the size of how many adjacent points are included
def rolling(EPC_sep, phase):
    for i in range(len(EPC_sep)):
        EPC_sep[i][phase] = EPC_sep[i][phase].rolling(window = 3).mean()
    return EPC_sep

# Gaussian filter: smooths data by applying a Gaussian kernel which gives more weight to the central 
# point and less weight as you traverse out
# signma is the stdv of the kernel, larger sigma, more smoothing
def gaussian(EPC_sep, phase):
    for i in range(len(EPC_sep)):
        EPC_sep[i][phase] = gaussian_filter1d(EPC_sep[i][phase], sigma = 1)
    return EPC_sep

# Savitzky-Golay filter: smooths data by using successive subsets of adjacent datapoints with a low-degree
# polynomial by the method of linear least squares
# window_length must be odd and greater than polyorder
def savgol(EPC_sep, phase):
    for i in range(len(EPC_sep)):
        EPC_sep[i][phase] = savgol_filter(EPC_sep[i][phase], window_length = 5, polyorder = 2)
    return EPC_sep

# Detrend function: removes any trend components of data
def detrend(EPC_sep, phase):
    for i in range(len(EPC_sep)):
        EPC_sep[i][phase] = detrend(EPC_sep[phase])
    return EPC_sep