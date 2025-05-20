import pandas as pd
import numpy as np

from travel_time_estimator import calculate_travel_time
from graph import RoadGraph, SCATSNode

class SearchObject:
    def __init__(self, graph, origin_id, destination_id, timestamp):
        self.graph = graph
        self.origin = origin_id
        self.destination = destination_id
        self.timestamp = timestamp
        
class EdgeClass:
    def __init__(self, from_node, to_node, time_cost):
        self.from_node = from_node
        self.to_node = to_node
        self.time_cost = time_cost
        
    def __repr__(self):
        return f"Edge({self.from_node}, {self.to_node}, {self.time_cost})"
    

def process_scats_data():
    # Generate SCATS data
    file_path = "TBRGS/data/processed/scats_data.csv"
    edge_path = "TBRGS/data/processed/scats_edges.csv"
    
    data_file = pd.read_csv(file_path)
    edges = pd.read_csv(edge_path)
    
    graph = RoadGraph()
    
    for _, row in data_file.iterrows():
        
        aSCATS = SCATSNode(row['site_id'], row["road_1"], row["road_2"], row["latitude"], row["longitude"])
        
        # Add the node to the graph
        graph.add_node(aSCATS )
        
    # Add edges to the graph
    for index, row in edges.iterrows():      
        from_node = row['site_id']
        to_nodes = row.iloc[1:].dropna().tolist()
        for to_node in to_nodes:
            graph.add_edge(from_node, to_node, calculate_travel_time(graph, from_node, to_node, "2006-11-01 00:00"))
        
    return graph


# if __name__ == "__main__":
#     # Test the process_scats_data function
#     graph = process_scats_data()
#     graph.print_graph()
    
    