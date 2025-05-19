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
    
    # all_roads_array = pd.concat([data_file['road_1'], data_file['road_2']]).unique()
    
    for index, row in data_file.iterrows():
        
        aSCATS = SCATSNode(row['site_id'], row["road_1"], row["road_2"], row["latitude"], row["longitude"])
        
        # Add the node to the graph
        graph.add_node(aSCATS )
        
    # Add edges to the graph
    # for main_road in all_roads_array:
    #     # Get all nodes that are on a main road
    #     main_road_nodes = data_file[data_file['road_1'] == main_road]
    #     joined_nodes = data_file[data_file['road_2'] == main_road]
        
    #     # Combine the two dataframes
    #     road_nodes = pd.concat([main_road_nodes, joined_nodes])

    #     iter_count = len(road_nodes)-1

    #     # def add_edge(self, from_node, to_node, time_cost):
    #     for i in range (iter_count):
    #         min_distance = 0
    #         if i == 0:
    #             scats = temp_road_nodes.iloc[i]['site_id']
    #             connected_node = None
                
    #         # if ( i == len(road_nodes)-2):
    #         #     temp_road_nodes = road_nodes.copy()
                
    #         for node in temp_road_nodes['site_id']:
    #             if scats == node:
    #                 continue
    #             d = graph.nodes[scats].distance_to(graph.nodes[node])
    #             if d < min_distance or min_distance == 0:
    #                 min_distance = d
    #                 connected_node = node
            
    #         graph.add_edge(scats, connected_node, calculate_travel_time(graph, scats, connected_node, "2006-11-01 00:00"))
    #         graph.add_edge(connected_node, scats, calculate_travel_time(graph, connected_node, scats, "2006-11-01 00:00"))
            
    #         # print(temp_road_nodes['site_id'], end="step\n")
    #         temp_road_nodes.drop(temp_road_nodes[temp_road_nodes['site_id'] == scats].index, inplace=True)
    #         scats = connected_node
    
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
    
    