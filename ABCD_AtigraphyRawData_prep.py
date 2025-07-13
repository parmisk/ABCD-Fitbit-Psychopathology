#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 16 2023

@author: khosravip2
"""

import pandas as pd
import os
import glob

def process_file(filepath, subject_number, event_name, column_rename_map=None):
    """Read each CSV file, renames columns (some columns were originally labeled as 'value'),
        and adds subject number and event information (time point of data collected)."""
    df = pd.read_csv(filepath)
    if column_rename_map:
        df.rename(columns=column_rename_map, inplace=True)
    df['Subject_Number'] = subject_number
    df['Event_Name'] = event_name
    return df

def extract_info_from_path(subject_path, filename):
    """Extracts subject number and event name from the file path using .split"""
    parts = subject_path.split('/')
    mainpart = parts[-1]
    parts = mainpart.split('_')
    subject_number = parts[0] + '_' + parts[1]
    event_name = '_'.join(parts[2:]).replace(filename, '')
    return subject_number, event_name

def combine_and_save_data(subject_folders, file_endings, column_rename_maps, output_folder, output_filenames):
    """Combine data from multiple files (by subject) and save them into separate CSV 
        files based on data (e.g., minutes sleep separate from stages of sleep)."""
    for file_ending, column_rename_map, output_filename in zip(file_endings, column_rename_maps, output_filenames):
        master_df = pd.DataFrame()
        for subject in subject_folders:
            if os.path.isdir(subject):
                for filename in os.listdir(subject):
                    if filename.endswith(file_ending):
                        filepath = os.path.join(subject, filename)
                        if os.path.isfile(filepath):
                            subject_number, event_name = extract_info_from_path(subject, file_ending)
                            df = process_file(filepath, subject_number, event_name, column_rename_map)
                            master_df = pd.concat([master_df, df], ignore_index=True)
        output_file = os.path.join(output_folder, output_filename)
        master_df.to_csv(output_file, index=False)

base_path = '/Users/khosravip2/Desktop/Fitbit_test/'  # Replace with the path to your base directory
output_folder = os.path.join(base_path, 'combined_data') # I made this directory as my output directory before runing the script.
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
subject_folders = glob.glob(os.path.join(base_path, 'NDAR*'))

file_endings = ['minuteSleep.csv', 'heartrate_1min.csv', 'minuteCaloriesNarrow.csv', 'minuteIntensitiesNarrow.csv', 'minuteMETsNarrow.csv', 'minuteStepsNarrow.csv', '30secondSleepStages.csv']
column_rename_maps = [
    {'value': 'minute_sleep', 'logId': 'minute_sleep_logId'},
    {'Value': 'HR_1min'},
    None,  # Add rename maps for other files as needed
    None,
    None,
    None,
    None
]

# saveubg all the merged dataframes 
output_filenames = ['minutesSleep_master_df.csv', '1minHR_master_df.csv', 'minuteCalories_master_df.csv', 'minuteIntensities_master_df.csv', 'minuteMETs_master_df.csv', 'minuteSteps_master_df.csv', '30second_sleep-stages_master_df.csv']

combine_and_save_data(subject_folders, file_endings, column_rename_maps, output_folder, output_filenames)
