import sys

from algorithms.yens_algorithm import print_top_k_routes_by_travel_time
from data_processing import process_scats_data

REQUIRED_PYTHON_VERSION = (3, 11, 11)
current_version = sys.version_info[:3]

def main():
    if current_version != REQUIRED_PYTHON_VERSION:
        print("❌ This program requires Python 3.11.11")
        print(f"You are using Python {'.'.join(map(str, current_version))}")
        sys.exit(1)
    else:
        print(f"✅ Runing Python version : {current_version[0]}.{current_version[1]}.{current_version[2]}")
        
    # Make the main graph object
    SCAT_Graph = process_scats_data()
    # Print the graph
    SCAT_Graph.print_graph()
    
    print_top_k_routes_by_travel_time(SCAT_Graph, 970, 2000, k=5)
    
        
if __name__ == "__main__":
    main()