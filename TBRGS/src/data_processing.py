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
        
    return graph

def process_scats_edges(graph, day, time, model):
    
    edges = pd.read_csv("TBRGS/data/processed/scats_edges.csv")
    
    if ( len(graph.edges) != 0 ):
        graph.remove_all_edges()
        
    # Validate day and time
    day_to_date = {
        "Monday": "2006-11-01",
        "Tuesday": "2006-11-01",
        "Wednesday": "2006-11-01",
        "Thursday": "2006-11-01",
        "Friday": "2006-11-01",
        "Saturday": "2006-11-01",
        "Sunday": "2006-11-01"  
    }
        
    if day not in day_to_date:
        return "❌ Invalid day"

    # Combine date and time, add seconds
    timestamp  = f"{day_to_date[day]} {time}:00"
    
    print(f"Processing edges for {day} at {time} using model {model} with timestamp {timestamp}")
    # exit()
    
    # Add edges to the graph
    for index, row in edges.iterrows():      
        from_node = row['site_id']
        to_nodes = row.iloc[1:].dropna().tolist() 
        for to_node in to_nodes:
            graph.add_edge(from_node, to_node, calculate_travel_time(graph, from_node, to_node, timestamp, model))
    
    final_graph = RoadGraph()
    final_graph.nodes = graph.nodes
    final_graph.edges = graph.edges
    
    return final_graph
    
    # return graph


# if __name__ == "__main__":
#     # Test the process_scats_data function
#     graph = process_scats_data()
#     graph.print_graph()
    
    