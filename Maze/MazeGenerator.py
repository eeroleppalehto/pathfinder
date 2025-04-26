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
            num_cols (int): width of the generated maze
            num_rows (int): height of the generated maze
            seed (int | float | str | bytes | bytearray | None): Variable to initialize seed. Defaults to None.

        Returns:
            maze: generated matrix
        """
        # Seed the random number generator for reproducibility.
        if seed is not None:
            random.seed(seed)

        num_cols = (num_cols if num_cols % 2 == 1 else num_cols + 1)
        num_rows = (num_rows if num_rows % 2 == 1 else num_rows + 1)

        start_col, end_col = 0, num_cols - 1
        start_row, end_row = 0, num_rows - 1

        maze = [[1] * num_cols for _ in range(num_rows)]
        maze[start_col + 1][start_row + 1] = 0  

        cell_stack = [(1, 1)]
        DIRECTIONS = [(0, -2), (2, 0), (0, 2), (-2, 0)]

        while cell_stack:
            x, y = cell_stack[-1]
            neighbour_cells = []
            
            for direction_x, direction_y in DIRECTIONS:
                neighbour_x = x + direction_x
                neighbour_y = y + direction_y

                in_bounds = (0 < neighbour_x < num_cols and 0 < neighbour_y < num_rows)
                if in_bounds and maze[neighbour_y][neighbour_x] == 1:
                    neighbour_cells.append((neighbour_x, neighbour_y))

            if neighbour_cells:
                neighbour_x, neighbour_y = random.choice(neighbour_cells)

                # compute the coordinates of the wall between the current cell and its neighbor
                wall_x = x + (neighbour_x - x) // 2
                wall_y = y + (neighbour_y - y) // 2

                maze[wall_y][wall_x] = 0
                maze[neighbour_y][neighbour_x] = 0
                cell_stack.append((neighbour_x, neighbour_y))
            else:
                cell_stack.pop()
        
        # open the two corner cells
        maze[start_row][end_row] = 0
        maze[start_row][start_col] = 0
 
        # Top-left corner connection.
        top_left_neighbors_are_walls = (maze[0][1] == 1 and maze[1][0] == 1)
        if (top_left_neighbors_are_walls):
            maze[start_row][start_col + 1] = 0  # Carve a passage to the right
        
        # Bottom-right corner connection.
        bottom_right_neighbors_are_walls = (maze[num_rows-2][num_cols-1] == 1 and maze[num_rows-1][num_cols-2] == 1)
        if bottom_right_neighbors_are_walls:
            maze[end_row - 1][end_col] = 0 
        
        # Mark start and end positions.
        maze[start_row][start_col] = 'S'
        maze[end_row][end_col] = 'E'
        
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
