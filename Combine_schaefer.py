#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:48:28 2023
@author: khosravip2
Updated on Wed Jun 28 2023 to match the paths for the current directory
"""

import pandas as pd
import os 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

ROOTDIR = '/data/NIMH_scratch/khosravip2/ABCD-CCA'
schaefer_DIR = os.path.join(ROOTDIR, "derivatives", "parcellation")


hemi = ["lh","rh"]
meas = ["thickness","area"]


value = {}
subjID = {}
row = {}
for h in hemi:
    for m in meas:
        if m == "area":
            value["{}_{}".format("area",h)] = pd.read_csv(os.path.join(schaefer_DIR, "schaefer-200-17N_meas-{}_hemi-{}.csv".format("area",h)))
            subjID["{}_{}".format("area",h)]= pd.read_csv(os.path.join(schaefer_DIR, "Ids_meas-{}_hemi-{}.csv".format("area",h)))
            row["{}_{}".format("area",h)]= pd.read_csv(os.path.join(schaefer_DIR, "ColNames_meas-{}_hemi-{}.csv".format("area",h)),index_col=0)
        if m == "thickness":

                value["{}_{}".format("thickness",h)] = pd.read_csv(os.path.join(schaefer_DIR, "schaefer-200-17N_meas-{}_hemi-{}.csv".format("thickness",h)))
                subjID["{}_{}".format("thickness",h)]= pd.read_csv(os.path.join(schaefer_DIR, "Ids_meas-{}_hemi-{}.csv".format("thickness",h)))
                row["{}_{}".format("thickness",h)]= pd.read_csv(os.path.join(schaefer_DIR, "ColNames_meas-{}_hemi-{}.csv".format("thickness",h)),index_col=0)
                
        
                value_area_lh = value["area_lh"]
                value_area_rh = value["area_rh"]  
                id_area_lh = subjID["area_lh"]
                id_area_rh = subjID["area_rh"]
                row_area_lh = row["area_lh"]
                row_area_rh = row["area_rh"]
                
                
                value_thickness_lh = value["thickness_lh"]
                value_thickness_rh = value["thickness_rh"]  
                id_thickness_lh = subjID["thickness_lh"]
                id_thickness_rh = subjID["thickness_rh"]
                row_thickness_lh = row["thickness_lh"]
                row_thickness_rh = row["thickness_rh"]

#%%

            
 #%%   
##############################################
#### combine AREA dataframes horizontally ####
##############################################
area_lh_rh = pd.concat([value_area_lh, value_area_rh], axis=1) 
id_area_lh_rh = pd.concat([id_area_lh, id_area_rh], axis = 1)
id_area_lh_rh.columns = ['id_area_lh', 'id_area_rh']
row_area_lh_rh = pd.concat([row_area_lh, row_area_rh], axis = 0)

# QC: Check for parcels with zero area
zero_area = (area_lh_rh_idx == 0).sum(axis=0)
print("Parcels with zero area across subjects:")
print(zero_area[zero_area > 0])


#%%
area_lh_rh.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "schaefer-200-17N_meas-area_hemi-bh.csv")) # save without index/header
id_area_lh_rh.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "Ids_meas-area_hemi-bh.csv")) # save index (subjectID)
row_area_lh_rh.to_csv(os.path.join(ROOTDIR,  "derivatives", "parcellation", "RowNames_meas-area_hemi-lh-rh.csv")) # save column names 

   
rowT_area_lh_rh = row_area_lh_rh.T
rowT_area_lh_rh.columns = rowT_area_lh_rh.iloc[0]
column_names = rowT_area_lh_rh.columns.tolist()

area_col = []
for c in column_names :
    area_col.append(eval(c).decode())
    
area_lh_rh.columns = area_col
area_lh_rh_idx = pd.concat([area_lh_rh, id_area_lh_rh], axis = 1)
area_lh_rh_idx = area_lh_rh_idx.drop(columns=["id_area_rh"])
# remove meaningless variables
area_lh_rh_idx = area_lh_rh_idx.loc[:, ~area_lh_rh_idx.columns.str.contains('Background\+FreeSurfer_Defined_Medial_Wall')]

area_lh_rh_idx = area_lh_rh_idx.rename(columns={"id_area_lh": "SubjectID"})
area_lh_rh_idx = area_lh_rh_idx.set_index('SubjectID') # set index 

area_lh_rh_idx.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "schaefer-200-17N_meas-area_hemi-bh.csv"), index= True, header=True) # save full df with index & header


###################################################
#### combine THICKNESS dataframes horizontally ####
###################################################  
    
thickness_lh_rh = pd.concat([value_thickness_lh, value_thickness_rh], axis=1) 
id_thickness_lh_rh = pd.concat([id_thickness_lh, id_thickness_rh], axis = 1)
id_thickness_lh_rh.columns = ['id_thickness_lh', 'id_thickness_rh']
row_thickness_lh_rh = pd.concat([row_thickness_lh, row_thickness_rh], axis = 0)

# QC: Check for parcels with zero thickness
zero_thick = (thickness_lh_rh_idx == 0).sum(axis=0)
print("Parcels with zero thickness across subjects:")
print(zero_thick[zero_thick > 0])


thickness_lh_rh.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "schaefer-200-17N_meas-thickness_hemi-lh-rh.csv")) # save without index/header
id_thickness_lh_rh.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "Ids_meas-thickness_hemi-lh-rh.csv")) # save index (subjectID)
row_thickness_lh_rh.to_csv(os.path.join(ROOTDIR,  "derivatives", "parcellation", "RowNames_meas-thickness_hemi-lh-rh.csv")) # save column names 

rowT_thickness_lh_rh = row_thickness_lh_rh.T
rowT_thickness_lh_rh.columns = rowT_thickness_lh_rh.iloc[0]
column_names = rowT_thickness_lh_rh.columns.tolist()

thickness_col = []
for c in column_names :
    thickness_col.append(eval(c).decode())
    
thickness_lh_rh.columns = thickness_col

thickness_lh_rh_idx = pd.concat([thickness_lh_rh, id_thickness_lh_rh], axis = 1)
thickness_lh_rh_idx  = thickness_lh_rh_idx.rename(columns={"id_thickness_lh": "SubjectID"})
# remove meaningless variables
thickness_lh_rh_idx = thickness_lh_rh_idx.loc[:, ~thickness_lh_rh_idx.columns.str.contains('Background\+FreeSurfer_Defined_Medial_Wall')]

thickness_lh_rh_idx = thickness_lh_rh_idx.drop(columns=["id_thickness_rh"])
thickness_lh_rh_idx  = thickness_lh_rh_idx.set_index('SubjectID') # set index 


thickness_lh_rh_idx.to_csv(os.path.join(ROOTDIR, "derivatives", "parcellation", "schaefer-200-17N_meas-thickness_hemi-bh.csv")) # save full df with index & header

#plot for one parcel
parcel_name = "lh_PFCd_1"  # change to a region of interest
if parcel_name in thickness_lh_rh_idx.columns:
    sns.histplot(thickness_lh_rh_idx[parcel_name])
    plt.title(f"Distribution of Thickness: {parcel_name}")
    plt.xlabel("Thickness (mm)")
    plt.ylabel("Subject Count")
    plt.show()
else:
    print(f"{parcel_name} not found in data.")
