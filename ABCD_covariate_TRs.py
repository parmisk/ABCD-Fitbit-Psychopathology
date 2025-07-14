#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 23:00:42 2022

@author: khosravip2
"""



import pandas as pd
import numpy as np
import os
import scipy
from matplotlib import pyplot as plt
from scipy.stats import norm
import seaborn as sns
import glob


path_to_data = '/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/'

df = pd.DataFrame()

print(len([x for x in glob.iglob(str('%s*.txt*'%path_to_data))]))

counter = 0
for i in glob.iglob(str('%s*.txt*'%path_to_data)) :
    counter = counter + 1
    if counter % 1000 == 0:
        print(counter)
    df = pd.concat([pd.read_csv(i)], sep='\t')


df.to_csv('/gpfs/gsfs6/users/khosravip2/ABCDcp/data/abcd_lpds01.csv', index = False, header = True)

# Read csv

demo = pd.read_csv(path.join(path_to_data, 'abcd_lpds01.csv'))

#%%
demo = pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/rawdata/abcd_lpds01.txt", sep = '\t')
demo_rstidx = demo.reset_index()
demo_rstidx.columns
demo2.columns
# dropping variable description row
demo2 = demo.drop(demo.index[0], axis = 0)
# count number of unique subjects
demo2["subjectkey"].nunique() # N = 11876
# get count of each event type
eventcnt_demo = demo2.groupby("eventname")["subjectkey"].nunique() # 3-yr N = 6251, 2-yr N = 10414, 1-yr N = 11225, baseline N = 11876

# set index
idxdemo = demo2.set_index(['subjectkey', 'eventname' ], append = False)
# filter by eventname
demo2 = idxdemo.filter(like = '2_year_follow_up_y_arm_1', axis = 0)

demofilt = demo2.filter(items=['interview_age','sex','demo_ed_v2_l','demo_gender_id_v2_l','demo_nat_lang_l','demo_relig_v2_l','demo_comb_income_v2_l'])


# change all 888 row to 0

d = demofilt.isin(['M', 'F']).any(axis = 0)
D = demofilt.replace('M', 1)
D = D.replace('F', 2)

d2 = demofilt.isin(['NR', 'O']).any(axis = 0) # these responses are within the selected subjects


# save resting-state as csv file
D.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/demo_test.csv", index = True, header = True)


#%%

# Resting state covariates

rs_goraseg= pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/mrirscor02.txt", sep = "\t")

# dropping variable description row
rs_goraseg = rs_goraseg.drop(rs_goraseg.index[0], axis = 0)
# count number of unique subjects
rs_goraseg["subjectkey"].nunique() # N = 11614
# get count of each event type
eventcnt = rs_goraseg.groupby("eventname")["subjectkey"].nunique() # 2-yr N = 7675, 1-yr = 11314
# set index
idxrs_goraseg = rs_goraseg.set_index(['subjectkey', 'eventname'], append = False)
# filter by eventname
rs_goraseg2yr = idxrs_goraseg.filter(like = '2_year_follow_up_y_arm_1', axis = 0)


# filter by motion correction columns
rs_goraseg_covar = rs_goraseg2yr.filter(regex = '^rsfmri_cor_ngd_scs', axis = 1)
# drop the visit ID column
rs_goraseg_covar2 = rs_goraseg_covar.drop(['rsfmri_cor_ngd_scs_visitid'], axis =1)
# save resting-state as csv file
rs_goraseg_covar2.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/rs_gor+aseg_covariates.csv", index = True, header = True)


rs_goraseg_covar2.dtypes
# to change variable type to float/numeric
# André said we can use stype as well which is better
rs_goraseg_covar2["rsfmri_cor_ngd_scs_nvols"]= rs_goraseg_covar2["rsfmri_cor_ngd_scs_nvols"].map(lambda x:float(x))
rs_goraseg_covar2.dtypes

# get some general descripts 
a = rs_goraseg_covar2.describe(include = 'all')

# make a histogram to check data distribution 
rs_goraseg_covar2.hist(column='rsfmri_cor_ngd_scs_numtrs')
rs_goraseg_covar2.hist(column='rsfmri_cor_ngd_scs_nvols')
# set a variable cut off and make a histogram 
above_900 = rs_goraseg_covar2[rs_goraseg_covar2["rsfmri_cor_ngd_scs_numtrs"] > 900]
above_900.hist(column='rsfmri_cor_ngd_scs_numtrs')

# separate columns with left/right ventral diencephalon
rs_goraseg_glob = rs_goraseg2yr.filter(regex= '(_vtdclh$|_vtdcrh$)', axis = 1)
# save resting-state as csv file
rs_goraseg_glob.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/rs_golb.csv", index = True, header = True)


# read datafile
rsgor = pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/abcd_betnet02.txt", sep = "\t")

# dropping variable description row
rsgor = rsgor.drop(rsgor.index[0], axis = 0)
# count number of unique subjects
rsgor["subjectkey"].nunique() # N = 11614
# get count of each event type
eventcnt = rsgor.groupby("eventname")["subjectkey"].nunique() # 2-yr N = 7675, 1-yr = 11314
# set index
idxrsgor = rsgor.set_index(['subjectkey', 'eventname'], append = False)
# filter by eventname
rsgor2yr = idxrsgor.filter(like = '2_year_follow_up_y_arm_1', axis = 0)

# filter by motion correction columns
rs_gor_covar = rsgor2yr.filter(regex = '^rsfmri_c_ngd', axis = 1)
# drop the visit ID column
rs_gor_covar2 = rs_gor_covar.drop(['rsfmri_c_ngd_visitid'], axis =1)
# save as csv
rs_gor_covar2.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/rs_gor_covariates.csv", index = True, header = True)

# check data type
rs_gor_covar2.dtypes
rs_gor_covar2.dtypes
# to change variable type to float/numeric
# André said we can use stype as well which is better
rs_gor_covar2["rsfrmi_c_ngd_numtrs"]= rs_gor_covar2["rsfmri_c_ngd_numtrs"].map(lambda x:float(x))
rs_gor_covar2.dtypes

# get some general descripts 
a = rs_gor_covar2.describe(include = 'all')

rs_gor_covar2.hist(column='rsfrmi_c_ngd_numtrs')

# set a variable cut off and make a histogram 
above_1000 = rs_gor_covar2[rs_gor_covar2["rsfrmi_c_ngd_numtrs"] > 1000]

a = above_1000.describe(include = 'all')
ax_1000 = above_1000.hist(column='rsfrmi_c_ngd_numtrs', bins=30, grid=True, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)


#%%

# Mid task

# read datafile

mid1 = pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/midaparc03.txt", sep = "\t")
mid2 = pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/midaparcp203.txt", sep = "\t")

# dropping variable description row
mid1= mid1.drop(mid1.index[0], axis = 0)
# count number of unique subjects
mid1["subjectkey"].nunique() # N = 10982
# get count of each event type
eventcnt = mid1.groupby("eventname")["subjectkey"].nunique() # 2-yr N = 7675, 1-yr = 11314
# set index
idxmid1 = mid1.set_index(['subjectkey', 'eventname'], append = False)
# filter by eventname
mid2yr = idxmid1.filter(like = '2_year_follow_up_y_arm_1', axis = 0)

# filter by motion correction columns
mid1_covar = mid2yr.filter(regex = '^tfmri_mid_all_b', axis = 1)
# drop the visit ID column
mid1_covar2 = mid1_covar.drop(['tfmri_mid_all_b_visitid'], axis =1)
# save as csv
mid1_covar2.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/mid_covariates.csv", index = True, header = True)

#check data type
mid1_covar2.dtypes
# to change variable type to float/numeric
# André said we can use stype as well which is better
mid1_covar2["tfmri_mid_all_b_numtrs"]= mid1_covar2["tfmri_mid_all_b_numtrs"].map(lambda x:float(x))
mid1_covar2["tfmri_mid_all_b_nvols"]= mid1_covar2["tfmri_mid_all_b_nvols"].map(lambda x:float(x))

# compare the two variables to see if they are the same or different
aa = mid1_covar2["tfmri_mid_all_b_numtrs"].values== mid1_covar2["tfmri_mid_all_b_nvols"].values
mid1_covar2.dtypes

# get some general descripts 
a = mid1_covar2.describe(include = 'all')

# make a histogram to check data distribution 
mid1_covar2.hist(column='tfmri_mid_all_b_numtrs')
mid1_covar2.hist(column='tfmri_mid_all_b_nvols')
mid1_covar2()
# set a variable cut off and make a histogram 
above_790 = mid1_covar2[mid1_covar2["tfmri_mid_all_b_numtrs"] > 790]
a = above_790.describe(include = 'all')
ax_790 = above_790.hist(column='tfmri_mid_all_b_numtrs', bins=30, grid=True, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)


# sst task

# read datafile

sst = pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/mrisst02.txt", sep = "\t")

# dropping variable description row
sst= sst.drop(sst.index[0], axis = 0)
# count number of unique subjects
sst["subjectkey"].nunique() # N = 10898
# get count of each event type
eventcnt = sst.groupby("eventname")["subjectkey"].nunique() # 2-yr N = 7675, 1-yr = 11314
# set index
idxsst = sst.set_index(['subjectkey', 'eventname'], append = False)
# filter by eventname
sst2yr = idxsst.filter(like = '2_year_follow_up_y_arm_1', axis = 0)

# filter by motion correction columns
sst_covar = sst2yr.filter(regex = '^tfmri_sa_beta', axis = 1)
# drop the visit ID column
sst_covar2 = sst_covar.drop(['tfmri_sa_beta_visitid'], axis =1)
# save as csv
sst_covar2.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/sst_covariates.csv", index = True, header = True)


# check data type 
sst_covar2.dtypes
# to change variable type to float/numeric
# André said we can use stype as well which is better
sst_covar2["tfmri_sa_beta_numtrs"]= sst_covar2["tfmri_sa_beta_numtrs"].map(lambda x:float(x))
sst_covar2.dtypes

# compare the two variables to see if they are the same or different
aa = sst_covar2["tfmri_sa_beta_numtrs"].values== sst_covar2["tfmri_sa_beta_nvols"].values

# get some general descripts 
a = sst_covar2.describe(include = 'all')

sst_covar2.hist(column='tfmri_sa_beta_numtrs')

ax = sst_covar2.hist(column='tfmri_sa_beta_numtrs', bins=30, grid=True, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)

# set a variable cut off and make a histogram 
above_850 = sst_covar2[sst_covar2["tfmri_sa_beta_numtrs"] > 850]
a = above_850.describe(include = 'all')

above_882 = sst_covar2[sst_covar2["tfmri_sa_beta_numtrs"] >= 882]
a = above_882.describe(include = 'all')

ax_882 = above_882.hist(column='tfmri_sa_beta_numtrs', bins=30, grid=True, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)


# Nback task 

# read datafile 

nback =  pd.read_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/origdata/imaging/nback_bwroi02.txt", sep = "\t")

# dropping variable description row
nback= nback.drop(nback.index[0], axis = 0)
# count number of unique subjects
nback["subjectkey"].nunique() # N = 10830
# get count of each event type
eventcnt = nback.groupby("eventname")["subjectkey"].nunique() # 2-yr N = 7675, 1-yr = 11314
# set index
idxnback = nback.set_index(['subjectkey', 'eventname'], append = False)
# filter by eventname
nback2yr = idxnback.filter(like = '2_year_follow_up_y_arm_1', axis = 0)
nback2yr.columns
# filter by motion correction columns
nback_covar = nback2yr.filter(regex = '^tfmri_nback_all_beta', axis = 1)
# drop the visit ID column
nback_covar2 = nback_covar.drop(['tfmri_nback_all_beta_visitid'], axis =1)

# save as csv
nback_covar2.to_csv("/gpfs/gsfs6/users/khosravip2/ABCDcp/data/nback_covariates.csv", index = True, header = True)

# check data type
nback_covar2.dtypes
# to change variable type to float/numeric
# André said we can use stype as well which is better
nback_covar2["tfmri_nback_all_beta_numtrs"]= nback_covar2["tfmri_nback_all_beta_numtrs"].map(lambda x:float(x))
# get some general descripts 
a = nback_covar2.describe(include = 'all')
aa = nback_covar2["tfmri_nback_all_beta_numtrs"].mean()





