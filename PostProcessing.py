import pandas as pd
import numpy as np
import click
import json
import pprint
from datetime import datetime
from tqdm import tqdm_notebook, tqdm

class ResponseTable:

    def __init__(self, response_json):

        self.response_object = response_json

        self.df_field_responses = pd.DataFrame(
            columns=[[
                'requested_url',
                'final_url',
                'device_type',
                'first_contentful_paint_ms',
                'first_contentful_paint_cat',
                'pct_first_contentful_paint_fast',
                'pct_first_contentful_paint_average',
                'pct_first_contentful_paint_slow',
            ]]
        )

        self.df_field_responses = self.create_field_data_table()

# Need to create two tables (one for FIELD data and one for LAB data)
    def create_field_data_table(self):
            for (url, i) in zip(
                self.response_object['mobile'].keys(),
                range(0, len(self.response_object['mobile'].keys()))
            ):
        
                # --MOBILE--:
                # Fill urls
                self.df_field_responses.loc[i, 'requested_url'] = self.response_object['mobile'][url]['lighthouseResult']['requestedUrl']
                self.df_field_responses.loc[i, 'final_url'] = self.response_object['mobile'][url]['lighthouseResult']['finalUrl']

                # Fill device type
                self.df_field_responses.loc[i, 'device_type'] = 'mobile'

                # Fill loading experience
                self.df_field_responses.loc[i, 'first_contentful_paint_ms'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile']
                self.df_field_responses.loc[i, 'first_contentful_paint_cat'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']

                # Fill proportions
                self.df_field_responses.loc[i, 'pct_first_contentful_paint_fast'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][0]['proportion']
                self.df_field_responses.loc[i, 'pct_first_contentful_paint_average'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][1]['proportion']
                self.df_field_responses.loc[i, 'pct_first_contentful_paint_slow'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][2]['proportion']

            return self.df_field_responses.reset_index(drop=True)
