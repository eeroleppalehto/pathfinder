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
    def __init__(self, maze_model: MazeModel, canvas_width: int = 650, canvas_height: int = 650, color_scheme: dict = MAZE_COLORS):
        self.maze_model = maze_model
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.color_scheme = color_scheme

        # Calculate cell size so maze exactly fills canvas height
        self.cell_size = canvas_height // self.maze_model.rows

        self.surface_width = self.maze_model.cols * self.cell_size
        self.surface_height = self.maze_model.rows * self.cell_size

        # Center the maze horizontally
        self.offset_x = (self.canvas_width - self.surface_width) // 2
        self.offset_y = (self.canvas_height - self.surface_height) // 2

        # Background = static walls/start/end; overlay = dynamic steps
        self.background_surface = pygame.Surface((self.surface_width, self.surface_height))
        self.overlay_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA).convert_alpha()

        self.initialize_background()

    def initialize_background(self):
        # Draw the static maze once
        self.background_surface.fill(self.color_scheme[0])
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                cell = self.maze_model.original_maze[i][j]
                if cell in (1, 'S', 'E'):
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.background_surface, self.color_scheme[cell], rect)
        # Clear dynamic overlay
        self.overlay_surface.fill((0, 0, 0, 0))

    def update_overlay(self):
        """
        Fallback: full redraw if you ever need to rebuild the entire dynamic layer
        (e.g. on seek/timeline jumps). Not used during normal playback.
        """
        self.overlay_surface.fill((0, 0, 0, 0))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                orig = self.maze_model.original_maze[i][j]
                curr = self.maze_model.current_maze[i][j]
                if curr != orig:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.overlay_surface, self.color_scheme[curr], rect)

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
        surface.blit(self.background_surface, (self.offset_x, self.offset_y))
        surface.blit(self.overlay_surface,    (self.offset_x, self.offset_y))
