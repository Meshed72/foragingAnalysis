# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:30:07 2024

@author: matan
"""

from os import listdir
import pandas as pd

PATH = 'C:/Users/matan/Documents/Matan/Foraging/DATA/Preliminary anlysis/Initial analysis 4_24/by parts/'

data_files = listdir(PATH)
dfs = []
for i in range(0, len(data_files)):
    dfs.append(pd.read_csv(PATH + data_files[i]))
uniuned = pd.concat(dfs)
uniuned.to_csv(PATH + 'uniuned' + '.csv', mode='w')

