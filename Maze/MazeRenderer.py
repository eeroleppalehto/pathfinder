import pygame

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
    def __init__(self, maze_model, canvas_width=650, canvas_height=650, color_scheme=MAZE_COLORS):
        self.maze_model = maze_model
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.color_scheme = color_scheme
        # Calculate maximum integer cell size that fits in the given canvas.
        self.cell_size = min(canvas_width // self.maze_model.cols, canvas_height // self.maze_model.rows)
        self.surface_width = self.maze_model.cols * self.cell_size
        self.surface_height = self.maze_model.rows * self.cell_size
        
        # Calculate offsets to center the maze.
        self.offset_x = (self.canvas_width - self.surface_width) // 2
        self.offset_y = (self.canvas_height - self.surface_height) // 2

        self.background_surface = pygame.Surface((self.surface_width, self.surface_height))
        self.overlay_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        self.overlay_surface = self.overlay_surface.convert_alpha()
        self.initialize_background()

    def initialize_background(self):
        self.background_surface.fill(self.color_scheme.get(0, (255, 255, 255)))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                cell = self.maze_model.original_maze[i][j]
                if cell in (1, 'S', 'E'):
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    color = self.color_scheme.get(cell, (255, 255, 255))
                    pygame.draw.rect(self.background_surface, color, rect)
        # Clear overlay initially.
        self.overlay_surface.fill((0, 0, 0, 0))

    def update_overlay(self):
        self.overlay_surface.fill((0, 0, 0, 0))
        for i in range(self.maze_model.rows):
            for j in range(self.maze_model.cols):
                original = self.maze_model.original_maze[i][j]
                current = self.maze_model.current_maze[i][j]
                if current != original:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    color = self.color_scheme.get(current, (0, 0, 0, 0))
                    pygame.draw.rect(self.overlay_surface, color, rect)

    def draw(self, surface):
        # Blit the maze surfaces using the computed offset.
        surface.blit(self.background_surface, (self.offset_x, self.offset_y))
        surface.blit(self.overlay_surface, (self.offset_x, self.offset_y))
