
from dataISTTOK import ISTTOK
import matplotlib.pyplot as plt
import numpy as np

shot_number = 49665
mirnov_Polarity = [-1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1]
mirnov_channels = ['MARTE_NODE_IVO3.DataCollection.Channel_129',
    'MARTE_NODE_IVO3.DataCollection.Channel_130',
    'MARTE_NODE_IVO3.DataCollection.Channel_131',
    'MARTE_NODE_IVO3.DataCollection.Channel_132',
    'MARTE_NODE_IVO3.DataCollection.Channel_133',
    'MARTE_NODE_IVO3.DataCollection.Channel_134',
    'MARTE_NODE_IVO3.DataCollection.Channel_135',
    'MARTE_NODE_IVO3.DataCollection.Channel_136',
    'MARTE_NODE_IVO3.DataCollection.Channel_137',
    'MARTE_NODE_IVO3.DataCollection.Channel_138',
    'MARTE_NODE_IVO3.DataCollection.Channel_139',
    'MARTE_NODE_IVO3.DataCollection.Channel_140']


def compute_DC(channel):
    a, b = np.polyfit(channel.data[:, 0] / 1e3, channel.data[:, 1], 1)
    return a


mirn = []
for channel in mirnov_channels:
    mirn.append(ISTTOK(channel=channel, shot_number=shot_number))

DCs = []
for channel in mirn:
    DCs.append(compute_DC(channel))

fig = plt.figure()
gs = fig.add_gridspec(12, hspace=0)
axs = gs.subplots(sharex=True)
fig.suptitle('Mirnov coils integrated')
for channel in mirn:
    axs[mirn.index(channel)].plot(channel.data[:, 0] / 1e3, channel.data[:, 1])
    axs[mirn.index(channel)].plot(channel.data[:, 0] / 1e3, DCs[mirn.index(channel)] * channel.data[:, 0] / 1e3, 'tab:orange')
for ax in axs:
    ax.label_outer()
plt.show()

print('')
print(DCs)
