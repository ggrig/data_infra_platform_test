import osmnx as ox
import geopandas as gpd
import pandas as pd

# List of states to retrieve data for
areas = [
    "New York, New York, USA",
    "LA, CA, USA",
    "SF, CA, USA",
    "Chicago, IL, USA",
    "Houston, TX, USA",
    # "Phoenix, AZ, USA",
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
    print(f"Fetching data for {area_name}")
    try:
        nodes = []
        edges = []
        
        # Fetch the graph data for each state
        graph = ox.graph_from_place(area_name, network_type='all')
        nodes, edges = ox.graph_to_gdfs(graph)

        # Save combined data to CSV files
        nodes.to_csv(transform_string(area_name) + '_nodes.csv', index=False)
        edges.to_csv(transform_string(area_name) + '_edges.csv', index=False)

        print(f"Finished fetching data for {area_name}")
    except Exception as e:
        print(f"An error occurred while fetching data for {area_name}: {e}")

# Iterate over the list of states and fetch data
for area_name in areas:
    fetch_and_append_state_data(area_name)

print("Job completed")