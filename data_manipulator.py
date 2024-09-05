# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:41:39 2024

@author: matan
"""

class Data_manipulator():
    import pandas as pd
    import numpy as np    
    
    def __init__(self):
        return self

    @staticmethod    
    def filter_subjects(df, subject_df):
        return df[(df["Subject ID"].isin(subject_df["Subject ID"].tolist()))]   
    
    @staticmethod
    def get_last_n_percent_data(data_df, n):
        import math
        
        # If 0 < n < 1 then the percent at the end of a patch is calculated,
        # i.e. the last 10% of each patch
        data_df = data_df.sort_values('id', ascending=True)
        subjects_ids = list(set(data_df['Subject ID'].to_list()))
        
        message = " percent" if 0 < n < 1 else " clicks"

        print("Limiting df to only last " + str(n) + message + " of each patch for " + str(data_df.columns.to_list()))
        for subject_id in subjects_ids:
            print("Current subject " + str(subject_id))
            subject_df = data_df[(data_df["Subject ID"] == subject_id)]

            # get subject's patches to iterate over
            subjects_patches = list(set(subject_df['patch_number'].to_list()))

            for patch_number in subjects_patches:
                current_patch = subject_df[(subject_df['patch_number'] == patch_number)]
                current_patch_ids = current_patch['id'].to_list()

                # Get n'th row value from the end of each patch (if possible)
                first_row_id = current_patch_ids[0]
                limit_row_id = current_patch_ids[0]

                if n >= 1:
                    if len(current_patch_ids) > n:
                        limit_row_id = current_patch_ids[-n]
                elif n > 0 and n < 1:
                    if len(current_patch_ids) > 1:
                        try:
                            limit_row_id = round(current_patch['id'].quantile(1 - n))
                        except:
                            limit_row_id = math.ceil(current_patch['id'].quantile(1 - n))

                data_df.drop(data_df[(data_df['id'] >= first_row_id) & (data_df['id'] < limit_row_id)].index, inplace = True)

        return data_df

    @staticmethod
    def set_task_data_parts(data_df, n_parts):
        data_df = data_df.sort_values('id', ascending=True)
        subjects_ids = list(set(data_df['Subject ID'].to_list()))
        # Add the new parts column with a default value
        data_df['part'] = 0

        print("Setting data parts for " + str(data_df.columns.to_list()))
        for subject_id in subjects_ids:
            print("Current subject " + str(subject_id))
            subject_df = data_df[(data_df["Subject ID"] == subject_id)]
            subject_entity = subject_df['id'].to_list()

            # Get the values of the list parts by the defined percentiles
            percentile_values = []
            percentile = len(subject_entity) / n_parts
            for part_number in range(1, n_parts):
                percentile_values.append(subject_entity[round(part_number * percentile)])

            percentile_values.insert(0, subject_entity[0])
            percentile_values.append(subject_entity[len(subject_entity) - 1])

            for part_number in range(0, n_parts):
                lower_limit_value = percentile_values[part_number]
                upper_limit_value = percentile_values[part_number + 1]

                # update values with parts
                sliced_clicks = subject_entity[subject_entity.index(lower_limit_value) : subject_entity.index(upper_limit_value) + 1]
                for subject_click in sliced_clicks:
                    data_df.loc[data_df['id'] == subject_click, 'part'] = part_number + 1

        return data_df

    @staticmethod
    def get_task_data_by_percentiles(click_df, lower_percentile, upper_percentile):
        # Used to get data for a certain section of the whole task, limited by lower and upper percentile limits of the clicks' ids
        # Returns the selected part of the dataframe, for all subjects
        click_df = click_df.sort_values('id', ascending=True)
        subjects_ids = list(set(click_df['Subject ID'].to_list()))

        for subject_id in subjects_ids:
            subject_df = click_df[(click_df["Subject ID"] == subject_id)]

            # get subject's total number of clicks
            subjects_clicks = subject_df['id'].to_list()
            lower_limit_value = round(subject_df['id'].quantile(lower_percentile))
            upper_limit_value = round(subject_df['id'].quantile(upper_percentile))

            click_df.drop(click_df[(click_df['id'] >= subjects_clicks[0]) & (click_df['id'] < lower_limit_value)].index, inplace = True)
            click_df.drop(click_df[(click_df['id'] > upper_limit_value) & (click_df['id'] <= subjects_clicks[len(subjects_clicks) - 1])].index, inplace = True)

        return click_df

    @staticmethod
    def get_num_clicks_per_patch(click_df, id_as_index=True):
        clicks_per_patch = click_df\
            .groupby(['Subject ID', 'patch_number'], as_index=False)\
            .count()\
            .rename(columns={"id": "num_clicks_per_patch"})\
            [['Subject ID', 'patch_number', 'num_clicks_per_patch']]

        if id_as_index:
           clicks_per_patch = clicks_per_patch.set_index("Subject ID")

        return clicks_per_patch

    @staticmethod
    def get_num_hits_per_patch(click_df, id_as_index=True):
        hits_per_patch = click_df[['Subject ID', 'patch_number', 'is_ripe']]\
            .groupby(['Subject ID', 'patch_number'], as_index=False)\
            .sum()\
            .rename(columns={"is_ripe": "num_hits_per_patch"})

        if id_as_index:
           hits_per_patch = hits_per_patch.set_index("Subject ID")

        return hits_per_patch

    @staticmethod    
    def get_num_unripe_per_patch(click_df, id_as_index=True):
        import numpy as np
        click_df['is_unripe'] = np.where((click_df["is_ripe"] == 0) & (click_df["is_green"] == 0), 1, 0)

        unripe_per_patch = click_df[['Subject ID', 'patch_number', 'is_unripe']]\
            .groupby(['Subject ID', 'patch_number'], as_index=False)\
            .sum()\
            .rename(columns={"is_unripe": "num_unripe_per_patch"})

        if id_as_index:
           unripe_per_patch = unripe_per_patch.set_index("Subject ID")

        return unripe_per_patch
    
    @staticmethod
    def get_num_berries_per_patch(click_df, id_as_index=True):
        clicks_per_patch = Data_manipulator.get_num_clicks_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        greens_per_patch = Data_manipulator.get_num_green_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        berries_per_patch = clicks_per_patch.join(greens_per_patch)

        berries_per_patch['num_berries_per_patch'] = berries_per_patch['num_clicks_per_patch'] - berries_per_patch['num_green_per_patch']
        berries_per_patch = berries_per_patch.reset_index()

        if id_as_index:
           berries_per_patch = berries_per_patch.set_index("Subject ID")

        return berries_per_patch
    
    @staticmethod
    def get_num_green_per_patch(click_df, id_as_index=True):
        green_per_patch = click_df[['Subject ID', 'patch_number', 'is_green']]\
            .groupby(['Subject ID', 'patch_number'], as_index=False)\
            .sum()\
            .rename(columns={"is_green": "num_green_per_patch"})

        if id_as_index:
           green_per_patch = green_per_patch.set_index("Subject ID")

        return green_per_patch

    @staticmethod
    def get_time_per_patch(patch_df):
        patch_df.set_index(['Subject ID', 'patch_number'])
        return patch_df[['Subject ID', 'patch_number', 'patch_length']]

    @staticmethod    
    def get_avg_time_patch(patch_df):
        patch_df = patch_df[['Subject ID', 'patch_length', 'part']].set_index('Subject ID')

        return patch_df\
            .groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"patch_length": "avg_patch_length"})\

    @staticmethod    
    def calc_level_of_redness(click_df):
        click_df['color_code'] = click_df['color'].map(Data_manipulator.color_to_code)
        return click_df

    @staticmethod    
    def color_to_code(color):
        code_dict = {
            "#FF0000" : 1,
            "#FA0000" : 2,
            "#F50000" : 3,
            "#F00000" : 4,
            "#EB0000" : 5,
            "#E60000" : 6,
            "#E10000" : 7,
            "#DC0000" : 8,
            "#D70000" : 9,
            "#D20000" : 10
        }

        try:
            code = code_dict[color]
        except KeyError:
            code = "NA"

        return code

    @staticmethod    
    def get_new_col_names(col_name, parts_number):
        if parts_number == 1:
            return [col_name]
        else:
            col_names = []
            for i in range(1, parts_number + 1):
                col_names.append(col_name + "_" + str(i))
            return col_names