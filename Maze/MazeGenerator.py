import random

class MazeGenerator:
    """
    This class cointains methods for generating mazes that are matrices where 
        walls are represented as 1,
        empty spaces by 0,
        start cell by 'S',
        and end cell by 'E'.
    """
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.state = "random"
        self.seed = 0

    def generate(self, num_cols, num_rows, seed=None):
        # Seed the random number generator for reproducibility.
        if seed is not None:
            random.seed(seed)

        num_cols = num_cols if num_cols % 2 == 1 else num_cols + 1
        num_rows = num_rows if num_rows % 2 == 1 else num_rows + 1

        if self.state != "random":
            return self.generate_empty_maze(num_rows, num_cols)
        else:
            self.seed += 1
            return self.generate_random(num_cols, num_rows, self.seed)
    
    def generate_random(self, num_cols: int, num_rows: int, seed: int | float | str | bytes | bytearray | None = None):
        """
        This method generates a randomized maze
        where start is placed top left and end to bottom right.
        
        Args:
            width (int): width of the generated maze
            height (int): height of the generated maze
            seed (int | float | str | bytes | bytearray | None): Variable to initialize seed. Defaults to None.

        Returns:
            maze: generated matrix
        """
        # Seed the random number generator for reproducibility.
        if seed is not None:
            random.seed(seed)

        num_cols = num_cols if num_cols % 2 == 1 else num_cols + 1
        num_rows = num_rows if num_rows % 2 == 1 else num_rows + 1
        maze = [[1 for _ in range(num_cols)] for _ in range(num_rows)]
        
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 0  # Mark as passage
        
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]
            # Check neighbors in 2-step increments (up, right, down, left).
            neighbors = []
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < num_cols and 0 < ny < num_rows and maze[ny][nx] == 1:
                    neighbors.append((nx, ny))
            if neighbors:
                nx, ny = random.choice(neighbors)
                # Remove wall between the current cell and neighbor.
                wall_x, wall_y = x + (nx - x) // 2, y + (ny - y) // 2
                maze[wall_y][wall_x] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Force a connection to the borders:
        # Top-left corner connection.
        maze[0][0] = 0
        if maze[0][1] == 1 and maze[1][0] == 1:
            maze[0][1] = 0  # Carve a passage to the right
        
        # Bottom-right corner connection.
        maze[num_rows - 1][num_cols - 1] = 0
        if maze[num_rows - 2][num_cols - 1] == 1 and maze[num_rows - 1][num_cols - 2] == 1:
            maze[num_rows - 2][num_cols - 1] = 0  # Carve a passage above
        
        # Mark start and end positions.
        maze[0][0] = 'S'
        maze[num_rows - 1][num_cols - 1] = 'E'
        
        return maze

    def generate_empty_maze(self, width, height):
        """
        This method generates a empty maze where the outer cells are walls
        and start is placed topleft and end to bottomright
        
        Args:
            width (int): width of the generated maze
            height (int): height of the generated maze

        Returns:
            maze: generated matrix
        """
        maze: list[list[int]] = []

        for i in range(width):
            maze.append([])
            for _ in range(height):
                maze[i].append(0)

        for i in range(height):
            maze[0][i] = 1
            maze[width-1][i] = 1

        for i in range(width):
            maze[i][0] = 1
            maze[i][height-1] = 1
        
        maze[1][1] = "S"
        maze[width-2][height-2] = "E"

        return maze
