# This file contains the classes for SCATS Site Nodes and SCATS Links.
# -------------------------------------------------------

print("Loading graph.py...")
import pandas as pd
import numpy as np
from geopy.distance import geodesic

# The SCATS Site Node class
class SCATSNode:
    def __init__(self, site_id, site_location, site_latitude, site_longitude):
        self.id = site_id
        self.location = site_location
        self.latitude = site_latitude
        self.longitude = site_longitude

    def __repr__(self):
        return f"SCATSNode({self.id}, {self.location}, {self.latitude}, {self.longitude})"
    
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
class SCATSLink:
    # Create a graph with nodes and edges
    def __init__(self):
        self.nodes = {} 
        self.edges = {}
        
    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
        else:
            print(f"Node {node.id} already exists.")
        