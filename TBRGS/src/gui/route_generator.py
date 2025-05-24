import pandas as pd
import osmnx as ox
import networkx as nx
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def plot_route_map(router):
    
    # Define the route SCATS numbers
    try:
        # route_scats = [970, 3685, 2000, 4043] 
        route_scats = router
    except NameError:
        print("❌ Route SCATS numbers not defined.")
        return False
    
    # Load SCATS data
    df = pd.read_csv("TBRGS/data/processed/map_data.csv").dropna(subset=['SCATS Number', 'NB_LATITUDE', 'NB_LONGITUDE'])
    df['SCATS Number'] = df['SCATS Number'].astype(int)
    
    # route_scats = [970, 3685, 2000, 4043] 

    # Center of map
    lat_center = -37.8222815
    lon_center = 145.0657007

    # Main roads only
    main_road_filter = (
        '["highway"~"motorway|trunk|primary|secondary|tertiary|motorway_link|trunk_link|primary_link"]'
    )

    # Download road network
    G = ox.graph_from_point(
        center_point=(lat_center, lon_center),
        dist=5000,
        network_type='drive',
        custom_filter=main_road_filter
    )

    # Map SCATS to nearest OSM nodes
    scats_sites = df[['SCATS Number', 'NB_LATITUDE', 'NB_LONGITUDE']].copy()
    scats_sites['osmid'] = scats_sites.apply(
        lambda row: ox.nearest_nodes(G, row['NB_LONGITUDE'], row['NB_LATITUDE']),
        axis=1
    )

    # Plot road network
    fig, ax = ox.plot_graph(
        G,
        node_size=0,
        edge_color='#cccccc',
        edge_linewidth=1,
        edge_alpha=0.9,
        bgcolor='white',
        show=False,
        close=False
    )

    # Plot SCATS nodes
    for _, row in scats_sites.iterrows():
        x, y = G.nodes[row['osmid']]['x'], G.nodes[row['osmid']]['y']
        ax.plot(x, y, marker='o', color='#88bef5', markersize=6)
        ax.text(x+0.002, y, int(row['SCATS Number']), fontsize=6, color='black')

    # Map SCATS Numbers to OSM node IDs
    scats_dict = dict(zip(scats_sites['SCATS Number'], scats_sites['osmid']))
    route_osm = [scats_dict[s] for s in route_scats if s in scats_dict]
    
    # Draw red route
    for i in range(len(route_osm) - 1):
        try:
            path = nx.shortest_path(G, route_osm[i], route_osm[i+1], weight='length')
            coords = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in path]
            xs, ys = zip(*coords)
            ax.plot(xs, ys, color='#324e7b', linewidth=3, alpha=0.9)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            print(f"⚠️ No path between SCATS {route_scats[i]} and {route_scats[i+1]}")
            continue
    
    return plt 