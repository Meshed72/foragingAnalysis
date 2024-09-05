# -*- coding: utf-8 -*-
"""
Created on Sun May 12 13:16:25 2024

@author: matan
"""

import pandas as pd
import numpy as np
from data_manipulator import Data_manipulator as dm
import parameters_generator as pg

class Foraging_analysis_object():
    def __init__(self, path, n_parts=3, last_n_percent=0.1, selected_part=0):
        self.path = path
        self.n_parts = n_parts
        self.selected_part = selected_part
        self.last_n_percent = last_n_percent
        self.all_paramteres_df = None
        self.parameters_generator = pg.Parameters_generator()  
        
    def load_files(self):
        self.click_df = pd.read_csv(self.path + 'click.csv')
        self.patch_df = pd.read_csv(self.path + 'patch.csv')
        self.subject_df = pd.read_csv(self.path + 'subjects.csv')
        self.oci_df = pd.read_csv(self.path + 'oci.csv')
        self.dass_df = pd.read_csv(self.path + 'dass.csv')
        self.aaq_df = pd.read_csv(self.path + 'aaq.csv')
        self.relevant_subjects_df = pd.read_csv(self.path + 'valid subjects.csv')
        # self.prolific_df = pd.read_csv(self.path + 'prolific data.csv')
        # self.all_parameters_df = pd.read_csv(self.path + 'all_parameters.csv')                        
        
        return self
    
    def set_click_parts(self):
        # Sets the parts nmuber for clicks an patchs dfs
        if self.n_parts > 0:            
            self.click_df = dm.set_task_data_parts(self.click_df, self.n_parts)
            self.patch_df = dm.set_task_data_parts(self.patch_df, self.n_parts)
            
            # Select a single part
            if self.selected_part > 0:
                self.click_df = self.click_df[(self.click_df["part"] == self.selected_part)]
                self.patch_df = self.patch_df[(self.patch_df["part"] == self.selected_part)]
        else:
            self.click_df['part'] = 0
            self.patch_df['part'] = 0
                
        return self
          
    def keep_last_n_of_data(self):
        if self.last_n_percent > 0:
            self.click_df = dm.get_last_n_percent_data(self.click_df, self.last_n_percent)
            self.patch_df = dm.get_last_n_percent_data(self.patch_df, self.last_n_percent)
        return self
    
    def calculate_questionnaires(self):
        self.oci_df = pg.Parameters_generator.calc_oci(self.oci_df)
        self.dass_df = pg.Parameters_generator.calc_dass(self.dass_df)
        self.aaq_df = pg.Parameters_generator.calc_aaq(self.aaq_df)
        return self
                
    def calc_level_of_redness(self):
        self.click_df = dm.calc_level_of_redness(self.click_df)
        return self
    
    def apply_basic_corrections(self):
        #  Fix columns
        self.patch_df = self.patch_df.drop(columns=['subject_uuid']).rename(columns={"subject_id": "Subject ID"})
        self.click_df = self.click_df.drop(columns=['subject_uuid']).rename(columns={"subject_id": "Subject ID"})
        self.oci_df = self.oci_df.drop(columns=['subject_uuid']).rename(columns={"subject_id": "Subject ID"})
        self.dass_df = self.dass_df.drop(columns=['subject_uuid']).rename(columns={"subject_id": "Subject ID"})
        self.aaq_df = self.aaq_df.drop(columns=['subject_uuid']).rename(columns={"subject_id": "Subject ID"})
        
        # Remove subjects with null IDs
        self.click_df = self.click_df[(self.click_df["Subject ID"] != "null")]
        self.patch_df = self.patch_df[(self.patch_df["Subject ID"] != "null")]
        self.subject_df = self.subject_df[(self.subject_df["Subject ID"] != "null")]
        
        return self
        
    def leave_relevant_subjects(self):    
        # Leave only relevant (valid) subjects on click_df, patch_df
        relevant_subjects_list = self.relevant_subjects_df["Subject ID"].to_list()
    
        self.click_df = self.click_df[(self.click_df["Subject ID"].isin(relevant_subjects_list))]
        self.patch_df = self.patch_df[(self.patch_df["Subject ID"].isin(relevant_subjects_list))]
        self.oci_df = self.oci_df[(self.oci_df["Subject ID"].isin(relevant_subjects_list))]
        self.dass_df = self.dass_df[(self.dass_df["Subject ID"].isin(relevant_subjects_list))]
        self.aaq_df = self.aaq_df[(self.aaq_df["Subject ID"].isin(relevant_subjects_list))]
        self.subject_df = self.subject_df[(self.subject_df["Subject ID"].isin(relevant_subjects_list))]
        
        return self
            
    def calculate_all_paramteres(self):
        # Calculate the parameters
        p1 = self.parameters_generator.get_p1(self.patch_df)
        print("p1 ready")
        p2 = self.parameters_generator.get_p2(self.patch_df)
        print("p2 ready")
        p3 = self.parameters_generator.get_p3(self.click_df)
        print("p3 ready")
        p4 = self.parameters_generator.get_p4(self.click_df)
        print("p4 ready")
        p5 = self.parameters_generator.get_p5(self.click_df)
        print("p5 ready")
        p6a = self.parameters_generator.get_p6a(self.click_df)
        print("p6a ready")
        p6b = self.parameters_generator.get_p6b(self.click_df)
        print("p6b ready")
        p7 = self.parameters_generator.get_p7(self.click_df)
        print("p7 ready")
        p8 = self.parameters_generator.get_p8(self.click_df)
        print("p8 ready")
        p9 = self.parameters_generator.get_p9(self.click_df)
        print("p9 ready")
        p10a = self.parameters_generator.get_p10a(self.click_df, self.subject_df)
        print("p10a ready")
        p10b = self.parameters_generator.get_p10b(self.click_df, self.patch_df)
        print("p10b ready")
        p11a = self.parameters_generator.get_p11a(self.click_df)
        print("p11a ready")
        p11b = self.parameters_generator.get_p11b(self.click_df)
        print("p11b ready")
        p13 = self.parameters_generator.get_p13(self.click_df)
        print("p13 ready")
        
        self.subject_df = self.subject_df[["Subject ID", "color_test_score", "color_test_length"]].set_index("Subject ID")
        # self.all_paramteres_df = self.all_paramteres_df.join([self.oci_df, self.dass_df, self.aaq_df, self.subject_df], how='inner')
        self.all_paramteres_df = p1.join([p2, p3, p4, p5, p6a, p6b, p7, p8, p9, p10a, p10b, p11a, p11b, p13, self.oci_df, self.dass_df, self.aaq_df, self.subject_df], how='outer')        
        
        if self.selected_part == 0:
            self.all_paramteres_df['part'] = 'all parts'
        
        return self
    
    def clean_outliers(self):  
        # Clean the data according to stds
        stds_limit = 2.5
        
        relevant_params = ['avg_patch_length', 'number_of_patches', 'avg_clicks_per_patch', 'avg_berries_per_patch',\
                           'avg_hits_per_patch_percent', 'false_alarm_percent_per_patch', 'avg_green_per_patch',\
                           'general_redness', 'avg_berries_left', 'color_test_score']
        
        stds_dict = {}
        for param in relevant_params:
            param_as_list = self.all_paramteres_df[param].tolist()
            stds_dict[param] = np.mean(param_as_list) + (stds_limit * np.std(param_as_list))
        
        stds_list = [
            f'avg_patch_length > {-1 * stds_dict["avg_patch_length"]} and avg_patch_length < {stds_dict["avg_patch_length"]}',\
            f'number_of_patches > {-1 * stds_dict["number_of_patches"]} and number_of_patches < {stds_dict["number_of_patches"]}',\
            f'avg_clicks_per_patch > {-1 * stds_dict["avg_clicks_per_patch"]} and avg_clicks_per_patch < {stds_dict["avg_clicks_per_patch"]}',\
            f'avg_berries_per_patch > {-1 * stds_dict["avg_berries_per_patch"]} and avg_berries_per_patch < {stds_dict["avg_berries_per_patch"]}',\
            f'avg_hits_per_patch_percent > {-1 * stds_dict["avg_hits_per_patch_percent"]}',\
            f'false_alarm_percent_per_patch < {stds_dict["false_alarm_percent_per_patch"]}',\
            f'avg_green_per_patch < {stds_dict["avg_green_per_patch"]}',\
            f'general_redness < {stds_dict["general_redness"]}',\
            f'avg_berries_left < {stds_dict["avg_berries_left"]}',\
            f'color_test_score < {stds_dict["color_test_score"]}'
        ]
        
        for std in stds_list:        
            self.all_paramteres_df = self.all_paramteres_df.query(std)
        return self
    
    def all_parameters_desc(self):
        self.all_paramteres_df.all_parameters.describe()
        
    def all_parameters_to_csv(self, file_name):
        # all_parameters.to_csv(self.path + 'all_parameters_part' + str(part) +'.csv', mode='w')
        self.all_paramteres_df.to_csv(self.path + file_name + '.csv', mode='w')
        print("Exported to csv: " + file_name)
        
        

        

        

        

        
    




    
    
    