class MazeRenderer:
    def __init__(self, maze_state, canvas_width=650, canvas_height=650):
        self.maze_state = maze_state
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.maze_state.initialize_maze_surfaces(canvas_width, canvas_height)

    def draw(self, surface):
        surface.blit(self.maze_state.background_surface, (0, 0))
        surface.blit(self.maze_state.overlay_surface, (0, 0))
