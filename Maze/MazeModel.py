from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MazeGenerator import MazeGenerator

class MazeModel:
    """
    This class is responsible for storing all relevant data relating to mazes and
    their algorithms.
    It contains the original maze, the current maze, and the steps taken by the algorithm.
    It also provides methods to generate new mazes, run algorithms, and display steps.

    Mazes are matrices where 
    walls are represented as 1,
    empty spaces by 0,
    start cell by 'S',
    and end cell by 'E'.
    """
    def __init__(self, maze_generator: MazeGenerator, maze_width=200, maze_height=200, seed=0):
        # Use the provided MazeGenerator instance to generate the maze.
        self.maze_generator = maze_generator
        self.maze = self.maze_generator.generate(maze_width, maze_height, seed)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.start, self.end = self.get_start_end()
        self.steps = []
        self.current_step = -1
        self.last_step = -1

    def generate_new_maze(self, maze_width, maze_height, seed=0):
        """
        Generate a new maze with the specified width, height, and seed.

        Args:
            maze_width (int): The width of the maze.
            maze_height (int): The height of the maze.
            seed (int, optional): The seed for random generation. Defaults to 0.
        """
        self.maze = self.maze_generator.generate(maze_width, maze_height, seed)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.start, self.end = self.get_start_end()
        self.steps = []
        self.current_step = -1
        self.last_step = -1

    def get_start_end(self):
        start = end = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == 'S':
                    start = (i, j)
                elif self.maze[i][j] == 'E':
                    end = (i, j)
        return start, end
    
    def get_final_path_length(self):
        return len(self.steps[-1])

    def run_algorithm(self, solver_factory, algorithm_name):
        """
        Run the specified algorithm to solve the maze.

        Args:
            solver_factory (Callable): A factory function to create a solver instance.
            algorithm_name (str): The name of the algorithm to use for solving.
        """
        solver = solver_factory(algorithm_name)
        start, end = self.get_start_end()
        if not start or not end:
            print("Start or end position not found!")
            return

        self.steps = []
        self.current_step = -1
        self.last_step = -1

        _, raw_steps = solver.solve(self.maze, start, end)

        # Some algorithms might return a single long list. Standardize it.
        if len(raw_steps) == 1 and len(raw_steps[0]) > 1:
            subdivided = [[update] for update in raw_steps[0]]
            self.steps = subdivided
        else:
            self.steps = raw_steps
        
        self.display_step(-1)

    def reset_maze_to_original(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] not in (1, 'S', 'E'):
                    self.maze[i][j] = 0
        self.current_step = -1
        self.last_step = -1
        
    
    def remove_previous_steps(self, step_ix, step_ix_end):
        """Method to remove previous steps from the current maze.

        Args:
            step_ix (int): The index of the first step to remove.
            step_ix_end (int): The index of the last step to remove.
        """

        # Check if the current step is the found path and mark it as visited.
        if self.steps[self.current_step][0][2] == 'P':
            for (x, y, _) in self.steps[self.current_step]:
                self.maze[x][y] = 'V'
            step_ix_end -= 1

        # Iterate through the specified steps and erase them from the current maze.
        for i in range(step_ix, step_ix_end):
            for (x, y, _) in self.steps[i]:
                self.maze[x][y] = 0

    def display_step(self, step_idx):
        """
        Display the maze at a specific step index.
        This method updates the current maze to reflect the state at the given step index.
        It handles both forward and backward navigation through the steps.

        Args:
            step_idx (int): The index of the step to display.
        """
        if step_idx < -1 or step_idx >= len(self.steps):
            return

        if step_idx < self.last_step:
            self.remove_previous_steps(step_idx, self.last_step)
        else:
            # Apply steps incrementally.
            for i in range(self.last_step + 1, step_idx + 1):
                for (x, y, val) in self.steps[i]:
                    self.maze[x][y] = val
        # Update step states
        self.last_step = step_idx
        self.current_step = step_idx
