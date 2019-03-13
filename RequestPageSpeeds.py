import pandas as pd
import numpy as np
import requests as re
import urllib.request
import urllib.parse
import click
import json
import time
from datetime import datetime
from tqdm import tqdm_notebook, tqdm

class APIResponse:

    def __init__(self, url_file):

        # Create full contents response dictionary
        self.contents_obj = {}

        self.contents_obj['mobile'] = {}

        self.url_list, self.df_urls = self.load_urls(url_file)


    def get_contents_obj(self):
        '''
        Request response object for each url and store as json.
        '''
        
        for i in tqdm(range(0, len(self.df_urls))):
            success = False

            for j in range(0, 10):
                try:
                    print('Requesting row #:', i)
                    print('Try #:', j)

                    url = self.df_urls.iloc[i]['URL']
                    escaped_url = urllib.parse.quote(url)

                    device_type = self.df_urls.iloc[i]['device_type']
                    page_type = self.df_urls.iloc[i]['page_type']

                    contents = urllib.request.urlopen(
                        'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy={}'\
                        .format(escaped_url, device_type)
                    ).read().decode('UTF-8')

                    contents_json = json.loads(contents)

                    # Insert returned json response into full contents
                    self.contents_obj[device_type][url] = contents_json
                    # Insert page type for that url into full contents
                    self.contents_obj[device_type][url]['page_type'] = page_type

                    success = True

                except Exception as e:
                    if 'Internal Server Error' in str(e):
                        print('Error:', e)
                        print("Error getting response. Sleeping for 5 seconds. Try #%d"%j)
                        time.sleep(5)
                    
                    else:
                        print('Error:', e)
                        print("Error getting response. Sleeping for 1 hour.Try #%d"%j)
                        time.sleep(3600)

                if success:
                    break

        # Save json response
        self.save_contents_to_file(self.contents_obj)

        return self.contents_obj


    def load_urls(self, url_file):
        '''
        Import list of urls.
        '''
        df_urls = pd.read_csv(url_file)
        urls_col = df_urls['URL']
        url_list = urls_col.tolist()

        return url_list, df_urls

    def save_contents_cummulatively(self, contents):
        with open('{}-cummulative_response.json'.format(datetime.now().strftime("%Y-%m-%d")), 'w') as outfile:
            json.dump(contents, outfile, indent=4)

    def save_contents_to_file(self, contents):
        with open('{}-response.json'.format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")), 'w') as outfile:
            json.dump(contents, outfile, indent=4)