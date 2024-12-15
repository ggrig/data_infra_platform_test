# import osmnx as ox
# import geopandas as gpd

# # Define a large area or multiple areas to increase data size
# large_area = "New York, New York, USA"

# # Fetch the network data; larger network types can fetch more data
# # Try 'all' to collect all types of roads, not just drivable ones
# graph = ox.graph_from_place(large_area, network_type='drive')

# # Convert to Node and Edge DataFrames
# nodes, edges = ox.graph_to_gdfs(graph)

# print(edges[:10].to_geo_dict())

# You can already download a large amount of data with this approach.
# To handle and store data efficiently, consider saving in formats like Parquet
# edges.to_csv('edges_california.csv', index=False)
# nodes.to_csv('nodes_california.csv', index=False)

# If data size needs to be increased:
# - Consider fetching additional layers, points of interest, or amenities
# - Consider repeating for adjacent geographical areas
# - Aggregate multiple downloads to achieve desired volume


a = [
    {
        "id": "(39076461, 274283981, 0)",
        "type": "Feature",
        "properties": {
            "osmid": 25161349,
            "highway": "motorway",
            "lanes": "2",
            "maxspeed": "50 mph",
            "name": "Cross Island Parkway",
            "oneway": True,
            "ref": "CI",
            "reversed": False,
            "length": 819.5016661477803,
            "bridge": None,
            "access": None,
            "tunnel": None,
            "width": None,
            "junction": None,
            "est_width": None,
        },
        "geometry": {
            "type": "LineString",
            "coordinates": (
                (-73.7947484, 40.7863451),
                (-73.794615, 40.7863898),
                (-73.7944856, 40.7864343),
                (-73.7943563, 40.7864809),
                (-73.7942289, 40.7865266),
                (-73.7940993, 40.7865739),
                (-73.7939726, 40.7866211),
                (-73.7938448, 40.786671),
                (-73.7937196, 40.7867213),
                (-73.793594, 40.7867723),
                (-73.793465, 40.7868253),
                (-73.7933444, 40.7868769),
                (-73.7932188, 40.7869306),
                (-73.7930954, 40.786984),
                (-73.7929753, 40.7870377),
                (-73.7928501, 40.7870933),
                (-73.7927279, 40.7871496),
                (-73.7926059, 40.7872061),
                (-73.7909163, 40.7880014),
                (-73.790792, 40.7880566),
                (-73.7906687, 40.7881112),
                (-73.7905452, 40.788166),
                (-73.7904232, 40.7882185),
                (-73.7903022, 40.7882687),
                (-73.7901731, 40.788322),
                (-73.7900483, 40.7883727),
                (-73.7899209, 40.7884227),
                (-73.7897938, 40.7884715),
                (-73.7896694, 40.7885183),
                (-73.7895408, 40.7885667),
                (-73.7894104, 40.7886139),
                (-73.7892832, 40.7886587),
                (-73.7891563, 40.7887019),
                (-73.7890238, 40.7887451),
                (-73.7888912, 40.788787),
                (-73.7887632, 40.7888264),
                (-73.7886299, 40.7888655),
                (-73.7884982, 40.788904),
                (-73.7883607, 40.7889423),
                (-73.7882291, 40.7889779),
                (-73.7880942, 40.7890128),
                (-73.7879575, 40.7890464),
                (-73.7878231, 40.7890787),
                (-73.7876873, 40.7891097),
                (-73.7875503, 40.7891395),
                (-73.7874134, 40.7891683),
                (-73.7872765, 40.789195),
                (-73.78714, 40.7892213),
                (-73.7870025, 40.7892452),
                (-73.7868924, 40.7892625),
                (-73.7867858, 40.7892791),
                (-73.7866664, 40.7892952),
                (-73.7865266, 40.7893131),
                (-73.7863885, 40.7893301),
                (-73.7862474, 40.7893469),
                (-73.7861069, 40.7893617),
                (-73.7859633, 40.7893759),
            ),
        },
    },
    {
        "id": "(39076461, 42854803, 0)",
        "type": "Feature",
        "properties": {
            "osmid": 25161578,
            "highway": "motorway_link",
            "lanes": None,
            "maxspeed": None,
            "name": None,
            "oneway": True,
            "ref": None,
            "reversed": False,
            "length": 268.1440952459794,
            "bridge": None,
            "access": None,
            "tunnel": None,
            "width": None,
            "junction": None,
            "est_width": None,
        },
        "geometry": {
            "type": "LineString",
            "coordinates": (
                (-73.7947484, 40.7863451),
                (-73.7933159, 40.7867884),
                (-73.7931917, 40.7868285),
                (-73.7930816, 40.7868672),
                (-73.792978, 40.7869061),
                (-73.7928878, 40.7869409),
                (-73.7928086, 40.7869726),
                (-73.7927378, 40.7870027),
                (-73.7926698, 40.7870305),
                (-73.7921607, 40.7872621),
                (-73.7921252, 40.7872747),
                (-73.7920916, 40.7872822),
                (-73.7920535, 40.7872824),
                (-73.7920208, 40.7872736),
                (-73.791997, 40.7872539),
                (-73.7919229, 40.7871641),
            ),
        },
    }
]

row = {}
row['osmid']    = a[0]['properties']['osmid']
row['highway']  = a[0]['properties']['highway']
row['maxspeed'] = a[0]['properties']['maxspeed']
row['name']     = a[0]['properties']['name']
row['oneway']   = a[0]['properties']['oneway']
row['reversed'] = a[0]['properties']['reversed']
row['length']   = a[0]['properties']['length']
row['geometry'] = a[0]['geometry']['coordinates']
row['lanes']    = a[0]['properties']['lanes']
row['ref']      = a[0]['properties']['ref']
row['access']   = a[0]['properties']['access']
row['bridge']   = a[0]['properties']['bridge']
row['tunnel']   = a[0]['properties']['tunnel']
row['width']    = a[0]['properties']['width']
row['junction'] = a[0]['properties']['junction']
print(row)