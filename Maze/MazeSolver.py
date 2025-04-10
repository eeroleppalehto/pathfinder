from Algorithms.AStar import a_star_steps
from Algorithms.BreadthFirstSearch import bfs_steps
from Algorithms.DepthFirstSearch import dfs_steps
from Algorithms.Dijkstra import dijkstra_steps

class MazeSolver:
    def __init__(self, algorithm="BFS"):
        self.algorithm = algorithm
        self.algorithms = {
            "BFS": bfs_steps,
            "DFS": dfs_steps,
            "Dijkstra": dijkstra_steps,
            "A*": a_star_steps
        }

    def solve(self, maze, start, end):
        if self.algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        return self.algorithms[self.algorithm](maze, start, end, snapshot_interval=1)
