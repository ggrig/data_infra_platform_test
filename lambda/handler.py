import logging
logger = logging.getLogger(__name__)


from BuchungWriter import BuchungWriter
import osmnx as ox
import geopandas as gpd
import pandas as pd

import logging
logger = logging.getLogger(__name__)

# List of states to retrieve data for
areas = [
    # "New York, New York, USA",
    # "LA, CA, USA",
    "SF, CA, USA",
    # "Chicago, IL, USA",
    # "Houston, TX, USA",
    # "Philadelphia[d], PA, USA",
    # "San Antonio, TX, USA",
    # "San Diego, CA, USA",
    # "Dallas, TX, USA",
    # "Jacksonville[e, FL, USA",
    # "Austin, TX, USA",
    # "Fort Worth, TX, USA",
    # "San Jose, CA, USA",
    # "Seattle, WA, USA",
    # Add more states as needed
]


def transform_string(original_string):
    # Remove commas and replace spaces with underscores
    result_string = original_string.replace(',', '').replace(' ', '_')
    return result_string


# Function to fetch and append data for each state
def fetch_and_append_state_data(area_name):
    logger.info(f"Fetching data for {area_name}")
    nodes = []
    edges = []
    try:

        
        # Fetch the graph data for each state
        graph = ox.graph_from_place(area_name, network_type='drive')
        nodes, edges = ox.graph_to_gdfs(graph)

        # Save combined data to CSV files
        # nodes.to_csv(transform_string(area_name) + '_nodes.csv', index=False)
        # edges.to_csv(transform_string(area_name) + '_edges.csv', index=False)

        logger.info(f"Finished fetching data for {area_name}")

    except Exception as e:
        logger.error(f"An error occurred while fetching data for {area_name}: {e}")
    
    return edges

STEP = 100

def dataset_handler(event, context):
    logging.basicConfig(
        filename='log-main.log', 
        # encoding='utf-8', 
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Iterate over the list of states and fetch data
    for area_name in areas:
        data = fetch_and_append_state_data(area_name).to_geo_dict()['features']
        logger.info(f'data length = {len(data)}')
        x = 0
        awq = BuchungWriter(context='')
        while x+STEP < len(data):
            logger.info(awq.run(data[x:x+STEP]))
            x += STEP
            # logger.info('\n\n\n-------------------------------------------------------\n\n\n')
            logger.info(f"{x}")

    logger.info("Job completed")

    # return ret_error("The handler not implemented")
    

import json
import urllib3

def handler(event, context):
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', 'https://api.ipify.org?format=json')
        status_code = response.status
        if status_code == 200:
            result = json.loads(response.data.decode('utf-8'))
            return {
                'statusCode': status_code,
                'body': json.dumps({
                    'message': 'Lambda has internet access.',
                    'public_ip': result['ip']
                })
            }
        else:
            return {
                'statusCode': status_code,
                'body': json.dumps('Failed to access the internet.')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Exception: {str(e)}')
        }
