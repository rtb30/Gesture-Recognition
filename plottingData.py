# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# this function uses 2D plots to show similarities between phase vs time and 
# RSSI vs time graphs dependent on iteration, also separated by EPC
def plot_2D(title, EPC_sep):
    # create figure of 2x2 subplot region
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # subplot 1: top left
    axs[0, 0].plot(EPC_sep[0]['TimeValue'], EPC_sep[0]['PhaseAngle'], marker = 'o', linestyle = '-', label = '1')
    axs[0, 0].plot(EPC_sep[2]['TimeValue'], EPC_sep[2]['PhaseAngle'], marker = 'o', linestyle = '-', label = '2')
    axs[0, 0].plot(EPC_sep[4]['TimeValue'], EPC_sep[4]['PhaseAngle'], marker = 'o', linestyle = '-', label = '3')
    axs[0, 0].set_ylabel('Phase Diff (rads)')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_xlim(left=0)
    axs[0, 0].set_title('A1 Phase vs. Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # subplot 2: top right
    axs[0, 1].plot(EPC_sep[0]['TimeValue'], EPC_sep[0]['RSSI'], marker = 'o', linestyle = '-', label = '1')
    axs[0, 1].plot(EPC_sep[2]['TimeValue'], EPC_sep[2]['RSSI'], marker = 'o', linestyle = '-', label = '2')
    axs[0, 1].plot(EPC_sep[4]['TimeValue'], EPC_sep[4]['RSSI'], marker = 'o', linestyle = '-', label = '3')
    axs[0, 1].set_ylabel('RSSI (Normalized)')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_xlim(left=0)
    axs[0, 1].set_title('A1 RSSI vs. Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # subplot 3: bot left
    axs[1, 0].plot(EPC_sep[1]['TimeValue'], EPC_sep[1]['PhaseAngle'], marker = 'o', linestyle = '-', label = '1')
    axs[1, 0].plot(EPC_sep[3]['TimeValue'], EPC_sep[3]['PhaseAngle'], marker = 'o', linestyle = '-', label = '2')
    axs[1, 0].plot(EPC_sep[5]['TimeValue'], EPC_sep[5]['PhaseAngle'], marker = 'o', linestyle = '-', label = '3')
    axs[1, 0].set_ylabel('Phase Diff (rads)')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_xlim(left=0)
    axs[1, 0].set_title('A2 Phase vs. Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # subplot 4: bot right
    axs[1, 1].plot(EPC_sep[1]['TimeValue'], EPC_sep[1]['RSSI'], marker = 'o', linestyle = '-', label = '1')
    axs[1, 1].plot(EPC_sep[3]['TimeValue'], EPC_sep[3]['RSSI'], marker = 'o', linestyle = '-', label = '2')
    axs[1, 1].plot(EPC_sep[5]['TimeValue'], EPC_sep[5]['RSSI'], marker = 'o', linestyle = '-', label = '3')
    axs[1, 1].set_ylabel('RSSI (Normalized)')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_xlim(left=0)
    axs[1, 1].set_title('A2 RSSI vs. Time')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.4, wspace=0.4)
    fig.suptitle(title, fontsize=16)
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.tight_layout()

    # dpi                   : resolution
    # bbox_inches = 'tight' : ensures it saves all components of figure
    #fig.savefig(f'Graphs/REV3 3m/{title}.png', dpi=300, bbox_inches='tight')

    print("-------------------- FINISHED 2D PLOTTING --------------------\n")

    # show the figure
    plt.show()

# this function makes a 3D plot with RSSI in the x, EPC in the y, and phase 
# in the z. This is to show similarities between RSSI vs phase graphs dependent
# on iteration, also separated by EPC
def plot_3D(EPC_sep, title):
    x = []
    y = []
    z = []
    label = []
    for i in range(len(EPC_sep)):
        label.append(f'{i + 1} A1')
        label.append(f'{i + 1} A2')
        label.append(f'{i + 2} A3')
        label.append(f'{i + 3} A4')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    for i in range(len(EPC_sep)):
        x.append(EPC_sep[i]['RSSI'])
        y.append(EPC_sep[i]['EPC'])
        z.append(EPC_sep[i]['PhaseAngle'])
        ax.plot(x[i], y[i], z[i], marker = 'o', label = label[i]) #c = c[i] for specific colors

    ax.set_xlabel('Normalized RSSI')
    ax.set_ylabel('EPC')
    ax.set_zlabel('Phase Angle (rads)')
    ax.set_title(title)

    ax.legend()

    print("-------------------- FINISHED 3D PLOTTING --------------------\n")

    plt.show()