# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:28:04 2016

@author: erikjohnson
"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utilityFcns

#%% Import data and store columns
data = pd.read_csv('/Users/erikjohnson/Desktop/penlink/WANA.csv')

#data = data.iloc[:10000]

colmns = data.columns.values.tolist()
#print colmns,'\n'
colmns = [x.upper() for x in colmns]
uniqueItems = ([str(int(x)) for x in set(data.UPC)])
uniqueQtys = ([str(x) for x in set(data.QTY)])
print len(uniqueQtys),len(uniqueItems)
print data[data.QTY!=1.0]
#print colmns,'\n'

#%% Types of data
for colmn in colmns:
    print colmn,type(data.loc[0,colmn])

#%% Check if UPC implies one QTY

upcDict = {}
for item in uniqueItems:
    upcDict[item]={}
    for qty in uniqueQtys:
        upcDict[item][qty]=0
print "Created upc dictionary\n\n Now counting qtys\n\n"

i=0
for index, row in data.iterrows():
#    print type(row['UPC'])
    upcDict[str(row['UPC'])][str(row['QTY'])] += 1
#    if i==10:
#        break
#    i+=1
print "Done counting qtys for upcs \n\n\n Now adding number of nonzero qtys for each upc\n\n"
upcQtys = np.empty(len(uniqueItems))
upcQtys.fill(0)

i=0
for upc in upcDict:
    print upc
    for qty in upcDict[upc]:
        if upcDict[upc][qty]!=0:
            upcQtys[i]+=1
            i+=1
print "Done counting number of nonzero qtys for each upc\n\n"


#%% Troubleshooting

#print utilityFcns.decider(colmns)

#data.ix[(data.PRICE==0) & (data.PROFIT==0) & (data.MOVE!=0)]
#data.ix[(data.SALE=='S')]
#data.ix[(data.SALE=='S') & (data.PRICE==0)]
#data.ix[(data.PROFIT)]
#print data[data.PRICE==0].shape
#print data.ix[data.PRICE==0].shape
#print data[(data.PROFIT==0) & (data.MOVE==0)].shape
#print data.ix[data.PROFIT==0].shape
#print (data.ix[data.PROFIT==0]==data.ix[data.PRICE==0]).all().all()
# (data.PRICE==0) & (data.PROFIT==0) & (data.MOVE==0)
#print data[(data.PRICE!=0) & (data.PROFIT==0)]
#print data[(data.MOVE!=0) & (data.PRICE!=0) & (data.PROFIT!=0)].shape
#print data[(data.MOVE!=0) & (data.PRICE==0) & (data.PROFIT==0)].shape
#print data[(data.MOVE!=0) & (data.PRICE==0) & (data.PROFIT!=0)].shape
#print data[(data.MOVE!=0) & (data.PRICE!=0) & (data.PROFIT==0)].shape
#print data[(data.MOVE==0) & (data.PRICE!=0) & (data.PROFIT!=0)].shape
#print data[(data.MOVE==0) & (data.PRICE==0) & (data.PROFIT==0)].shape
#print data[(data.MOVE==0) & (data.PRICE==0) & (data.PROFIT!=0)].shape
#print data[(data.MOVE==0) & (data.PRICE!=0) & (data.PROFIT==0)].shape
#print data[(data.MOVE!=0) & (data.PRICE!=0) & (data.PROFIT==0)]

