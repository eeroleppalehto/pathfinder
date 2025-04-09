import copy
import pygame


COLOR_PANEL_BG = (217, 217, 217)
COLOR_WINDOW_BG = (224, 224, 224)
COLOR_CANVAS_BG = (240, 240, 240)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

MAZE_COLORS = {
    'S': (0, 255, 0),    # Start: Green
    'E': (255, 0, 0),    # End: Red
    1: (0, 0, 0),        # Wall: Black
    0: (255, 255, 255),  # Path: White
    'V': (0, 0, 255),    # Visited: Blue
    'P': (255, 0, 255)   # Final Path: Magenta
}

class MazeState:
    def __init__(self, maze_generator, maze_width=200, maze_height=200, seed=0):
        self.original_maze = maze_generator(maze_width, maze_height, seed)
        self.rows = len(self.original_maze)
        self.cols = len(self.original_maze[0])
        self.current_maze = copy.deepcopy(self.original_maze)
        self.steps = []
        self.current_step = -1
        self.last_step = -1
        self.cell_size = 0
        self.background_surface = None
        self.overlay_surface = None

    def initialize_maze_surfaces(self, canvas_width, canvas_height):
        self.cell_size = min(canvas_width // self.cols, canvas_height // self.rows)
        surface_width = self.cols * self.cell_size
        surface_height = self.rows * self.cell_size
        
        self.background_surface = pygame.Surface((surface_width, surface_height))
        self.background_surface.fill(COLOR_WHITE)
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.original_maze[i][j]
                if cell in (1, 'S', 'E'):
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.background_surface, MAZE_COLORS.get(cell, COLOR_WHITE), rect)
            if i % 50 == 0:
                pygame.event.pump()
        
        self.overlay_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        self.overlay_surface = self.overlay_surface.convert_alpha()
        self.overlay_surface.fill((0, 0, 0, 0))

    def update_dynamic_cell(self, x, y):
        cell = self.current_maze[x][y]
        rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
        if cell in ['V', 'P']:
            pygame.draw.rect(self.overlay_surface, MAZE_COLORS[cell], rect)
        else:
            pygame.draw.rect(self.overlay_surface, (0, 0, 0, 0), rect)

    def rebuild_overlay(self, upto_index):
        self.overlay_surface.fill((0, 0, 0, 0))
        self.current_maze = copy.deepcopy(self.original_maze)
        for i in range(upto_index + 1):
            for (x, y, val) in self.steps[i]:
                self.current_maze[x][y] = val
                self.update_dynamic_cell(x, y)
        self.last_step = upto_index
        self.current_step = upto_index

    def get_start_end(self):
        start = end = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.original_maze[i][j] == 'S':
                    start = (i, j)
                elif self.original_maze[i][j] == 'E':
                    end = (i, j)
        return start, end

    def run_algorithm(self, solver_factory, algorithm_name):
        solver = solver_factory(algorithm_name)
        start, end = self.get_start_end()
        if not start or not end:
            print("Start or end position not found!")
            return
        self.current_maze = copy.deepcopy(self.original_maze)
        self.steps = []
        self.current_step = -1
        self.last_step = -1

        _, raw_steps = solver.solve(copy.deepcopy(self.original_maze), start, end)

        if len(raw_steps) == 1 and len(raw_steps[0]) > 1:
            subdivided = [[update] for update in raw_steps[0]]
            self.steps = subdivided
        else:
            self.steps = raw_steps
        
        self.display_step(-1)

    def display_step(self, step_idx):
        if step_idx < -1 or step_idx >= len(self.steps):
            return

        if step_idx == -1:
            self.current_maze = copy.deepcopy(self.original_maze)
            self.last_step = -1
            self.overlay_surface.fill((0, 0, 0, 0))
            return

        if step_idx < self.last_step:
            self.rebuild_overlay(step_idx)
        else:
            for i in range(self.last_step + 1, step_idx + 1):
                for (x, y, val) in self.steps[i]:
                    self.current_maze[x][y] = val
                    self.update_dynamic_cell(x, y)
            self.last_step = step_idx
            self.current_step = step_idx
