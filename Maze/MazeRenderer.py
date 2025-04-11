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
        # Use SRCALPHA to allow for overlay transparency.
        self.overlay_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        self.overlay_surface = self.overlay_surface.convert_alpha()

        self.initialize_background()

    def initialize_background(self):
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

    def draw(self, surface):
        # Blit both the background and overlay surfaces using the computed offsets.
        surface.blit(self.background_surface, (self.offset_x, self.offset_y))
        surface.blit(self.overlay_surface, (self.offset_x, self.offset_y))
