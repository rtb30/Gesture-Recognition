# import
import pandas as pd
# this gets rid of some random warning when separating data into EPC1 & EPC2
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# this function uses 2D plots to show similarities between phase vs time and 
# RSSI vs time graphs dependent on iteration, also separated by EPC
def plot_2D(title, EPC_sep, EPC_count):
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

def plot_2D_new(title, EPC_sep):
    # EPC values assumed to be 1, 2, 3, and 4
    epcs = [1, 2, 3, 4]
    
    # Set up the figure and axes for 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()  # Flatten to easily iterate over them
    
    # Colors for plotting
    colors = plt.cm.get_cmap('tab10', len(EPC_sep))

    for i, epc in enumerate(epcs):
        ax = axes[i]
        ax.set_title(f'EPC {epc}')
        ax.set_xlabel('RSSI')
        ax.set_ylabel('PhaseAngle')
        
        # Plot each dataframe for the current EPC
        for idx, df in enumerate(EPC_sep):
            # Filter dataframe for the current EPC
            epc_data = df[df['EPC'] == epc]
            if not epc_data.empty:
                ax.plot(
                    epc_data['RSSI'], epc_data['PhaseAngle'],
                    marker='o', linestyle='-', color=colors(idx),
                    #label=f'DataFrame {idx}'
                )

                # Highlight the starting point
                ax.plot(
                    epc_data['RSSI'].iloc[0], epc_data['PhaseAngle'].iloc[0],
                    marker='s', color=colors(idx), markersize=10
                )
                
                # Highlight the ending point
                ax.plot(
                    epc_data['RSSI'].iloc[-1], epc_data['PhaseAngle'].iloc[-1],
                    marker='^', color=colors(idx), markersize=10
                )
        
        # Add legend if any data was plotted
        if ax.has_data():
            ax.legend()
    
    plt.tight_layout()
    plt.show()

def plot_gesture_data_interactive(df_list):
    # EPC values assumed to be 1, 2, 3, and 4
    epcs = [1, 2, 3, 4]
    
    # Colors for plotting
    colors = plt.cm.get_cmap('tab10', len(df_list))

    fig, ax = plt.subplots(figsize=(8, 6))
    
    for epc in epcs:
        # Create a new figure for each EPC
        ax.clear()
        ax.set_title(f'EPC {epc}')
        ax.set_xlabel('RSSI')
        ax.set_ylabel('PhaseAngle')

        # Plot each dataframe for the current EPC one by one
        for idx, df in enumerate(df_list):
            # Filter dataframe for the current EPC
            epc_data = df[df['EPC'] == epc]
            if not epc_data.empty:
                ax.plot(
                    epc_data['RSSI'], epc_data['PhaseAngle'],
                    marker='o', linestyle='-', color=colors(idx),
                    label=f'DataFrame {idx}'
                )

                # Highlight the starting point
                ax.plot(
                    epc_data['RSSI'].iloc[0], epc_data['PhaseAngle'].iloc[0],
                    marker='s', color=colors(idx), markersize=10, label=f'Start (DF {idx})'
                )
                
                # Highlight the ending point
                ax.plot(
                    epc_data['RSSI'].iloc[-1], epc_data['PhaseAngle'].iloc[-1],
                    marker='^', color=colors(idx), markersize=10, label=f'End (DF {idx})'
                )

                plt.draw()  # Update the plot
                plt.pause(0.5)  # Pause for a short moment
                input(f'Press Enter to continue to the next curve for EPC {epc}...')
        
        # Display legend if any data was plotted
        if ax.has_data():
            ax.legend()

        input(f'Press Enter to proceed to the next EPC plot...')

    plt.close(fig)

# this function makes a 3D plot with RSSI in the x, EPC in the y, and phase 
# in the z. This is to show similarities between RSSI vs phase graphs dependent
# on iteration, also separated by EPC
def plot_3D(EPC_sep):
    x = []
    y = []
    z = []
    count = 0
    k = 0

    fig = plt.figure(figsize=(8, 6))
    
    ax = fig.add_subplot(111, projection = '3d')

    # Colors for plotting
    colors = ['r', 'g', 'b']
    #colors = plt.cm.get_cmap('tab10', 2)

    for i in range(len(EPC_sep)):
        if EPC_sep[i].empty == True:
            count += 1
            continue
        if(EPC_sep[i]['RSSI'].iloc[0] == 0):
            count += 1
            continue

        x.append(EPC_sep[i]['RSSI'])
        y.append(EPC_sep[i]['EPC'])
        z.append(EPC_sep[i]['PhaseAngle'])
        ax.plot(x[-1], y[-1], z[-1], marker = 'o', color = colors[k]) #c = c[i] for specific colors
        count += 1

        if(count == 8):
            k += 1
            count = 0

    ax.set_xlabel('Normalized RSSI')
    ax.set_ylabel('EPC')
    ax.set_zlabel('Phase Angle (rads)')

    # Adjust the margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    print("-------------------- FINISHED 3D PLOTTING --------------------\n")

    plt.show()