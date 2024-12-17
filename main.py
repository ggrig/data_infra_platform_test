from BuchungWriter import BuchungWriter
import osmnx as ox
import geopandas as gpd
import pandas as pd
# import threading
from multiprocessing import Pool

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
        graph = ox.graph_from_place(area_name, network_type='all')
        nodes, edges = ox.graph_to_gdfs(graph)

        # Save combined data to CSV files
        # nodes.to_csv(transform_string(area_name) + '_nodes.csv', index=False)
        # edges.to_csv(transform_string(area_name) + '_edges.csv', index=False)

        logger.info(f"Finished fetching data for {area_name}")


    except Exception as e:
        logger.error(f"An error occurred while fetching data for {area_name}: {e}")

    logger.info(f"{len(edges)}")
    return edges

# def open_new_thread(awq, data):
#     # awq = BuchungWriter(context='')
#     t = threading.Thread(target=awq.run, args=(data,))
#     t.start()
#     return t

def f(data):
    awq = BuchungWriter(context='')
    awq.run(data)

if __name__ == '__main__':
    logging.basicConfig(
        filename='log-main_fv.log', 
        # encoding='utf-8', 
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Iterate over the list of states and fetch data
    for area_name in areas:
        data = fetch_and_append_state_data(area_name)
        logger.info(f'data length = {len(data)}')
        i = 0
        awq = BuchungWriter(context='')
        
# - - - - - - - - - -

        # while i < len(data):
        #     print(awq.run(data.iloc[i:i+50]))
        #     i += 50
            
# - - - - - - - - - -
            
        # threads = []
        # while i < 5000:
        #     t = open_new_thread(awq, data.iloc[i:i+50])
        #     logger.info('thread open')
        #     threads.append(t)
        #     i += 50
        
        # for t in threads:
        #     t.join()
        #     logger.info('thread close')
            
# - - - - - - - - - -
        
        with Pool(processes=3) as pool:
            values = [data.iloc[0:50], data.iloc[50:100], data.iloc[100:150], data.iloc[150:200], data.iloc[200:250], data.iloc[250:300]]
            results = pool.map(f, values)
            print(results)

    logger.info("Job completed")