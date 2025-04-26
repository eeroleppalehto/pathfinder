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

        # Create surfaces for the background and the overlay.
        self.background_surface = pygame.Surface((self.surface_width, self.surface_height))
        self.overlay_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        self.overlay_surface = self.overlay_surface.convert_alpha()

        self.initialize_background()

    def initialize_background(self):
        """Initializes the background surface with the maze's original state."""
        # Fill the background with the color for a path.
        self.background_surface.fill(self.color_scheme.get(0, (255, 255, 255)))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                cell = self.maze_model.original_maze[i][j]
                # For walls and the special start/end cells, draw the colored block.
                if cell in (1, 'S', 'E'):
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    color = self.color_scheme.get(cell, (255, 255, 255))
                    pygame.draw.rect(self.background_surface, color, rect)
        # Initially clear the overlay.
        self.overlay_surface.fill((0, 0, 0, 0))

    def update_overlay(self):
        """Updates the overlay surface to reflect the current state of the maze."""
        self.overlay_surface.fill((0, 0, 0, 0))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                original = self.maze_model.original_maze[i][j]
                current = self.maze_model.current_maze[i][j]
                # Draw only if there is a difference between the original and the current cell.
                if current != original:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    color = self.color_scheme.get(current, (0, 0, 0, 0))
                    pygame.draw.rect(self.overlay_surface, color, rect)

    def incremental_update_overlay(self, updates):
        """
        Very fast: only draw the exact cells that just changed.
        `updates` is a list of (row, col, new_val) tuples.
        """
        for i, j, val in updates:
            rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.overlay_surface, self.color_scheme[val], rect)

    def draw(self, surface: pygame.Surface):
        """Draws the maze on the given surface, including the background and overlay."""
        # Blit both the background and overlay surfaces using the computed offsets.
        surface.blit(self.background_surface, (self.offset_x, self.offset_y))
        surface.blit(self.overlay_surface, (self.offset_x, self.offset_y))