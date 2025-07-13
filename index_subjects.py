#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:34:32 2023

@author: khosravip2
"""


import pandas as pd
import os
import numpy as np

# indexing subjects to include those that have all data modalities

ROOTDIR='/data/NIMH_scratch/khosravip2/ABCD-CCA'
netmatdir = os.path.join(ROOTDIR,'derivatives','netmats')
mrtrix = os.path.join(ROOTDIR,'derivatives','mrtrix')
dti = os.path.join(ROOTDIR, 'derivatives', 'd')
subject_list = []

################
def get_jasonfile (file_path):
    with open(file_path, 'r') as file_path:
        j = json.load(file_path)
    return j

################

for filename in os.listdir(netmatdir):
    if filename.startswith('sub-'):
        subject_list.append(filename)

output = pd.DataFrame(columns=['SUBJECT_KEY','netmats'])

for s in subject_list:
        countnetmat = 0
        for rootFILE, folders, files in os.walk(os.path.join(netmatdir,s)) :
        #for folders, files in os.path.join(netmatdir,s) :
         v
            for file in files :
                #for "func" in rootFILE:
                    if "csv" in file :
                        countnetmat = countnetmat + 1
        print("this subject named {} has {} netmat".format(s,countnetmat))
        
        SUBJECT_KEY = s.split('sub-')[1]
        row = {'SUBJECT_KEY':SUBJECT_KEY, 'netmats':countnetmat}
        
        # Append the new row to the DataFrame
        output = pd.concat([output, pd.DataFrame([row])], ignore_index=True)
    
        output.to_csv(os.path.join(ROOTDIR,'list', 'netmats_list.csv'))
        print('done')  
        
output["SUBJECT_KEY"].nunique()# N = 4049
unique_values = set(subject_list)
count_unique = len(unique_values) # N = 4049






subject_list = []

################

for filename in os.listdir(mrtrix):
    if filename.startswith('sub-'):
        subject_list.append(filename)

output = pd.DataFrame(columns=['SUBJECT_KEY','mrtrix'])

for s in subject_list:
        countmrtrix = 0
        for rootFILE, folders, files in os.walk(os.path.join(mrtrix,s)) :
        #for folders, files in os.path.join(netmatdir,s) :
         
            for file in files :
                #for "dwi" in rootFILE:
                  if "tck" in file :
                      countmrtrix = countmrtrix + 1
        print("this subject named {} has {} mrtrix".format(s,countmrtrix))
        
        SUBJECT_KEY = s.split('sub-')[1]
        row = {'SUBJECT_KEY':SUBJECT_KEY, 'mrtrix':countmrtrix}
        
        # Append the new row to the DataFrame
        output = pd.concat([output, pd.DataFrame([row])], ignore_index=True)
    
        output.to_csv(os.path.join(ROOTDIR,'list', 'mrtrix_list.csv'))
        print('done')  
        
output["SUBJECT_KEY"].nunique()# N = 4449
unique_values = set(subject_list)
count_unique = len(unique_values) # N = 4449



# load the netmats subject list that we created above 
netmatslist = pd.read_csv(os.path.join(ROOTDIR, 'list', 'netmats_list.csv'), index_col=0)
fitbit = pd.read_csv(os.path.join(ROOTDIR, 'group', 'fitbit.csv'))
area = pd.read_csv(os.path.join(ROOTDIR, 'group', 'area.csv'))
thickness = pd.read_csv(os.path.join(ROOTDIR, 'group', 'thickness.csv'))
clinic = pd.read_csv(os.path.join(ROOTDIR, 'derivatives', 'clinic.csv'))
#clinic = pd.read_csv(os.path.join(ROOTDIR, 'group', 'clinical.csv'))
demo = pd.read_csv(os.path.join(ROOTDIR, 'group', 'demographic.csv'))
mrtrix = pd.read_csv(os.path.join(ROOTDIR, 'list', 'mrtrix_list.csv'), index_col = 0)
famid = pd.read_csv(os.path.join(ROOTDIR, 'group', 'familyID.csv'))
sites = pd.read_csv(os.path.join(ROOTDIR, 'group', 'sites.csv'))
scanners = pd.read_csv(os.path.join(ROOTDIR, 'group', 'scanners.csv'))


netmatslist.dtypes
netmatslist= netmatslist.rename(columns={ 'SUBJECT_KEY':'subjectkey'})
fitbit = fitbit.rename(columns={'src_subject_id':'subjectkey'})
fitbit['subjectkey'] = fitbit['subjectkey'].str.replace('_', '')
fitbit.dtypes
area = area.rename(columns={'SubjectID':'subjectkey'})
thickness = thickness.rename(columns={'SubjectID': 'subjectkey'})
mrtrix = mrtrix.rename(columns={'SUBJECT_KEY':'subjectkey'})

# clinic= clinic.drop(columns='Unnamed: 0')

clinic['subjectkey'].nunique()

clinic['subjectkey'] = clinic['subjectkey'].str.replace('_', '')
netmatslist['subjectkey'] = netmatslist['subjectkey'].str.replace('sub-','')
mrtrix['subjectkey'] = mrtrix['subjectkey'].str.replace('sub-','')
area['subjectkey']= area['subjectkey'].str.replace('sub-','')
thickness['subjectkey']= thickness['subjectkey'].str.replace('sub-','')
famid['subjectkey']=famid['subjectkey'].str.replace('_', '')
demo['subjectkey']=demo['subjectkey'].str.replace('_','')
sites['subjectkey']=sites['subjectkey'].str.replace('_', '')
scanners['subjectkey']=scanners['subjectkey'].str.replace('_', '')


fitbit.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'fitbit.csv'))
# f = pd.read_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'fitbit.csv')) # testing
area.to_csv(os.path.join(ROOTDIR, 'derivatives','match_subjectID_column', 'area.csv'))
thickness.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'thickness.csv'))
clinic.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'clinic.csv'))
demo.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'demographic.csv'))
famid.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'familyID.csv'))
sites.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'sites.csv'))
scanners.to_csv(os.path.join(ROOTDIR, 'derivatives', 'match_subjectID_column', 'scanners.csv'))



# apply the function to the subject column using apply()
#fitbit['SUBJECT_KEY'] = fitbit['SUBJECT_KEY'].apply(add_prefix)



netmatslist = netmatslist.set_index(['subjectkey'])
fitbit = fitbit.set_index(['subjectkey'])


df_inner = (
    netmatslist.merge(fitbit, on="subjectkey", how="inner")
            .merge(mrtrix, on="subjectkey", how="inner")
            .merge(area, on="subjectkey", how="inner")
            .merge(thickness, on="subjectkey", how="inner")
            .merge(clinic, on="subjectkey", how="inner")
            .merge(demo, on="subjectkey", how="inner")
            .merge(scanners, on="subjectkey", how="inner")
            .merge(sites, on="subjectkey", how = "inner")
            .merge(sites, on="subjectkey", how = "inner")
            .merge(famid, on="subjectkey", how = "inner")
            )
df_inner['subjectkey'].nunique()
df_unique = df_inner.drop_duplicates(subset=['subjectkey'])

# Select the subjectkey column and save it to a new dataframe
df_subjlist = df_unique[["subjectkey"]]

# Save the subject ID dataframe to a CSV file
df_subjlist.to_csv(os.path.join(ROOTDIR, 'group', 'subjectsID.csv'), index=False)







