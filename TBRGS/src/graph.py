# This file contains the classes for SCATS Site Nodes and SCATS Links.
# -------------------------------------------------------

print("Loading graph.py...")
import pandas as pd
import numpy as np
from geopy.distance import geodesic

# The SCATS Site Node class
class SCATSNode:
    def __init__(self, site_id, road_1, road_2, site_latitude, site_longitude ):
        self.id = site_id
        self.road_1 = road_1
        self.road_2 = road_2
        self.latitude = site_latitude
        self.longitude = site_longitude
        self.neighbors = []
        
    def add_neighbor(self, neighbor_node):
        if(len(self.neighbors) >= 5):
            print(f"Node {self.id} already has 4 neighbors.")
            return
        else:
            self.neighbors.append(neighbor_node)

    def __repr__(self):
        return f"SCATSNode({self.id}, {self.road_1}, {self.road_2}, {self.latitude}, {self.longitude})"
    
    def distance_to(self, other):
        self_lat = float(self.latitude)
        self_long = float(self.longitude)
        other_lat = float(other.latitude)
        other_long = float(other.longitude)
        
        coord1 = (self_lat, self_long)
        coord2 = (other_lat, other_long)
        
        # Calculate the distance using geopy
        return geodesic(coord1, coord2).kilometers
     
    
# The SCATS Link class
class RoadGraph:
    # Create a graph with nodes and edges
    def __init__(self):
        self.nodes = {} 
        self.edges = {}
        
    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
        else:
            print(f"Node {node.id} already exists.")
            
    # Add a directed edge to the graph
    def add_edge(self, from_node, to_node, time_cost):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, time_cost))
        self.nodes[from_node].add_neighbor(to_node)
    
    # Print the graph (NODES + EDGES)
    def print_graph(self):
        print("SCATS:")
        for node_id, node in self.nodes.items():
            print(f"  SCATS {node_id}: {node.road_1} <-> {node.road_2} (Lat: {node.latitude}, Long: {node.longitude})")
        
        print("\nConnections:")
        for from_node, neighbors in self.edges.items():
            for (to_node, cost) in neighbors:
                print(f"  {from_node} -> {to_node} (time_cost: {cost})")
