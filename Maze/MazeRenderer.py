import pygame
from .MazeModel import MazeModel

# Default color scheme for maze cells
MAZE_COLORS = {
    'S': (0, 255, 0),    # Start: Green
    'E': (255, 0, 0),    # End: Red
    1:    (0, 0, 0),      # Wall: Black
    0:    (255, 255, 255),# Path: White
    'V':  (0, 0, 255),    # Visited: Blue
    'P':  (255, 0, 255)   # Final Path: Magenta
}

class MazeRenderer:
    """
    Renders the maze in two layers:
      - background: walls, paths, start/end (static)
      - overlay: visited and final-path cells (dynamic)
    """
    def __init__(self,
                 maze_model: MazeModel,
                 canvas_width: int = 650,
                 canvas_height: int = 650,
                 color_scheme: dict = MAZE_COLORS):
        # Core references
        self.maze_model = maze_model
        self.color_scheme = color_scheme

        # Compute cell and surface sizes
        self.cell_size = canvas_height // self.maze_model.rows
        self.surface_width = self.maze_model.cols * self.cell_size
        self.surface_height = self.maze_model.rows * self.cell_size

        # Center offsets
        self.offset_x = (canvas_width - self.surface_width) // 2
        self.offset_y = (canvas_height - self.surface_height) // 2

        # Create two surfaces:
        #   background: RGB surface for static cells
        #   overlay:  RGBA surface for dynamic cells (allows clearing with alpha)
        self.background = pygame.Surface((self.surface_width, self.surface_height))
        self.overlay    = pygame.Surface((self.surface_width, self.surface_height), flags=pygame.SRCALPHA)

        # Initial draw of static maze
        self._draw_static()

    def _draw_static(self):
        """Draw walls, empty cells, start & end onto the background layer."""
        self.background.fill((0, 0, 0))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                cell = self.maze_model.maze[i][j]
                if cell == 1:
                    continue
                rect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                color = self.color_scheme.get(cell, (255, 255, 255))
                pygame.draw.rect(self.background, color, rect)

        # Clear any existing overlay markings
        self.overlay.fill((0, 0, 0, 0))

    def update_maze_surface(self):
        """Call whenever the static maze has changed (e.g., new maze or reset)."""
        self._draw_static()

    def update_maze_surface_cell(self, i: int, j: int, value):
        """
        Update a single static cell on the background (e.g.
        when the user draws walls or moves start/end).
        """
        rect = pygame.Rect(
            j * self.cell_size,
            i * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        color = self.color_scheme.get(value, (255, 255, 255))
        pygame.draw.rect(self.background, color, rect)

    def incremental_update_overlay(self, updates):
        """
        Fast path for forward playback: draw only the newly visited or final path cells.
        `updates` is a list of (row, col, val) tuples, where val is 'V' or 'P'.
        """
        for i, j, val in updates:
            rect = pygame.Rect(
                j * self.cell_size,
                i * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.overlay, self.color_scheme[val], rect)

    def clear_overlay(self):
        """
        Wipe all dynamic markings (visited/final) without touching the background.
        """
        # Transparent fill clears any alpha surface content
        self.overlay.fill((0, 0, 0, 0))

    def draw(self, surface: pygame.Surface):
        """
        Blit background and overlay in order onto the target surface.
        """
        surface.blit(self.background, (self.offset_x, self.offset_y))
        surface.blit(self.overlay,    (self.offset_x, self.offset_y))
