from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from MazeRenderer import MazeRenderer
    from UserInterface.Cursor import Cursor
class MazeDrawing:
    """
        Class that contains event handling methods to
        draw on the maze frame.
    """
    def __init__(self, maze_renderer: MazeRenderer, cursor: Cursor):
        """Class constructor

        Args:
            maze_renderer (MazeRenderer): MazeRenderer class that is used for updating the maze
            cursor (Cursor): Used to update the shown cursor.
        """
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
        """Handles mouse events to draw walls on the maze.

        Args:
            event (pygame.event): pygame's event module that contains the event data.
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
            if len(self.maze_model.steps) > 0:
                self.maze_model.steps = []
                self.maze_model.reset_maze_to_original()
                self.maze_renderer.update_maze_surface()
            self.current_draw_action(row, col)
        if self.current_draw_state != "disabled":
            self.cursor.set_cross_cursor()

    def is_on_canvas(self, x, y) -> bool:
        if 0 <= x < self.maze_renderer.surface_width and 0 <= y < self.maze_renderer.surface_height:
            return True
        return False

    def mouse_position(self, event: pygame.event) -> tuple[int, int]:
        # Get the mouse position relative to the maze.
        x, y = event.pos
        # Adjust for the maze offset.
        maze_x = x - self.maze_renderer.offset_x
        maze_y = y - self.maze_renderer.offset_y
        return maze_x, maze_y

    def draw_wall(self, row, col):
        """
        Changes the state of a cell from empty space (0) to a wall (1)
        """
        # Ensure the cell is within bounds and not a start ('S') or end ('E') cell.
        if self.maze_model.maze[row][col] not in ('S', 'E'):
            # Toggle between wall (1) and path (0).
            self.maze_model.maze[row][col] = 1
            # self.maze_model.maze[row][col] = 1
            # Redraw the background to reflect the change.
            self.reset_steps()
            self.maze_renderer.update_maze_surface_cell(row, col, 1)
    
    def remove_wall(self, row, col):
        """
        Changes the state of a cell from wall (1) to an empty space (0)
        """
        # Ensure the cell is within bounds and not a start ('S') or end ('E') cell.
        if self.maze_model.maze[row][col] not in ('S', 'E'):
            self.maze_model.maze[row][col] = 0
            self.reset_steps()
            self.maze_renderer.update_maze_surface_cell(row, col, 0)

    def place_start(self, row: int, col: int):
        # Remove old start from maze
        self.maze_model.maze[self.maze_model.start[0]][self.maze_model.start[1]] = 0
        self.maze_renderer.update_maze_surface_cell(self.maze_model.start[0], self.maze_model.start[1], 0)

        # Update new start
        self.maze_model.maze[row][col] = "S"
        self.maze_model.start = (row, col)
        self.reset_steps()
        self.maze_renderer.update_maze_surface_cell(row, col, 'S')

    def place_end(self, row: int, col: int):
        """_summary_

        Args:
            row (int): row to be updated
            col (int): column to be updated
        """
        # Remove old start from maze
        self.maze_model.maze[self.maze_model.end[0]][self.maze_model.end[1]] = 0
        self.maze_renderer.update_maze_surface_cell(self.maze_model.end[0], self.maze_model.end[1], 0)

        # Update new start
        self.maze_model.maze[row][col] = "E"
        self.maze_model.end = (row, col)
        self.reset_steps()
        self.maze_renderer.update_maze_surface_cell(row, col, 'E')


    def reset_steps(self):
        if len(self.maze_model.steps) != 0:
            self.maze_model.steps = []