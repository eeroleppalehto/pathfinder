import copy

class MazeModel:
    def __init__(self, maze_generator, maze_width=200, maze_height=200, seed=0):
        # Use the provided MazeGenerator instance to generate the maze.
        self.maze_generator = maze_generator
        self.original_maze = self.maze_generator.generate(maze_width, maze_height, seed)
        self.rows = len(self.original_maze)
        self.cols = len(self.original_maze[0])
        self.current_maze = copy.deepcopy(self.original_maze)
        self.steps = []
        self.current_step = -1
        self.last_step = -1

    def get_start_end(self):
        start = end = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.original_maze[i][j] == 'S':
                    start = (i, j)
                elif self.original_maze[i][j] == 'E':
                    end = (i, j)
        return start, end

    def run_algorithm(self, solver_factory, algorithm_name):
        solver = solver_factory(algorithm_name)
        start, end = self.get_start_end()
        if not start or not end:
            print("Start or end position not found!")
            return

        self.current_maze = copy.deepcopy(self.original_maze)
        self.steps = []
        self.current_step = -1
        self.last_step = -1

        _, raw_steps = solver.solve(copy.deepcopy(self.original_maze), start, end)

        # Some algorithms might return a single long list. Standardize it.
        if len(raw_steps) == 1 and len(raw_steps[0]) > 1:
            subdivided = [[update] for update in raw_steps[0]]
            self.steps = subdivided
        else:
            self.steps = raw_steps
        
        self.display_step(-1)

    def rebuild_state(self, upto_index):
        # Reset the current maze to the original
        self.current_maze = copy.deepcopy(self.original_maze)
        # Apply all steps up to and including the specified index.
        for i in range(upto_index + 1):
            for (x, y, val) in self.steps[i]:
                self.current_maze[x][y] = val
        self.last_step = upto_index
        self.current_step = upto_index

    def display_step(self, step_idx):
        if step_idx < -1 or step_idx >= len(self.steps):
            return

        if step_idx == -1:
            self.current_maze = copy.deepcopy(self.original_maze)
            self.last_step = -1
            return

        if step_idx < self.last_step:
            self.rebuild_state(step_idx)
        else:
            # Apply steps incrementally.
            for i in range(self.last_step + 1, step_idx + 1):
                for (x, y, val) in self.steps[i]:
                    self.current_maze[x][y] = val
            self.last_step = step_idx
            self.current_step = step_idx
