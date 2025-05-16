import pandas as pd
import numpy as np

from graph import RoadGraph, SCATSNode

class SearchObject:
    def __init__(self, graph, origin_id, destination_id, timestamp):
        self.graph = graph
        self.origin = origin_id
        self.destination = destination_id
        self.timestamp = timestamp

def process_scats_data():
    # Generate SCATS data
    file_path = "TBRGS/data/processed/scats_data.csv"
    data_file = pd.read_csv(file_path)
    
    graph = RoadGraph()
    
    for index, row in data_file.iterrows():
        
        aSCATS = SCATSNode(row['site_id'], row["road_1"], row["road_2"], row["latitude"], row["longitude"])
        
        # Add the node to the graph
        graph.add_node(aSCATS)
        
        # Add edges to the graph
        
        

        
        
        
        
        
        # Assuming the data is in the format: site_id, site_location, site_latitude, site_longitude
        
        
        # parts = line.split(',')
        # site_id = parts[0]
        # site_location = parts[1]
        # site_latitude = float(parts[2])
        # site_longitude = float(parts[3])
        
        # node = SCATSNode(site_id, site_location, site_latitude, site_longitude)
        # graph.add_node(node)
    
    
    
    return graph


if __name__ == "__main__":
    # Test the process_scats_data function
    graph = process_scats_data()
    
    print("Graph nodes:")
    print(graph.nodes[970])
    
    