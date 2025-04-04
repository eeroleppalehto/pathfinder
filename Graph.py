class Graph:
    """
        The graph is represetented as a dictionary 
        where the values for the keys are list of tuples

        See example:

        graph = {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("C", 3)],
            "C": [("A", 2), ("B", 3)],
        }
    """
    
    def __init__(self):
        self.graph: dict[str, list[tuple[str, int]]] = {}

    def add_vertix(self, key):...

    def add_edge(self, vertex_1, vertex_2):...

    def get_vertices(self)->list[str]:
        return list(self.graph.keys())

    def create_graph_from_source(self):...


if __name__ == "__main__":
    pass
