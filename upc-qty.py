# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:04:04 2016

@author: erikjohnson
"""

#%% DESCRIPTION
# This is a script that walks the through the W*.csv files in the Dominick's
# sales database and finds UPCs which have QTY=1 and QTY!=1. Stores number 
# of both in a dataframe along with UPCs for which QTY!=1

#%% IMPORTS
import pandas as pd
import numpy as np
import os
import sys

#%% MAIN

walk_dir = '/Users/erikjohnson/Dropbox/Dominicks_Database/Category_Files/'
walk_dir = os.path.abspath(walk_dir)
df = pd.DataFrame(columns=('W*.csv File', '# of UPCs having QTY=1',
                           '# of UPCs having QTY>1','UPCs with QTY>1'))
list_file_path = os.path.join('/Users/erikjohnson/Desktop/recursiveFileTest/','list.txt')

i=0
for root, subdirs, files in os.walk(walk_dir):
#    if i>=4:
#        break
    for filename in files:
        if filename[-3:]=='csv' and filename[0]=='W':
            print i,filename

            wfile_df =  pd.read_csv(os.path.join(root,filename))
            wfile_df = wfile_df[['UPC','QTY']]
            wfile_df.drop_duplicates(inplace=True)

            group = wfile_df.groupby('UPC')
            agg = group.agg('count')

            nonone = agg[agg['QTY']!=1].shape[0]
            one = agg[agg['QTY']==1].shape[0]
            upcs = agg[agg['QTY']!=1].index.values
            upcs = list(upcs)
#            upcs = ",".join(map(str,upcs))
            
            df.loc[i] = [filename, one, nonone, upcs]
            i += 1

df.to_csv('/Users/erikjohnson/Desktop/penlink/UPC-QTY.csv',index=False)