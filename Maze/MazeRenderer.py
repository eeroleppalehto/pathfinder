import pygame
from .MazeModel import MazeModel

# Define a color scheme (used for both static and dynamic cells).
MAZE_COLORS = {
    'S': (0, 255, 0),    # Start: Green
    'E': (255, 0, 0),    # End: Red
    1: (0, 0, 0),        # Wall: Black
    0: (255, 255, 255),  # Path: White
    'V': (0, 0, 255),    # Visited: Blue
    'P': (255, 0, 255)   # Final Path: Magenta
}

class MazeRenderer:
    """
    A class to render the maze using Pygame.
    It creates a background surface for the maze and an overlay surface for dynamic updates.
    The maze is centered in the canvas, and the cell size is calculated based on the canvas height.
    The color scheme for the maze is defined in a dictionary, allowing for easy customization.
    The maze is represented as a grid of cells, where each cell can be a wall, path, start, end, or visited cell.
    The class provides methods to initialize the background, update the overlay based on the current maze state,
    and draw the maze on a given surface.
    """
    def __init__(self, maze_model: MazeModel, canvas_width: int = 650, canvas_height: int = 650, color_scheme: dict = MAZE_COLORS):
        """Initializes the MazeRenderer with the given maze model and canvas dimensions.

        Args:
            maze_model (MazeModel): The model representing the maze structure.
            canvas_width (int, optional): The width of the canvas. Defaults to 650.
            canvas_height (int, optional): The height of the canvas. Defaults to 650.
            color_scheme (dict, optional): A dictionary defining the colors for different cell types. Defaults to MAZE_COLORS.
        """
        self.maze_model = maze_model
        self.canvas_width: int = canvas_width
        self.canvas_height: int = canvas_height
        self.color_scheme: dict = color_scheme

        # Calculate the cell size so that the maze fills the canvas height.
        self.cell_size = canvas_height // self.maze_model.rows

        # Update the surface dimensions based on the new cell_size.
        self.surface_width = self.maze_model.cols * self.cell_size
        self.surface_height = self.maze_model.rows * self.cell_size
        
        # Center the maze horizontally (vertical centering will be exact now).
        self.offset_x = (self.canvas_width - self.surface_width) // 2
        self.offset_y = (self.canvas_height - self.surface_height) // 2

        self.maze_surface = pygame.Surface((self.surface_width, self.surface_height))
        self.update_maze_surface()

    def update_maze_surface(self):
        self.maze_surface.fill((0, 0, 0))  # Clear the maze surface
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                cell = self.maze_model.maze[i][j]
                if cell == 1:
                    continue
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                    self.cell_size, self.cell_size)
                color = self.color_scheme.get(cell, (255, 255, 255))
                pygame.draw.rect(self.maze_surface, color, rect)
    
    def update_maze_surface_cell(self, i: int, j: int, value):
        rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                            self.cell_size, self.cell_size)
        color = self.color_scheme.get(value, (255, 255, 255))
        pygame.draw.rect(self.maze_surface, color, rect)

    def incremental_update_overlay(self, updates):
        """
        Very fast: only draw the exact cells that just changed.
        `updates` is a list of (row, col, new_val) tuples.
        """
        len(updates)
        for i, j, val in updates:
            rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.maze_surface, self.color_scheme[val], rect)
            
    def draw(self, surface: pygame.Surface):
        """Draws the maze on the given surface, including the background and overlay."""
        # Blit both the background and overlay surfaces using the computed offsets.
        surface.blit(self.maze_surface, (self.offset_x, self.offset_y))