# Source https://www.cs.helsinki.fi/u/ahslaaks/tirakirja/
# https://tira.mooc.fi/kevat-2025/kaikki2/
from Graph import Graph
from Action import ActionDA
import heapq

def dijkstra(graph: Graph, source):
    """A pathfinder algorithm that finds the shortest paths to
    each vertex in the graph from the source vertex.

    Args:
        graph (Graph): The graph for which the algorithm operates on
        source (Any): The starting vertex

    Returns:
        dict[Any,float]: Output is given as dictionary where the keys are the verteces
        and values are the shortest distance to them from the starting vertex.
    """

    # Dictionary of where the key is the vertex and 
    # value is the distance to it from the source vertex.
    # On initialization all values are set to infinity
    shortest_paths = {vertex: float('inf') for vertex in graph.get_vertices()}
    processed_verteces = []

    # Initialize a heap to queue items
    heap = []
    heapq.heappush(heap, (0, source))
    
    # Set path to source to 0
    shortest_paths[source] = 0
    while len(heap) != 0:
        vertex = heapq.heappop(heap)[1]

        if vertex in processed_verteces:
            continue
        processed_verteces.append(vertex)

        for edge in graph.get_edge_list(vertex):

            current_length = shortest_paths[edge[0]]
            new_length = shortest_paths[vertex] + edge[1]

            if new_length < current_length:
                shortest_paths[edge[0]] = new_length
                heapq.heappush(heap,(new_length,edge[0]))
    
    return shortest_paths

def dijkstra_actions(graph: Graph, source):
    """This algorithm tells what dijkstra's algorithm traverses the graph and updates the shortest paths.

    Args:
        graph (Graph): The graph for which the algorithm operates on.
        source (Any): The starting vertex.

    Returns:
        list[ActionDA]: List of ActionDA objects.
    """
    actions: list[ActionDA] = []
    
    shortest_paths = {vertex: float('inf') for vertex in graph.get_vertices()}
    processed_verteces = []

    # Initialize a heap to queue items
    heap = []
    heapq.heappush(heap, (0, source))
    
    # Set path to source to 0
    shortest_paths[source] = 0
    while len(heap) != 0:
        vertex = heapq.heappop(heap)[1]

        if vertex in processed_verteces:
            continue
        processed_verteces.append(vertex)

        for edge in graph.get_edge_list(vertex):
            action = ActionDA(vertex, edge[0])
            current_length = shortest_paths[edge[0]]
            new_length = shortest_paths[vertex] + edge[1]

            if new_length < current_length:
                action.update_path_length(new_length, current_length)
                shortest_paths[edge[0]] = new_length
                heapq.heappush(heap,(new_length,edge[0]))
            actions.append(action)
    
    return actions

if __name__ == "__main__":
    graph = Graph()

    # A----3----B
    # | \2    1/|
    # |  \   /  |
    # 5    E    6
    # | 2/   \3 |
    # | /     \ |
    # C----4----D

    graph.graph = {
        "A": [("B", 3), ("C", 5), ("E", 2)],
        "B": [("A", 3), ("D", 6), ("E", 1)],
        "C": [("A", 5), ("D", 4), ("E", 2)],
        "D": [("B", 6), ("C", 4), ("E", 3)],
        "E": [("A", 2), ("B", 1), ("C", 2), ("D", 3) ],
    }

    paths = dijkstra(graph, "A")
    for v in list(paths.keys()):
        print(f"{v}: {paths[v]}")


    def update_string(action: ActionDA):
        if action.new_path_length != float('inf'):
            return f" and update distance to said vertex from {action.previous_length} to {action.new_path_length}"
        return ""

    print("\n----------------------\n")

    actions = dijkstra_actions(graph, "A")
    for action in actions:
        print(f"Check from vertex {action.edge_start} the distance to vertex {action.edge_end}{update_string(action)}")