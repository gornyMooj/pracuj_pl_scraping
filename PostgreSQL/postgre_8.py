'''
merges csv files
'''
import pandas as pd
from os import listdir
from os.path import isfile, join
import os

mypath = os.path.abspath(os.getcwd())

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


csvs = []


for file in onlyfiles:
        if file[-4:] == '.csv':
               csvs.append(file) 



df = pd.concat(
    map(pd.read_csv, csvs), ignore_index=True)


df = df.drop_duplicates()


df.to_csv('merged.csv', index=False)






