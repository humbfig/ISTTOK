#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 14:40:38 2022

@author: humbfig
"""

import numpy as np
from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp
from datetime import datetime
import matplotlib.pyplot as plt


class isttok:
    
    host = 'baco.ipfn.ist.utl.pt'
    port = 8888
    client = None
    
    def __init__(self, channel='', shot_number=None):
        self.channel = channel
        self.shot_number = shot_number
        if isttok.client is None:
            isttok.client = SDASClient(isttok.host, isttok.port)
        self.tbs = None
        self.tzero = None
        self.data = isttok.get_data(self)

    def last_shot_number(self):
        last_shot = int(isttok.client.searchMaxEventNumber('0x0000'))
        return last_shot

    def get_data(self):
        if self.shot_number is (None or 0):
            self.shot_number = isttok.LastShotNumber(self)
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

    def save_data(self):
        filename = str(self.shotN) + '.' + self.channel + '.csv'
        np.savetxt(filename, self.data, delimiter=",")
        # filename = str(self.shotN) + '.' + self.channel + '.xls'
        # print(filename)
        # pd.DataFrame(self.data).to_excel(filename, header = ['time', self.channel], index = False)

    def plot_data(self):
        plt.plot(self.data[:, 0] / 1e3, self.data[:, 1])
        plt.xlabel('time (ms)')
        plt.ylabel('')
        plt.show()
