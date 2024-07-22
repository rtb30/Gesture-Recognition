This project is to format, save, and plot data originally exported from a program named ItemTest. 
ItemTest is software for IMPINJ RFID readers to collect backscattered data from RFID tags.

The following list is an explanation of some of the project files & folders:

CSV_formatted : Folder that contains the new formatted data as .csv
Data          : Folder that contains all data. There are multiple reivisions of data which are explained below
    REV2:       0  deg rotation with 3  reps per gesture & 2 tags
    REV3:       90 deg rotation with 3  reps per gesture & 2 tags
    REV4:       0  deg rotation with 20 reps per gesture & 2 tags
    REV5:       0  deg rotation with 5  reps per gesture & 2 tags (to better test REV4)
    REV6:       0  deg rotation with 20 reps per gesture & 4 tags
    REV6 IM:    0  deg rotaiton with 5  reps per gesture & 4 tags (on Ines left arm)
    REV6 RB1:   0  deg rotation with 5  reps per gesture & 4 tags (done at the same time as REV6)
    REV6 RB2:   0  deg rotation with 5  reps per gesture & 4 tags (different day w different tag placement)
    REV6 RB3:   0  deg rotation with 5  reps per gesture & 4 tags (left arm)
    REV6 RB4:   0  deg rotation with 5  reps per gesture & 4 tags (3m away)
    REV6 RB5:   90 deg rotation with 5  reps per gesture & 4 tags
Graphs        : Folder that contains all graphs from processing the exported data.
    REV2: Original
    REV3: 90 deg rotation
HDF5_formatted: Folder that contains the new formatted data as .h5