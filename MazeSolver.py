# MazeSolver.py
from Algorithms.Algorithms import bfs_steps, dfs_steps, dijkstra_steps, a_star_steps

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
        """
        Solve the maze using the selected algorithm.
        Returns a tuple (final_path, steps) where steps is a list of maze snapshots.
        """
        if self.algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        return self.algorithms[self.algorithm](maze, start, end)
