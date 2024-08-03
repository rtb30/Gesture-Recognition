# import
import numpy as np

def add_constant_offset(augment_df, RSSI_offset = 0.05, phase_offset = 1):
    # add offsets to RSSI and Phase
    augment_df['RSSI'] += RSSI_offset
    augment_df['PhaseAngle'] += phase_offset
    return augment_df

def sub_constant_offset(augment_df, RSSI_offset = 0.05, phase_offset = 1):
    # add offsets to RSSI and Phase
    augment_df['RSSI'] -= RSSI_offset
    augment_df['PhaseAngle'] -= phase_offset
    return augment_df

def add_gaussian_noise(augment_df, RSSI_std = 0.1, phase_std = 0.5):
    # add Gaussian noise to RSSI and Phase
    augment_df['RSSI'] += np.random.normal(0, RSSI_std, augment_df['RSSI'].shape)
    augment_df['PhaseAngle'] += np.random.normal(0, phase_std, augment_df['PhaseAngle'].shape)
    return augment_df

def add_offset_and_noise(augment_df, RSSI_offset = 0.05, phase_offset = 1, RSSI_std = 0.1, phase_std = 0.5):
    # add constant offset
    augment_df['RSSI'] += RSSI_offset
    augment_df['PhaseAngle'] += phase_offset

    # add Gaussian noise
    augment_df['RSSI'] += np.random.normal(0, RSSI_std, augment_df['RSSI'].shape)
    augment_df['PhaseAngle'] += np.random.normal(0, phase_std, augment_df['PhaseAngle'].shape)
    return augment_df

def sub_offset_and_noise(augment_df, RSSI_offset = 0.05, phase_offset = 1, RSSI_std = 0.1, phase_std = 0.5):
    # add constant offset
    augment_df['RSSI'] -= RSSI_offset
    augment_df['PhaseAngle'] -= phase_offset

    # add Gaussian noise
    augment_df['RSSI'] += np.random.normal(0, RSSI_std, augment_df['RSSI'].shape)
    augment_df['PhaseAngle'] += np.random.normal(0, phase_std, augment_df['PhaseAngle'].shape)
    return augment_df