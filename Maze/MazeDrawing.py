import pygame

class MazeDrawing:
    def __init__(self, maze_renderer, cursor):
        self.maze_renderer = maze_renderer
        self.maze_model = maze_renderer.maze_model
        self.cursor = cursor
        self.draw_actions = {
            "disabled": lambda row, col : None,
            "draw_walls": self.draw_wall,
            "remove_walls": self.remove_wall,
            "place_start": self.place_start,
            "place_end": self.place_end,
        }
        self.current_draw_state = "disabled"
        self.current_draw_action = self.draw_actions["disabled"]
        
    def handle_event(self, event: pygame.event):
        """
        Handles mouse events to draw walls on the maze.
        """
        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            return
        mouse_x, mouse_y = self.mouse_position(event)

        # Check if the mouse is within the maze bounds.
        if not self.is_on_canvas(mouse_x, mouse_y):
            self.cursor.set_default_cursor()
            return
        
        # Determine the cell coordinates.
        col = mouse_x // self.maze_renderer.cell_size
        row = mouse_y // self.maze_renderer.cell_size

        # Handle mouse button down or motion while holding the button.
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0]):
            # Toggle the wall state for the hovered cell.
            self.current_draw_action(row, col)
        if self.current_draw_state != "disabled":
            self.cursor.set_cross_cursor()
    def is_on_canvas(self, x, y):
        if 0 <= x < self.maze_renderer.surface_width and 0 <= y < self.maze_renderer.surface_height:
            return True
        return False

    def mouse_position(self, event: pygame.event):
        # Get the mouse position relative to the maze.
        x, y = event.pos
        # Adjust for the maze offset.
        maze_x = x - self.maze_renderer.offset_x
        maze_y = y - self.maze_renderer.offset_y
        return maze_x, maze_y

    def draw_wall(self, row, col):
        """
        Toggles the state of a cell between a wall (1) and a path (0).
        """
        # Ensure the cell is within bounds and not a start ('S') or end ('E') cell.
        if self.maze_model.original_maze[row][col] not in ('S', 'E'):
            # Toggle between wall (1) and path (0).
            self.maze_model.original_maze[row][col] = 1
            self.maze_model.current_maze[row][col] = 1
            # Redraw the background to reflect the change.
            self.reset_steps()
            self.maze_renderer.initialize_background()
    
    def remove_wall(self, row, col):
        """
        Toggles the state of a cell between a wall (1) and a path (0).
        """
        # Ensure the cell is within bounds and not a start ('S') or end ('E') cell.
        if self.maze_model.original_maze[row][col] not in ('S', 'E'):
            # Toggle between wall (1) and path (0).
            #self.maze_model.original_maze[row][col] = 1 if self.maze_model.original_maze[row][col] == 0 else 0
            self.maze_model.original_maze[row][col] = 0
            self.maze_model.current_maze[row][col] = 0
            # Redraw the background to reflect the change.
            self.reset_steps()
            self.maze_renderer.initialize_background()

    def place_start(self, row, col):
        # Remove old start from maze
        self.maze_model.original_maze[self.maze_model.start[0]][self.maze_model.start[1]] = 0

        # Update new start
        self.maze_model.original_maze[row][col] = "S"
        self.maze_model.start = (row, col)
        self.reset_steps()
        self.maze_renderer.initialize_background()

    def place_end(self, row, col):
        # Remove old start from maze
        self.maze_model.original_maze[self.maze_model.end[0]][self.maze_model.end[1]] = 0

        # Update new start
        self.maze_model.original_maze[row][col] = "E"
        self.maze_model.end = (row, col)
        self.reset_steps()
        self.maze_renderer.initialize_background()


    def reset_steps(self):
        if len(self.maze_model.steps) != 0:
            self.maze_model.steps = []