import pandas as pd
import numpy as np
from models.LSTM_model import LSTM_prediction
from graph import RoadGraph, SCATSNode
from data_processing import process_scats_data

def calculate_travel_time(graph, origin_id, destination_id, timestamp):
    # Get the origin and destination nodes
    origin_node = graph.nodes[int(origin_id)]
    destination_node = graph.nodes[int(destination_id)]

    # Calculate the distance between the two nodes
    distance = origin_node.distance_to(destination_node)
    
    flow = LSTM_prediction(destination_id, timestamp)
    # flow = 0
    
    if flow is None:
        print("Flow data is not available.")
        return None
    
    if flow > 351:
        # Calculate the speed using the quadratic formula
        a = -1.4648375
        b = 93.75
        c = -flow

        # Calculate the discriminant
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            print("No real roots, speed cannot be calculated.")
            return None

        # Calculate the two possible speeds
        speed1 = (-b + np.sqrt(discriminant)) / (2*a)
        speed2 = (-b - np.sqrt(discriminant)) / (2*a)

        # Choose the positive speed
        speed = max(speed1, speed2)
    else:
        # If flow is less than or equal to 351, use a constant speed
        speed = 60.0
        
    # Calculate the travel time in minutes
    travel_time = ((distance / speed) + 30 ) * 60  # Convert to minutes
    
    print(f"Travel time from {origin_id} to {destination_id} at {timestamp}: {travel_time:.2f} minutes")

    return travel_time


# if __name__ =="__main__":
#     calculate_travel_time(process_scats_data(), "2000", "2200", "2006-11-01 00:00")
    