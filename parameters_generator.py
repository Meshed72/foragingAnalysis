# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:44:37 2024

@author: matan
"""

from data_manipulator import Data_manipulator as dm

class Parameters_generator:    
    def __init__(self):        
        return None
    
    def get_p1(self, patch_df):
        # Average time in each patch
        return dm.get_avg_time_patch(patch_df)

    def get_p2(self, patch_df):
        # Number of overall patches visited
        sum_patches = patch_df\
            .groupby(['Subject ID'], as_index=False)\
            .count()\
            [['Subject ID', 'patch_number']]

        return sum_patches.rename(columns={"patch_number": "number_of_patches"})\
            .set_index("Subject ID")

    def get_p3(self, click_df):
        # The average number of overall clicks (including greens)
        return dm.get_num_clicks_per_patch(click_df).groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"num_clicks_per_patch": "avg_clicks_per_patch"})\
            ["avg_clicks_per_patch"]\
            .to_frame()

    def get_p4(self, click_df):
        # The average number of berries collected (not including greens)
        clicks_per_patch = dm.get_num_clicks_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        greens_per_patch = dm.get_num_green_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])

        join_df = clicks_per_patch.join(greens_per_patch)
        join_df['num_berries_per_patch'] = join_df['num_clicks_per_patch'] - join_df['num_green_per_patch']

        return join_df.groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"num_berries_per_patch": "avg_berries_per_patch"})\
            ["avg_berries_per_patch"]\
                .to_frame()

    def get_p5(self, click_df):
        # Average number of "hits" (ripe berries picked) in each patch
        return dm.get_num_hits_per_patch(click_df).groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"num_hits_per_patch": "avg_hits_per_patch"})\
                ["avg_hits_per_patch"]\
                .to_frame()

    def get_p6a(self, click_df):
        # Hits % - number of hits out of all the clicks
        num_hits_per_patch = dm.get_num_hits_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        num_clicks_per_patch = dm.get_num_clicks_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])

        hits_percent = (num_hits_per_patch["num_hits_per_patch"] / num_clicks_per_patch["num_clicks_per_patch"])
        hits_percent = hits_percent.rename("avg_hits_per_patch_percent")
        return hits_percent.groupby(['Subject ID'], as_index=True)\
            .mean()\
            .to_frame()

    def get_p6b(self, click_df):
        # Hits % - number of hits out of berries clicks
        num_hits_per_patch = dm.get_num_hits_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        num_berries_per_patch = dm.get_num_berries_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])

        hits_percent = (num_hits_per_patch["num_hits_per_patch"] / num_berries_per_patch["num_clicks_per_patch"])
        hits_percent = hits_percent.rename("avg_hits_of_berries_per_patch_percent")
        return hits_percent.groupby(['Subject ID'], as_index=True)\
            .mean()\
            .to_frame()

    def get_p7(self, click_df):
        # Average number of "False alarm" (unripe berries picked) in each patch
        return dm.get_num_unripe_per_patch(click_df).groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"num_unripe_per_patch": "avg_unripe_per_patch"})\
                ["avg_unripe_per_patch"]\
                .to_frame()

    def get_p8(self, click_df):
        # Average of false alarm % (unripe berries picked) in each patch
        num_unripe_per_patch = dm.get_num_unripe_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])
        num_berries_per_patch = dm.get_num_berries_per_patch(click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])

        hits_percent = num_unripe_per_patch["num_unripe_per_patch"] / num_berries_per_patch["num_berries_per_patch"]
        false_alarm_percent = hits_percent.rename("false_alarm_percent_per_patch").to_frame()

        # In case only greens were clicked, we set a default value of 0 for unripe berries
        false_alarm_percent['false_alarm_percent_per_patch'] = false_alarm_percent['false_alarm_percent_per_patch'].fillna(0)

        return false_alarm_percent.groupby(['Subject ID'], as_index=True)\
            .mean()

    def get_p9(self, click_df):
        # Average number of green squares picked in each patch
        return dm.get_num_green_per_patch(click_df).groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={"num_green_per_patch": "avg_green_per_patch"})\
            ["avg_green_per_patch"]\
            .to_frame()

    def get_p10a(self, click_df, subject_df):
        # General: number of hits (good berries)/ seconds elapsed – at the end of the task
        total_time_per_subject = subject_df.set_index("Subject ID")['task_length']

        num_of_clicks = 10
        limited_click_df = dm.get_last_n_percent_data(click_df, num_of_clicks)

        total_hits_per_subject = limited_click_df[['Subject ID', 'is_ripe']]\
            .groupby(['Subject ID'], as_index=False)\
            .sum()\
            .rename(columns={"is_ripe": "num_hits_per_patch"})\
            [['Subject ID', 'num_hits_per_patch']]\
            .set_index("Subject ID")

        join = total_hits_per_subject.join(total_time_per_subject)
        return_rate = (join['num_hits_per_patch'] / join['task_length'])\
        .to_frame()\
        .rename(columns={0 : 'general_return_rate_click_' + str(num_of_clicks)})
        p10a = return_rate

        # Calculate the rest of the clicks
        for click_n in range(num_of_clicks - 1, 0, -1):
            print("p10a: click " + str(click_n))
            limited_click_df = dm.get_last_n_percent_data(click_df, click_n)

            total_hits_per_subject = limited_click_df[['Subject ID', 'is_ripe']]\
                .groupby(['Subject ID'], as_index=False)\
                .sum()\
                .rename(columns={"is_ripe": "num_hits_per_patch"})\
                [['Subject ID', 'num_hits_per_patch']]\
                .set_index("Subject ID")

            join = total_hits_per_subject.join(total_time_per_subject)
            return_rate = (join['num_hits_per_patch'] / join['task_length'])\
            .to_frame()\
            .rename(columns={0 : 'general_return_rate_click_' + str(click_n)})
            p10a = p10a.join(return_rate)

        return p10a

    def get_p10b(self, click_df, patch_df):
        # 10 last clicks in reverse order: (good berries)/ seconds elapsed – average from all patches

        # The calculation is:
        # 1: get num of hits per patch
        # 2: get time per patch
        # 3: join 1 and 2
        # 3: calculate mean of 3 per subject

        num_of_clicks = 10
        limited_click_df = dm.get_last_n_percent_data(click_df, num_of_clicks)

        num_hits_per_patch = dm.get_num_hits_per_patch(limited_click_df, id_as_index=False)\
            .set_index(['Subject ID', 'patch_number'])

        patch_length = dm.get_time_per_patch(patch_df)\
            .set_index(['Subject ID', 'patch_number'])

        patch_hits_time_join = num_hits_per_patch.join(patch_length)
        patch_hits_time_join['hits_time_ratio_mean_click_' + str(num_of_clicks)] = patch_hits_time_join['num_hits_per_patch'] / patch_hits_time_join['patch_length']
        p10b = patch_hits_time_join.groupby(['Subject ID'], as_index=True)\
            .mean()\
            ['hits_time_ratio_mean_click_' + str(num_of_clicks)]\
            .to_frame()

        # Calculate the rest of the clicks
        for click_n in range(num_of_clicks - 1, 0, -1):
            print("p10b: click " + str(click_n))
            limited_click_df = dm.get_last_n_percent_data(click_df, click_n)

            num_hits_per_patch = dm.get_num_hits_per_patch(limited_click_df, id_as_index=False)\
                .set_index(['Subject ID', 'patch_number'])
            patch_length = dm.get_time_per_patch(patch_df)\
                .set_index(['Subject ID', 'patch_number'])

            patch_hits_time_join = num_hits_per_patch.join(patch_length)
            patch_hits_time_join['hits_time_ratio_mean_click_' + str(click_n)] = patch_hits_time_join['num_hits_per_patch'] / patch_hits_time_join['patch_length']
            p10b = p10b.join(patch_hits_time_join.groupby(['Subject ID'], as_index=True)\
                .mean()\
                ['hits_time_ratio_mean_click_' + str(click_n)]\
                .to_frame())

        return p10b

    def get_p11a(self, click_df):
        # Average level of redness all over the task
        general_redness = click_df[(click_df["color_code"] != "NA")]\
        .set_index("Subject ID")['color_code']
        general_redness = general_redness.groupby(['Subject ID'], as_index=True)\
            .mean()

        return general_redness.rename('general_redness').to_frame()

    def get_p11b(self, click_df):        
        # Average level of redness in 10 last clicks
        num_of_clicks = 10

        redness_df = click_df[(click_df["color_code"] != "NA")]\
        .set_index("Subject ID")['color_code']

        p11b = redness_df.groupby(['Subject ID'], as_index=True)\
            .mean()\
            .to_frame()\
            .rename(columns={'color_code' : 'redness_per_patch_click_' + str(num_of_clicks)})

        # Calculate the rest of the clicks
        for click_n in range(num_of_clicks - 1, 0, -1):
            print("p11b: click " + str(click_n))
            limited_click_df = dm.get_last_n_percent_data(click_df, click_n)

            redness_df = limited_click_df[(limited_click_df["color_code"] != "NA")]\
            .set_index("Subject ID")['color_code']

            redness_df = redness_df.groupby(['Subject ID'], as_index=True)\
                .mean()\
                .to_frame()\
                .rename(columns={'color_code' : 'redness_per_patch_click_' + str(click_n)})

            p11b = p11b.join(redness_df)

        return p11b

    def get_p13(self, click_df):
        # Number of ripe berries left
        num_berries_in_patch = 40
        hits_per_patch = dm.get_num_hits_per_patch(click_df)
        hits_per_patch['berries_left'] = num_berries_in_patch - hits_per_patch['num_hits_per_patch']

        return hits_per_patch.groupby(['Subject ID'], as_index=True)\
            .mean()\
            .rename(columns={'berries_left' : 'avg_berries_left'})\
            ['avg_berries_left']\
            .to_frame()

    @staticmethod 
    def calc_dass(dass_df):
        #  Drop infrequency item 14
        dass_df = dass_df.query('question_14 == 0')
        dass_df = dass_df.drop(columns=['id', 'question_14'])
        
        depression_items = ["question_" + str(i) for i in [3, 5, 10, 13, 16, 17, 21]]
        anxiety_items = ["question_" + str(i) for i in [2, 4, 7, 9, 15, 19, 20]]    
        all_items = depression_items + anxiety_items

        dass_df['dass_depression'] = dass_df[depression_items].sum(axis=1)
        dass_df['dass_anxiety'] = dass_df[anxiety_items].sum(axis=1)
        dass_df['dass_general'] = dass_df[all_items].sum(axis=1)
        return dass_df[['Subject ID', 'dass_depression', 'dass_anxiety', 'dass_general']].set_index('Subject ID')

    @staticmethod     
    def calc_oci(oci_df):
        #  Drop infrequency item 11
        oci_df = oci_df.set_index('Subject ID').query('question_11 == 0')
        oci_df['oci_sum'] = oci_df.drop(columns=['id', 'question_11']).sum(axis=1, numeric_only=True)
        return oci_df[['oci_sum']]

    @staticmethod 
    def calc_aaq(aaq_df):
        #  Drop infrequency item 5
        aaq_df = aaq_df.set_index('Subject ID').query('question_6 == 7')
        aaq_df['aaq_sum'] = aaq_df.drop(columns=['id', 'question_6']).sum(axis=1, numeric_only=True)
        return aaq_df[['aaq_sum']]
    