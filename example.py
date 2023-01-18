
from isttok import isttok
import matplotlib.pyplot as plt


shot_number = 0
# 0 means last shot in database

# These are the channels uniqueIDs.
rfa_channel = 'PCIE_ATCA_ADC_16.BOARD_3.CHANNEL_023'
sweep_channel = 'PCIE_ATCA_ADC_16.BOARD_3.CHANNEL_018'

# This will create instances of the isttok object that contains all data from the channels.
rfa = isttok(channel=rfa_channel, shot_number=shot_number)
sweep = isttok(channel=sweep_channel, shot_number=shot_number)

#This will plot the data in a zoomable window.
rfa.plot_data()

# This will save the data in a ascii file
rfa.save_data('rfa', ti=32, tf=46)
# file name will start by shot number followed by string "rfa" with extension "csv".
# it will consist of two columns [time, data] starting at "ti" and ending at "tf" (in ms).
# It is possible to call save_data() without any arguments: "rfa.save_data()". In that case the file will
# contain all the data and its name will be "shot number" followed by the channel uniqueID.

sweep.plot_data()
sweep.save_data('sweep', ti=32, tf=46)

# In case there is the need to find unique ID's of any other channels (Plasma current, for example), one
# can search the database for "names" using:
channels_found = rfa.find_channels_name('plasma')
print(channels_found)
pause = input('Press Enter to continue')
# or
channels_found = sweep.find_channels_name('plasma')

pause = input('Press Enter to continue')

# or, even better, creating an empty object (no data):
instance = isttok()
channels_found = instance.find_channels_name('plasma')

pause = input('Press Enter to continue')

#This will find all channels that contain the word "plasma" in the name and list the findings
# in the format [name, uniqueID]. One of them will be
# ['MagneticProbesPlasmaCurrent', 'MARTE_NODE_IVO3.DataCollection.Channel_085']
# Now, one can get the data for the plasma current:
IP_channel = 'MARTE_NODE_IVO3.DataCollection.Channel_085'
IP = isttok(channel=IP_channel, shot_number=shot_number)
#plot it and save it in the same way:
IP.plot_data()
IP.save_data('IP', ti=500)

# To search for unique ID's instead of names, the function to use should be:
channels_found = instance.find_channels_uniqueID('string to search for')
# It will list the findings in [uniqueID, name] format.

pause = input('Press Enter to continue')

# To search for the channels that are saved in the database for a specific shot:
channels_found = instance.find_channels_shot(49738)
# For the last shot one can use "instances.find_channels_shot()" or "(0)"

pause = input('Press Enter to continue')

# To plot both channels
fig = plt.figure()
gs = fig.add_gridspec(2, hspace=0)
axs = gs.subplots(sharex=True)
fig.suptitle('rfa')
axs[0].plot(sweep.data[:, 0] / 1e3, sweep.data[:, 1])
axs[0].set_ylabel('sweep')
axs[1].plot(rfa.data[:, 0] / 1e3, rfa.data[:, 1])
axs[1].set_xlabel('time (ms)')
axs[1].set_ylabel('rfa')
for ax in axs:
    ax.label_outer()
plt.show()
