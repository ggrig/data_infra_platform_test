from BuchungWriter import BuchungWriter
import osmnx as ox
import geopandas as gpd
import pandas as pd

import logging
logger = logging.getLogger(__name__)

# List of states to retrieve data for
areas = [
    "New York, New York, USA",
    "LA, CA, USA",
    # "SF, CA, USA",
    "Chicago, IL, USA",
    "Houston, TX, USA",
    "Philadelphia[d], PA, USA",
    "San Antonio, TX, USA",
    "San Diego, CA, USA",
    "Dallas, TX, USA",
    "Jacksonville[e, FL, USA",
    "Austin, TX, USA",
    "Fort Worth, TX, USA",
    "San Jose, CA, USA",
    "Seattle, WA, USA",
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
        data = fetch_and_append_state_data(area_name)#.to_geo_dict()['features']
        # data = data.iloc[:500]
        # logger.info(f'\n{data}')
        # logger.info(f'osmid = {data.iloc[0]['osmid']}')
        # logger.info(f'highway = {data.iloc[0]['highway']}')
        # logger.info(f'maxspeed = {data.iloc[0]['maxspeed']}')
        # logger.info(f'name = {data.iloc[0]['name']}')
        # logger.info(f'oneway = {data.iloc[0]['oneway']}')
        # logger.info(f'reversed = {data.iloc[0]['reversed']}')
        # logger.info(f'length = {data.iloc[0]['length']}')
        # logger.info(f'geometry = {data.iloc[0]['geometry']}')
        # logger.info(f'lanes = {data.iloc[0]['lanes']}')
        # logger.info(f'ref = {data.iloc[0]['ref']}')
        # logger.info(f'access = {data.iloc[0]['access']}')
        # logger.info(f'bridge = {data.iloc[0]['bridge']}')
        # logger.info(f'tunnel = {data.iloc[0]['tunnel']}')
        # logger.info(f'width = {data.iloc[0]['width']}')
        # logger.info(f'junction = {data.iloc[0]['junction']}')
        # awq = BuchungWriter(context='')
        # print(awq.run(data.iloc[:50]))
        logger.info(f'data length = {len(data)}')
        x = 0
        y = 0
        awq = BuchungWriter(context='')
        while y < len(data):
            y += 50
            print(awq.run(data.iloc[x:y]))
            x += 50
            logger.info('\n\n\n-------------------------------------------------------\n\n\n')

    logger.info("Job completed")