import pygame
import sys
import copy
from pygame.locals import QUIT
from .MazeGenerator import MazeGenerator
from .MazeModel import MazeModel
from .MazeSolver import MazeSolver
from .MazeRenderer import MazeRenderer
from .MazeDrawing import MazeDrawing
from UserInterface.UserInterface import UserInterface
from UserInterface.Cursor import Cursor
 
COLOR_WINDOW_BG = (224, 224, 224)

SIZE_OF_MAZE = 100

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
        self.speed = 1
        self.max_speed = 20
        self.step_counter = 0
        self.final_step_count = 0

        self.cursor = Cursor()
        self.maze_generator = MazeGenerator()
        self.maze_model = MazeModel(self.maze_generator, SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer = MazeRenderer(self.maze_model, self.canvas_width, self.canvas_height)
        self.maze_drawing = MazeDrawing(self.maze_renderer, self.cursor)
        self.UserInterface = UserInterface(self, self.canvas_width, self.control_panel_width, screen_height, self.speed, self.max_speed)

        self.is_playing = False
        self.drawing_state = "disabled"
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
                self.maze_drawing.handle_event(event)
                self.UserInterface.handle_event(event)

            if self.is_playing and self.maze_model.steps:
                self.accumulated_time += delta_time
                time_per_step = base_time_per_step / self.speed
                steps_to_process = min(
                    int(self.accumulated_time / time_per_step),
                    len(self.maze_model.steps) - self.maze_model.current_step - 1,
                    100
                )

                if steps_to_process > 0:
                    self.step_counter += steps_to_process
                    self.accumulated_time -= steps_to_process * time_per_step
                    self.maze_model.current_step += steps_to_process
                    self.maze_model.display_step(self.maze_model.current_step)
                    self.maze_renderer.update_overlay()
                elif steps_to_process == 0:
                    self.final_step_count = len(self.maze_model.steps[len(self.maze_model.steps)-1])

            else:
                pygame.time.wait(2)

            self.screen.fill(COLOR_WINDOW_BG)
            self.maze_renderer.draw(self.screen)
            self.UserInterface.draw(self.screen)
            if self.maze_model.steps:
                self.UserInterface.set_timeline(
                    min = 0,
                    max = len(self.maze_model.steps) - 1,
                    value = self.maze_model.current_step
                )
            pygame.display.flip()
            self.clock.tick(60)

  
    def play(self):
        #self.control_panel.draw_option_buttons.deactivate_all()
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions["disabled"]

        if not self.maze_model.steps:
            algorithm_name = self.UserInterface.dropdown.options[self.UserInterface.dropdown.selected]
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
        self.step_counter = 0
        self.maze_model.steps = []
        self.UserInterface.reset_timeline()
        self.maze_model.current_maze = copy.deepcopy(self.maze_model.original_maze)
        self.maze_renderer.initialize_background()

    def next_step(self):
        self.pause()
        self.step_counter += 1
        if self.maze_model.current_step < len(self.maze_model.steps) - 1:
            self.maze_model.display_step(self.maze_model.current_step + 1)
            self.maze_renderer.update_overlay()

    def prev_step(self):
        self.pause()
        self.step_counter -= 1
        if self.maze_model.current_step > 0:
            self.maze_model.display_step(self.maze_model.current_step - 1)
            self.maze_renderer.update_overlay()

    def on_speed_changed(self, value: float):
        self.speed = value

    def on_algorithm_changed(self, value: str):
        if value:
            self.stop()

    def on_timeline_changed(self, value: int):
        if not self.maze_model.steps:
            self.play()

        new_step = int(round(value))
        new_step = max(0, min(new_step, len(self.maze_model.steps) - 1))
        self.step_counter = new_step
        self.maze_model.display_step(new_step)
        self.maze_renderer.update_overlay()
        self.pause()

    def generate_random_maze(self):
        self.maze_model.maze_generator.state = "random"
        self.maze_model.generate_new_maze(SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer.initialize_background()

    def generate_empty_maze(self):
        self.maze_model.maze_generator.state = "empty"
        self.maze_model.generate_new_maze(SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer.initialize_background()

    def set_draw_walls(self):
        self.drawing_state = "draw_walls"
        self.maze_drawing.current_draw_state = self.drawing_state
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions[self.drawing_state]
    
    def set_remove_walls(self):
        self.drawing_state = "remove_walls"
        self.maze_drawing.current_draw_state = self.drawing_state
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions[self.drawing_state]
    
    def set_place_start(self):
        self.drawing_state = "place_start"
        self.maze_drawing.current_draw_state = self.drawing_state
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions[self.drawing_state]
    
    def set_place_end(self):
        self.drawing_state = "place_end"
        self.maze_drawing.current_draw_state = self.drawing_state
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions[self.drawing_state]

if __name__ == "__main__":
    app = MazeApp()
    app.run()
