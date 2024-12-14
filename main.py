import osmnx as ox
import geopandas as gpd
import pandas as pd

# List of states to retrieve data for
states = [
    "California, USA",
    "Texas, USA",
    "Florida, USA",
    # Add more states as needed
]

# Initialize lists to hold DataFrames
all_nodes = []
all_edges = []

# Function to fetch and append data for each state
def fetch_and_append_state_data(state_name):
    print(f"Fetching data for {state_name}")
    try:
        # Fetch the graph data for each state
        graph = ox.graph_from_place(state_name, network_type='drive')
        nodes, edges = ox.graph_to_gdfs(graph)
        
        # Append DataFrames to the lists
        all_nodes.append(nodes)
        all_edges.append(edges)

        print(f"Finished fetching data for {state_name}")
    except Exception as e:
        print(f"An error occurred while fetching data for {state_name}: {e}")

# Iterate over the list of states and fetch data
for state in states:
    fetch_and_append_state_data(state)

# Concatenate all DataFrames into one
combined_nodes = pd.concat(all_nodes, ignore_index=True)
combined_edges = pd.concat(all_edges, ignore_index=True)

# Save combined data to CSV files
combined_nodes.to_csv('all_states_nodes.csv', index=False)
combined_edges.to_csv('all_states_edges.csv', index=False)

print("Data from all states saved to all_states_nodes.csv and all_states_edges.csv")