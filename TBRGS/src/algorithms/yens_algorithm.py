import networkx as nx
from itertools import islice

import heapq

def find_k_shortest_routes(graph, start_id, end_id, k=5):
    if start_id not in graph.nodes or end_id not in graph.nodes:
        print("Invalid node IDs.")
        return []

    # Each path: (total_cost, [path_nodes])
    paths_found = []
    queue = [(0, [start_id])]  # min-heap priority queue: (cost, path)

    visited_paths = set()

    while queue and len(paths_found) < k:
        cost, path = heapq.heappop(queue)
        last_node = path[-1]

        # If path ends at destination and is unique, store it
        if last_node == end_id and tuple(path) not in visited_paths:
            paths_found.append((cost, path))
            visited_paths.add(tuple(path))
            continue

        if last_node in graph.edges:
            for neighbor_id, edge_cost in graph.edges[last_node]:
                if neighbor_id not in path:  # Avoid cycles
                    new_path = path + [neighbor_id]
                    new_cost = float(cost) + float(edge_cost)
                    heapq.heappush(queue, (new_cost, new_path))

    return paths_found
