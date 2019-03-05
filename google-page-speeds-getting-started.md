# Getting Started with Google's Page Speed API

Page speed is one of the biggest indicators of how long someone will spend on your site. Have slower page speeds is directly correlated with higher bounce rates, lower conversion rates, and hence, lower revenue.

To get some insight into whether load times may be affecting your audience retension and conversion, the Google's Page Speed Insights tool is great for a quick glance at your website's performance.

## What's so great about Page Speed Insights?
With this tool, you can plug in a URL and receive a summary of its performance. This is great for a quick overview, but what if you have a bigger ecommerce website and want to dive deeper into the performance of multiple sections and page types?
This is where the API comes in. The Page Speed Insights API gives websites the opportunity to analyze performance at a more granular level, both in terms of time frame and web pages.

***This is a quick setup guide for anyone who wishes to make API requests for multiple web pages at custom timed intervals.***
*This guide assumes some familiarity with scripting and uses **Python**, a programming language that is fairly beginner-friendly due to its readability.*

## Objectives
1. Understand how to form an API query URL
2. Construct a loop to request multiple URL queries
3. Extract basic information from the API resonse without having to navigate pages of documentation
4. Run the given example script

## Getting set up
There are a few steps you will need to follow before running a Python script that queries the Page Speed Insights API. This mostly includes Python-related tools.

* ### API setup
    
    Unlike some other Google APIs, you don't need an API key to get started with this one.

* ### Make sure you have [Python 3](https://www.python.org/downloads/) installed
    You'll also need to setup your [mac](https://sourabhbajaj.com/mac-setup/)/[windows](TODO) development environment if you haven't already

* ### Python client library setup
    In order to use the API's Python client library to acccess the API, you will need to run this command in the terminal:

    ```
    pip install --upgrade google-api-python-client
    ```

## Making the requests

### Basics of a request
The format of a query is an HTTP request as follows:

`GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed`

We can then tag on additional [parameters](https://developers.google.com/speed/docs/insights/v5/reference/pagespeedapi/runpagespeed) for a unique request, such as the URL we want to find the page speed of, and the device type to use, as shown below:

`
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={`url`}&strategy={`device_type`}
`

### Python packages
In order to make and read the requests, we will need to import several Python libraries:
- **urllib**: To open the request URLs
- **json**: To parse and read the response objects


### Constructing the query
Now, to make the request using Python, we use the `urllib.request.urlopen()` method from `urllib`:

```python
url = 'www.example_1.com'
device_type = 'mobile'

# Construct request url
contents = urllib.request.urlopen(
    'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy={}'\
    .format(url, device_type)
).read().decode('UTF-8')
```


### Making multiple queries
As the point of using this API is to be able to run more than just one request, we will need to be able to construct and run multiple URLs through.

One way to do this is to store the parameters for the requests (`URLs` and `device types`) in a CSV, which we can load into a Pandas DataFrame to iterate over. Notice below that each request, or unique `URL` - `device_type` pair has its own row.

#### Store data in CSV

```python
    URL                 device_type
0   www.example_1.com   desktop
1   www.example_1.com   mobile
2   www.example_2.com   desktop
3   www.example_2.com   mobile
```

#### Load the CSV

```python
def load_urls(self, url_file):
    '''
    Import urls.
    '''
    df_urls = pd.read_csv(url_file)
    urls_col = df_urls['URL']
    url_list = urls_col.tolist()

    return url_list, df_urls
```
Once we have a dataset with all the URLs to request, we can create a loop to iterate through and make a query per row of the dataframe. We can see this happening in the function, `get_contents_obj()` below:

```python

def get_contents_obj(df):
        '''
        Input: Takes in dataframe (df) of URLs to request.
        Action: Requests response object for each url and stores as json.
        Output: Returns response_object with all responses.
        '''

        # This is where the responses will be stored
        response_object = {}
        
        # Iterating through df
        for i in range(0, len(df)):

            # Define the request parameters
            url = df.iloc[i]['URL']
            device_type = df.iloc[i]['device_type']

            # Making request
            contents = urllib.request.urlopen(
                'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy={}'\
                .format(url, device_type)
            ).read().decode('UTF-8')

            # Converts to json format
            contents_json = json.loads(contents)

            # Insert returned json response into response_object
            response_object[device_type][url] = contents_json

        return response_object

```

## Reading the response
Before applying any filters or formatting on the data, we can first store the full response object for future use with a function like this:
```python
def save_all_contents_to_file(self, contents):
    with open('data/{}-response.json'.format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")), 'w') as outfile:
        json.dump(contents, outfile, indent=4)
```

The response returned is a large object (JSON) with many different properties and is too large to decipher without filtering and formatting. To do this, we will be using the Pandas library, which makes it easy to format data in table format and export to CSV.

As there are two different sources of page speed data, we will be focusing on just `field data` for now, and on just these properties:
- `Requested URL`
- `Final URL`
- `First Contentful Paint` (ms)
- `First Contentful Paint` (proportions of slow, average, fast)
- `First Input Delay` (ms)
- `First Input Delay` (proportions of slow, average, fast)



We can extract this for either, or both, the mobile and desktop data.

If we call our Pandas dataframe `df_field_responses`, here is how we would extract these properties:
```python
# Specify the device_type (mobile or desktop)
device_type = 'mobile'

for (url, i) in zip(
    response_object[device_type].keys(),
    range(0, len(df))
):
    # URLs
    df_field_responses.loc[i, 'requested_url'] =
        response_object[device_type][url]['lighthouseResult']['requestedUrl']
    df_field_responses.loc[i, 'final_url'] =
        response_object[device_type][url]['lighthouseResult']['finalUrl']

    # Loading experience: First Contentful Paint (ms)
    df_field_responses.loc[i, 'FCP_ms'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile']
    df_field_responses.loc[i, 'FCP_category'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['category']
    # Loading experience: First Input Delay (ms)
    df_field_responses.loc[i, 'FID_ms'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile']
    df_field_responses.loc[i, 'FID_category'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['category']

    # Proportions: First Contentful Paint
    df_field_responses.loc[i, 'FCP_fast'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][0]['proportion']
    df_field_responses.loc[i, 'FCP_avg'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][1]['proportion']
    df_field_responses.loc[i, 'FCP_slow'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions'][2]['proportion']
    # Proportions: First Contentful Paint
    df_field_responses.loc[i, 'FID_fast'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][0]['proportion']
    df_field_responses.loc[i, 'FID_avg'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][1]['proportion']
    df_field_responses.loc[i, 'FID_slow'] =
    response_object['mobile'][url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions'][2]['proportion']
```
Then to store the dataframe, `df_field_responses`, in a CSV:

```python
df_field_responses.to_csv('filtered_responses.csv', index=False)
```


## 

## Things to keep in mind:
* #### The API has a limit as to how many requests you can make per day and per second.

    There are several ways to prepare for this including:
    * **Error handling:** Repeat requests that return an error
    * **Throttling:** in your script to lijmit the number of requests sent per second, and re-requesting if a URL fails.
    * Get an [API key](https://developers.google.com/speed/docs/insights/v5/get-started) if necessary (usually if you're making more than one query per second).

____________

Hopefully after reading this guide you're able to get up and running with some basic querying of the Google Page Speed Insights API.

**Source Code:** You can find the GitHub project with an example script to run [here](TODO).

Feel free to reach us on twitter [@ayima](https://twitter.com/ayima) with any questions or if you run into any problems! Thanks for reading!