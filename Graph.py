class Graph:
    """
        This graph is undirected.
    
        The graph is represetented as a dictionary 
        where the values for the keys are list of tuples

        Example of the stored dictionary:

        graph = {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("C", 3)],
            "C": [("A", 2), ("B", 3)],
        }
    """
    
    def __init__(self):
        self.graph: dict[str, list[tuple[str, int]]] = {}

    def add_vertix(self, key):
        if self.graph.get(key) == None:
            self.graph[key] = []

    def add_edge(self, vertex_1, vertex_2, weight: int):
        self.graph[vertex_1].append((vertex_2, weight))
        self.graph[vertex_2].append((vertex_1, weight))

    def get_vertices(self)->list[str]:
        return list(self.graph.keys())
    
    def get_edge_list(self, vertix) -> list[list[tuple[str, int]]]:
        return self.graph[vertix]
    
    def get_edge_dict(self, vertix) -> dict[str, int]:
        edge_list = self.get_edge_list(vertix)
        edge_dict = {}

        for edge in edge_list:
            edge_dict[edge[0]] = edge[1]

        return edge_dict


    def create_graph_from_source(self):...



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

    print(graph.get_edge_dict("A"))
