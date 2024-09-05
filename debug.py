# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:16:18 2024

@author: matan
"""

# Users which weren't received
# prolific_subjects = prolific_df['Participant id'].to_list()

# subjects_received = subject_df[(subject_df["start_time"].str.contains("2024-01-09"))]['Subject ID'].to_list()
# subjects_not_received = [user_id for user_id in relevant_subjects_df["Subject ID"].to_list() if user_id not in all_parameters_df["Subject ID"].to_list()]

# Questionnaires - no longer needed
# oci_received = [user_id for user_id in prolific_subjects if user_id in oci_df['Subject ID'].to_list()]
# dass_received = [user_id for user_id in prolific_subjects if user_id in dass_df['Subject ID'].to_list()]
# aaq_received = [user_id for user_id in prolific_subjects if user_id in aaq_df['Subject ID'].to_list()]

# Get specific subjects
# relevant_subjects_list = [s.replace(" ", "") for s in relevant_subjects_df['Subject ID'].to_list()]

# DEBUG
# subject_id = '644024b5ad69ecb3872c8680'
# patch_df = patch_df[(patch_df["Subject ID"] in relevant_subjects_list)]
# subject_df = subject_df[(subject_df["start_time"].str.contains("2024-01-09"))]