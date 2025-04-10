import pygame
import sys
import copy
from pygame.locals import QUIT
from .MazeGenerator import MazeGenerator
from .MazeModel import MazeModel
from .MazeSolver import MazeSolver
from .MazeRenderer import MazeRenderer
from UserInterface.UserInterface import ControlPanel

COLOR_WINDOW_BG = (224, 224, 224)

class MazeApp:
    def __init__(self, screen_width=950, screen_height=650):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height),
            pygame.HWSURFACE | pygame.DOUBLEBUF 
        )

        pygame.display.set_caption("Maze Solver Visualization")

        self.clock = pygame.time.Clock()
        self.canvas_width = 650
        self.canvas_height = 650
        self.control_panel_width = 250

        maze_generator = MazeGenerator()
        self.maze_model = MazeModel(maze_generator, 100, 100)
        self.maze_renderer = MazeRenderer(self.maze_model, self.canvas_width, self.canvas_height)
        self.control_panel = ControlPanel(self, self.canvas_width, self.control_panel_width, screen_height)

        self.is_playing = False
        self.accumulated_time = 0


    def solver_factory(self, algorithm_name):
        return MazeSolver(algorithm=algorithm_name)

    def run(self):
        self.stop()
        self.accumulated_time = 0
        base_time_per_step = 50  # Base delay (ms) per cell update at 1x speed
        last_update = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - last_update
            last_update = current_time
            delta_time = min(delta_time, 50)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.control_panel.handle_event(event)

            if self.is_playing and self.maze_model.steps:
                self.accumulated_time += delta_time
                time_per_step = base_time_per_step / self.control_panel.slider.value
                steps_to_process = min(
                    int(self.accumulated_time / time_per_step),
                    len(self.maze_model.steps) - self.maze_model.current_step - 1,
                    100
                )

                if steps_to_process > 0:
                    self.accumulated_time -= steps_to_process * time_per_step
                    self.maze_model.current_step += steps_to_process
                    self.maze_model.display_step(self.maze_model.current_step)
                    self.maze_renderer.update_overlay()

            else:
                pygame.time.wait(2)

            self.screen.fill(COLOR_WINDOW_BG)
            self.maze_renderer.draw(self.screen)
            self.control_panel.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)

    def play(self):
        if not self.maze_model.steps:
            algorithm_name = self.control_panel.dropdown.options[self.control_panel.dropdown.selected]
            self.maze_model.run_algorithm(self.solver_factory, algorithm_name)
            self.maze_renderer.update_overlay()

        if not self.is_playing:
            self.is_playing = True
            self.accumulated_time = 0

    def pause(self):
        self.is_playing = False

    def stop(self):
        self.is_playing = False
        self.maze_model.current_step = -1
        self.maze_model.steps = []
        self.maze_model.current_maze = copy.deepcopy(self.maze_model.original_maze)
        self.maze_renderer.initialize_background()

    def next_step(self):
        self.pause()
        if self.maze_model.current_step < len(self.maze_model.steps) - 1:
            self.maze_model.display_step(self.maze_model.current_step + 1)
            self.maze_renderer.update_overlay()

    def prev_step(self):
        self.pause()
        if self.maze_model.current_step > 0:
            self.maze_model.display_step(self.maze_model.current_step - 1)
            self.maze_renderer.update_overlay()

if __name__ == "__main__":
    app = MazeApp()
    app.run()
