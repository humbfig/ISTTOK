#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp
from datetime import datetime
import matplotlib.pyplot as plt


class isttok:
    
    host = 'baco.ipfn.ist.utl.pt'
    port = 8888
    client = None

    def __init__(self, channel='', shot_number=0):
        if isttok.client is None:
            isttok.client = SDASClient(isttok.host, isttok.port)
        self.channel = channel
        if shot_number == 0:
            self.shot_number = isttok.last_shot_number(self)
        else:
            self.shot_number = shot_number
        self.tbs = None
        self.tzero = None
        if self.channel != '':
            if isttok.channel_exists(self):
                self.data = isttok.get_data(self)
            else:
                print('')
                print('The requested channel does not exist, at least for the shot number', str(self.shot_number))
                print('')

    def channel_exists(self):
        channel_present = isttok.client.parameterExists(self.channel, '0x0000', self.shot_number)
        return channel_present

    def last_shot_number(self):
        last_shot = int(isttok.client.searchMaxEventNumber('0x0000'))
        return last_shot

    def get_data(self):
        dataStruct = isttok.client.getData(self.channel, '0x0000', self.shot_number)[0]
        data = dataStruct.getData()
        tStart = dataStruct.getTStart().getTimeInMicros()
        tEnd = dataStruct.getTEnd().getTimeInMicros()
        len_d = len(data)
        self.tbs = (tEnd - tStart) / len_d
        events = dataStruct.get('events')[0]
        tevent = TimeStamp(tstamp=events.get('tstamp')).getTimeInMicros()
        self.tzero = datetime.fromtimestamp(tevent / 1e6, tz=None)
        delay = tStart - tevent
        timeVector = np.linspace(delay, delay + self.tbs * (len_d - 1), len_d)
        return np.array([timeVector, data]).T

    def save_data(self, name_string='', ti=None, tf=None):
        if name_string == '':
            filename = str(self.shot_number) + '.' + self.channel + '.csv'
        else:
            filename = str(self.shot_number) + '.' + name_string + '.csv'
        if ti != None:
            start_index = np.abs(self.data[:, 0] / 1e3 - ti).argmin()
        else:
            start_index = 0
        if tf != None:
            end_index = np.abs(self.data[:, 0] / 1e3 - tf).argmin()
        else:
            end_index = -1
        segmented_data = self.data[start_index:end_index, :]
        np.savetxt(filename, segmented_data, delimiter=",")
        # filename = str(self.shotN) + '.' + self.channel + '.xls'
        # print(filename)
        # pd.DataFrame(self.data).to_excel(filename, header = ['time', self.channel], index = False)

    def plot_data(self):
        plt.plot(self.data[:, 0] / 1e3, self.data[:, 1])
        plt.xlabel('time (ms)')
        plt.ylabel('')
        plt.title(self.channel)
        plt.show()

    def find_channels_uniqueID(self, search_string=''):
        channels_found = isttok.client.searchParametersByUniqueID(search_string)
        uniqueID_channels = np.array([])
        name_channels = np.array([])
        for p in channels_found:
            uniqueID_channels = np.append(uniqueID_channels, p['descriptorUID']['uniqueID'])
            name_channels = np.append(name_channels, p['descriptorUID']['name'])
        print('')
        print(len(uniqueID_channels), 'entries found [uniqueID, name]')
        print('')
        return np.array([uniqueID_channels, name_channels]).T

    def find_channels_name(self, search_string=''):
        channels_found = isttok.client.searchParametersByName(search_string)
        name_channels = np.array([])
        uniqueID_channels = np.array([])
        for p in channels_found:
            name_channels = np.append(name_channels, p['descriptorUID']['name'])
            uniqueID_channels = np.append(uniqueID_channels, p['descriptorUID']['uniqueID'])
        print('')
        print(len(uniqueID_channels), 'entries found [name, uniqueID]')
        print('')
        return np.array([name_channels, uniqueID_channels]).T

    def find_channels_shot(self, shot_number=0):
        if shot_number == 0:
            shot_number = self.shot_number
        uniqueID_channels = isttok.client.searchDataByEvent('0x0000', shot_number)
        print('')
        print(len(uniqueID_channels), 'entries found [uniqueID]')
        print('')
        return uniqueID_channels
