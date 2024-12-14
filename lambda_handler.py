import osmnx as ox
import pandas as pd

def get_data(place_name):

    # Download the street network data as a graph
    graph = ox.graph_from_place(place_name, network_type='drive')

    # Convert the graph into Node and Edge DataFrames
    nodes, edges = ox.graph_to_gdfs(graph)

    # Save nodes and edges to CSV files
    nodes.to_csv('nodes.csv', index=False)
    edges.to_csv('edges.csv', index=False)

    print("Data successfully saved to nodes.csv and edges.csv")

if __name__ == '__main__':

    # Specify the location you are interested in
    place_name = "Manhattan, New York City, New York, USA"

    get_data(place_name)