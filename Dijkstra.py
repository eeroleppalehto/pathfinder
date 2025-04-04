# Source https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php
from Graph import Graph
import heapq

def dijkstra(graph: Graph, start):
    # Priority queue to store (distance, vertex) pairs
    priority_queue = [(0, start)]
    # Dictionary to store the shortest path to each vertex
    shortest_paths = {vertex: float('inf') for vertex in graph}
    shortest_paths[start] = 0

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # If the distance is greater than the recorded shortest path, skip it
        if current_distance > shortest_paths[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths

def dijkstra(graph, start):
    # Priority queue to store (distance, vertex) pairs
    priority_queue = [(0, start)]
    # Dictionary to store the shortest path to each vertex
    shortest_paths = {vertex: float('inf') for vertex in graph}
    shortest_paths[start] = 0

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # If the distance is greater than the recorded shortest path, skip it
        if current_distance > shortest_paths[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths

if __name__ == "__main__":
    pass