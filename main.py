import pandas as pd
import numpy as np
import click
import time
import psycopg2
import json
from RequestPageSpeeds import APIResponse
from ResponsePostProcessing import ResponseTable
@click.command()
@click.option(
    '--config-file',
    help='Name of config file.'
)

def main(config_file):

    # Pass in config file
    with open(config_file) as f:
        config_data = json.load(f)

    # 1. Get API response object and save
    my_reponse = APIResponse(config_data['url_file'])
    response = my_reponse.get_contents_obj()

    # 2. Select relevant fields of response
    

    # 3. Get response object in uploadable table
    post_processing = ResponseTable(response)
    field_table_to_upload = post_processing.create_field_data_table()
    lab_table_to_upload = post_processing.create_lab_data_table()

if __name__ == '__main__':
    main()