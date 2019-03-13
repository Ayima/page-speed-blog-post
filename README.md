# Getting Started With Google Page Speed Insights API
This contains an example of how to query URLs using Google Page Speed Insights API.
Please read the full blog post [here]().

## To run the scripts:
1. Clone this repository.
    `git clone https://github.com/Ayima/page-speed-blog-post.git`
    
2. Create a CSV file with the URLs you would like to run in this format:

    | URL | device_type |
    ----- | :---------: |
    | www.example_1.com | mobile |
    | www.example_2.com | mobile |

     *Note: This example only takes in `mobile` as a device type*

3. Change the config.json file to reflect your URL file name.
4. Run the script:

    `python main.py --config-file config.json`
    
