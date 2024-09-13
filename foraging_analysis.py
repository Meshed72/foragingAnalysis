# -*- coding: utf-8 -*-
"""
Created on Sun May 12 13:16:25 2024

@author: matan
"""

import foraging_analysis_object as fgo

N_PARTS = 3
LAST_N_PERCENT = 0
SELECTED_PART = 0

# 'C:/Users/matan/Documents/Matan/Foraging/DATA/Preliminary anlysis/Initial analysis 4_24/'
fgo.Foraging_analysis_object('C:/Users/meshe/OneDrive/Documents/Foraging/DATA/Preliminary anlysis/Initial analysis 4_24/', N_PARTS, LAST_N_PERCENT, SELECTED_PART)\
    .load_files()\
    .apply_basic_corrections()\
    .leave_relevant_subjects()\
    .calc_level_of_redness()\
    .calculate_questionnaires()\
    .set_click_parts()\
    .keep_last_n_of_data()\
    .calculate_all_paramteres()\
    .clean_outliers()\
    .all_parameters_to_csv('all_parameters_all_parts_no_outliers')

# create a method in Foraging_analysis_object that reads all csv files in a folder an unions them

