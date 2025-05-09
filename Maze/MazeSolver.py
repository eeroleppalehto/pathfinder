from Algorithms.AStar import a_star_steps, set_heuristic_weight
from Algorithms.BreadthFirstSearch import bfs_steps
from Algorithms.DepthFirstSearch import dfs_steps
from Algorithms.Dijkstra import dijkstra_steps

class MazeSolver:
    """
    A class to solve mazes using different algorithms.
    """
    def __init__(self, algorithm="BFS"):
        """
        Initializes the MazeSolver with a specified algorithm.
        Args:
            algorithm (str, optional): The algorithm to use for solving the maze. Defaults to "BFS".
        """
        self.algorithm = algorithm
        self.algorithms = {
            "BFS": bfs_steps,
            "DFS": dfs_steps,
            "Dijkstra": dijkstra_steps,
            "A*": a_star_steps
        }

    def set_heuristic_weight(weight: float):
        set_heuristic_weight(weight)

    def solve(self, maze, start, end):
        if self.algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        
        if(self.algorithm == "A*"):
            return self.algorithms[self.algorithm](maze, start, end, 1)
        else:
            return self.algorithms[self.algorithm](maze, start, end, 1)
