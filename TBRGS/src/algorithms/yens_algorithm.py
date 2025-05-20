import networkx as nx
from itertools import islice

def print_top_k_routes_by_travel_time(G, source, target, k=5):
    # if source not in G or target not in G:
    #     print(f"❌ One or both site IDs not found in the graph: {source}, {target}")
    #     return 
    
    if source not in G.nodes or target not in G.nodes:
        print(f"❌ One or both site IDs not found in the graph: {source}, {target}")
        return

    print(f"\n🔍 Finding top {k} fastest SCATS routes from {source} to {target}...\n")

    try:
        routes = islice(nx.shortest_simple_paths(G, source, target, weight='travel_time'), k)

        for idx, path in enumerate(routes, 1):
            # Calculate total travel time for this route
            total_time = 0
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                time = G[a][b]['travel_time']
                total_time += time

            # Print route and time
            route_str = ' → '.join(str(sid) for sid in path)
            print(f"Route {idx}: {route_str}")
            print(f"  ⏱️ Estimated Travel Time: {total_time:.2f} seconds\n")

    except nx.NetworkXNoPath:
        print("❗ No path found between the selected SCATS sites.")