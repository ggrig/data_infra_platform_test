import osmnx as ox
import geopandas as gpd

# Define a large area or multiple areas to increase data size
large_area = "California, USA"

# Fetch the network data; larger network types can fetch more data
# Try 'all' to collect all types of roads, not just drivable ones
graph = ox.graph_from_place(large_area, network_type='drive')

# Convert to Node and Edge DataFrames
nodes, edges = ox.graph_to_gdfs(graph)

# You can already download a large amount of data with this approach.
# To handle and store data efficiently, consider saving in formats like Parquet
edges.to_csv('edges_california.csv', index=False)
nodes.to_csv('nodes_california.csv', index=False)

# If data size needs to be increased:
# - Consider fetching additional layers, points of interest, or amenities
# - Consider repeating for adjacent geographical areas
# - Aggregate multiple downloads to achieve desired volume