import random

def generate_maze(num_cols, num_rows, seed=None):
    # Seed the random number generator for reproducibility.
    if seed is not None:
        random.seed(seed)
        
    # Ensure odd dimensions for proper maze structure.
    num_cols = num_cols if num_cols % 2 == 1 else num_cols + 1
    num_rows = num_rows if num_rows % 2 == 1 else num_rows + 1

    # Initialize maze: fill with walls represented by 1's.
    maze = [[1 for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Start carving from (1,1) inside the maze.
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