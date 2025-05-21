import sys

from gui.route_generator import plot_route_map
from algorithms.yens_algorithm import find_k_shortest_routes
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
    
    paths = find_k_shortest_routes(SCAT_Graph, 2200, 3804, k=5)
    
    plots = []
    
    # print(paths, "\n")
    for path in paths:
        print(path[0], ":", path[1])
        print("Total cost:", path[0])
        print("Path:", " -> ".join(map(str, path[1])))
        print()
        plots.append(plot_route_map(path[1]))
        
    for plot in plots:
        plot.show()
    
    # dashboard_interface()
    
        
if __name__ == "__main__":
    main()