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
                'first_input_delay_ms',
                'first_input_delay_cat',
                'overall_category',
                'pct_first_input_delay_ms_fast',
                'pct_first_input_delay_ms_average',
                'pct_first_input_delay_ms_slow',
                'pct_first_contentful_paint_fast',
                'pct_first_contentful_paint_average',
                'pct_first_contentful_paint_slow',
                'page_type',
                'fetch_time',
                'fetch_date'
            ]]
        )

        self.df_lab_responses = pd.DataFrame(
            columns=[[
                'requested_url',
                'final_url',
                'device_type',
                'fetch_time',
                'overall_speed_score',
                'first_contentful_paint',
                'first_meaningful_paint',
                'speed_index',
                'first_cpu_idle',
                'time_to_interactive',
                'estimated_input_latency',
                'fetch_date',
                'page_type'
            ]]
        )

        self.df_field_responses = self.create_field_data_table()
        self.df_lab_responses = self.create_lab_data_table()

# Need to create two tables (one for FIELD data and one for LAB data)
    def create_field_data_table(self):
            for (url, i, j) in zip(
                self.response_object['mobile'].keys(),
                range(0, len(self.response_object['mobile'].keys())),
                range(
                    len(self.response_object['mobile'].keys()),
                    (len(self.response_object['mobile'].keys())*2)+1
                )
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
                self.df_field_responses.loc[i, 'first_input_delay_ms'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
                self.df_field_responses.loc[i, 'first_input_delay_cat'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category']

                # Fill proportions
                self.df_field_responses.loc[i, 'pct_first_input_delay_ms_fast'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][0]['proportion']
                self.df_field_responses.loc[i, 'pct_first_input_delay_ms_average'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][1]['proportion']
                self.df_field_responses.loc[i, 'pct_first_input_delay_ms_slow'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][2]['proportion']

                self.df_field_responses.loc[i, 'pct_first_contentful_paint_fast'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][0]['proportion']
                self.df_field_responses.loc[i, 'pct_first_contentful_paint_average'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][1]['proportion']
                self.df_field_responses.loc[i, 'pct_first_contentful_paint_slow'] = self.response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][2]['proportion']

                # Fill overall category
                self.df_field_responses.loc[i, 'overall_category'] = self.response_object['mobile'][url]['loadingExperience']['overall_category']

                # Fill page type
                self.df_field_responses.loc[i, 'page_type'] = self.response_object['mobile'][url]['page_type']

                # Fill datetime
                self.df_field_responses.loc[i, 'fetch_time'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

                # Fill date understandable by data studio
                self.df_field_responses.loc[i, 'fetch_date'] = datetime.now().strftime("%Y%m%d")

                # --DESKTOP--:
                # Fill urls
                self.df_field_responses.loc[j, 'requested_url'] = self.response_object['desktop'][url]['lighthouseResult']['requestedUrl']
                self.df_field_responses.loc[j, 'final_url'] = self.response_object['desktop'][url]['lighthouseResult']['finalUrl']

                # Fill device type
                self.df_field_responses.loc[j, 'device_type'] = 'desktop'

                # Fill loading experience
                self.df_field_responses.loc[j, 'first_contentful_paint_ms'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile']
                self.df_field_responses.loc[j, 'first_contentful_paint_cat'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']
                self.df_field_responses.loc[j, 'first_input_delay_ms'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
                self.df_field_responses.loc[j, 'first_input_delay_cat'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category']

                # Fill proportions
                self.df_field_responses.loc[j, 'pct_first_input_delay_ms_fast'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][0]['proportion']
                self.df_field_responses.loc[j, 'pct_first_input_delay_ms_average'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][1]['proportion']
                self.df_field_responses.loc[j, 'pct_first_input_delay_ms_slow'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][2]['proportion']

                self.df_field_responses.loc[j, 'pct_first_contentful_paint_fast'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][0]['proportion']
                self.df_field_responses.loc[j, 'pct_first_contentful_paint_average'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][1]['proportion']
                self.df_field_responses.loc[j, 'pct_first_contentful_paint_slow'] = self.response_object['desktop'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][2]['proportion']
                
                # Fill overall category
                self.df_field_responses.loc[j, 'overall_category'] = self.response_object['desktop'][url]['loadingExperience']['overall_category']

                # Fill page type
                self.df_field_responses.loc[j, 'page_type'] = self.response_object['desktop'][url]['page_type']

                # Fill datetime
                self.df_field_responses.loc[j, 'fetch_time'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

                # Fill date understandable by data studio
                self.df_field_responses.loc[j, 'fetch_date'] = datetime.now().strftime("%Y%m%d")

            return self.df_field_responses.reset_index(drop=True)

    
    def create_lab_data_table(self):
        for (url, i, j) in zip(
            self.response_object['mobile'].keys(),
            range(0, len(self.response_object['mobile'].keys())),
            range(
                len(self.response_object['mobile'].keys()),
                (len(self.response_object['mobile'].keys())*2)+1
            )
        ):
            # --MOBILE--:
            self.df_lab_responses.loc[i, 'requested_url'] = self.response_object['mobile'][url]['lighthouseResult']['requestedUrl']
            self.df_lab_responses.loc[i, 'final_url'] = self.response_object['mobile'][url]['lighthouseResult']['finalUrl']
            self.df_lab_responses.loc[i, 'device_type'] = 'mobile'
            self.df_lab_responses.loc[i, 'fetch_time'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.df_lab_responses.loc[i, 'fetch_date'] = datetime.now().strftime("%Y%m%d")

            self.df_lab_responses.loc[i, 'overall_speed_score'] = self.response_object['mobile'][url]['lighthouseResult']['categories']['performance']['score']
            self.df_lab_responses.loc[i, 'first_contentful_paint'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['first-contentful-paint']['score']
            self.df_lab_responses.loc[i, 'first_meaningful_paint'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['first-meaningful-paint']['score']

            self.df_lab_responses.loc[i, 'speed_index'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['speed-index']['score']
            self.df_lab_responses.loc[i, 'first_cpu_idle'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['first-cpu-idle']['score']
            self.df_lab_responses.loc[i, 'time_to_interactive'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['interactive']['score']
            self.df_lab_responses.loc[i, 'estimated_input_latency'] = self.response_object['mobile'][url]['lighthouseResult']['audits']['estimated-input-latency']['score']
            
            self.df_lab_responses.loc[i, 'page_type'] = self.response_object['mobile'][url]['page_type']

            # --DESKTOP--:
            self.df_lab_responses.loc[j, 'requested_url'] = self.response_object['desktop'][url]['lighthouseResult']['requestedUrl']
            self.df_lab_responses.loc[j, 'final_url'] = self.response_object['desktop'][url]['lighthouseResult']['finalUrl']
            self.df_lab_responses.loc[j, 'device_type'] = 'desktop'
            self.df_lab_responses.loc[j, 'fetch_time'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.df_lab_responses.loc[j, 'fetch_date'] = datetime.now().strftime("%Y%m%d")

            self.df_lab_responses.loc[j, 'overall_speed_score'] = self.response_object['desktop'][url]['lighthouseResult']['categories']['performance']['score']
            self.df_lab_responses.loc[j, 'first_contentful_paint'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['first-contentful-paint']['score']
            self.df_lab_responses.loc[j, 'first_meaningful_paint'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['first-meaningful-paint']['score']
            
            self.df_lab_responses.loc[j, 'speed_index'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['speed-index']['score']
            self.df_lab_responses.loc[j, 'first_cpu_idle'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['first-cpu-idle']['score']
            self.df_lab_responses.loc[j, 'time_to_interactive'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['interactive']['score']
            self.df_lab_responses.loc[j, 'estimated_input_latency'] = self.response_object['desktop'][url]['lighthouseResult']['audits']['estimated-input-latency']['score']

            self.df_lab_responses.loc[j, 'page_type'] = self.response_object['desktop'][url]['page_type']

        return self.df_lab_responses.reset_index(drop=True)



