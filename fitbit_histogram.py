#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 2023

@author: khosravip2
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
from datetime import datetime, timedelta

path = ("/Users/khosravip2/OneDrive - National Institutes of Health/ParmisK/PROJECTS/fitbit_hist")

# load df with day counts each subject wear fitbit (already had this df ready when we were cleaning the data)
fitday = pd.read_csv(os.pathjoin(path, "fitbit_daycount.csv"), sep = ",")

# make a histogram
fitday.plot.hist(edgecolor = 'black', bins=range(80))
plt.xticks(ticks= np.arange(0,85,5))
fitday.hist(edgecolor = 'black', bins=range(80), grid=False,color='turquoise')
plt.xticks(ticks= np.arange(0,80,5))
plt.xlabel("number of days")
plt.ylabel("frequency")


# load df with subject and date of fitbit wear (already had this df ready when we were cleaning the data)

fitdate = pd.read_csv(os.pathjoin(path, "fitbit_dates.csv"), sep = ",")

fitdate = fitdate.set_index('SUBJECT')
# format date
fitdate['date'] = pd.to_datetime(fitdate['date'],unit='ns', errors='coerce')
fitdate.dtypes
# sort date
fitdate = fitdate.sort_values(['SUBJECT', 'date'], ascending=(True, True))

# find consecutive dates
datediff = fitdate.groupby('SUBJECT').date.diff().dt.days.ne(1).cumsum()
datediff_a = fitdate.groupby(['SUBJECT', s]).size().reset_index(level=1, drop=True)
datediff_b = pd.DataFrame(datediff_a)

# rename the new column
datediff_b = datediff_b.rename(columns={0: "grp_dt"})

count = len(datediff_b[datediff_b['grp_dt']> 7])

def dt (series):
    if series < 7: # for less than 7 consecutive days
        return 0   # recod to zero
    elif series >= 7: # for 7 or more consecutive days
        return 1    # recode to 1
        
datediff_b = datediff_b.reset_index()
datediff_b['flag'] = datediff_b['grp_dt'].apply(dt)

count = len(datediff_b[datediff_b['flag'] ==1])
filter_dt = datediff_b.loc[(c['flag']==1)] # filter subjects with 7 and more consecutive days of data
subjcount = filter_dt.nunique(axis=1) # count unique subjects with 7 and more consecutive days of data
filter_dt.nunique()

#fitdate_c = filter_dt.nunique('SUBJECT').filter(lambda g: g.flag==1) # DO NOT USE
#fitdate_c = filter_dt.groupby('SUBJECT').filter(lambda g: g.flag.nunique()==1) # DO NOT USE

# make a histogram for those with data from 7 or more consecutive days
filter_dt.hist('grp_dt', edgecolor = 'black', bins=range(7,36), grid=False,color='turquoise')
plt.xticks(ticks= np.arange(7,36,3))
plt.xlabel("number of consecutive days")
plt.ylabel("frequency")

