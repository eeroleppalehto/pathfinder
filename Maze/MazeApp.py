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

class FPSCounter:
    def __init__(self, clock, update_rate_fps=10):
        self.clock = clock
        self.update_interval = 1000 // update_rate_fps  # ms between logs
        self.last_log_time = 0

    def update(self, current_time: int, loop_start_time: int):
        if current_time - self.last_log_time >= self.update_interval:
            fps = self.clock.get_fps()
            loop_duration = pygame.time.get_ticks() - loop_start_time
            print(f"[Perf] FPS: {fps:.1f}, loop time: {loop_duration} ms")
            self.last_log_time = current_time


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
        self.last_scrubbed_step = 0
        self.target_fps = 1000

        self.speed = 1
        self.max_speed = 20
        self.step_counter = 0
        self.final_step_count = 0

        self.cursor = Cursor()
        self.maze_generator = MazeGenerator()
        self.maze_model = MazeModel(self.maze_generator, SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer = MazeRenderer(self.maze_model, self.canvas_width, self.canvas_height)
        self.maze_drawing = MazeDrawing(self.maze_renderer, self.cursor)
        self.UserInterface = UserInterface(self,self.canvas_width, self.control_panel_width, screen_height)

        self.is_playing = False
        self.drawing_state = "disabled"
        self.accumulated_time = 0

    def solver_factory(self, algorithm_name):
        return MazeSolver(algorithm=algorithm_name)

    def run(self):
        self.stop()
        self.accumulated_time = 0
        time_per_cell_at_1x = 50  # milliseconds per step at 1× speed
        fps_counter = FPSCounter(self.clock, update_rate_fps=5)

        last_frame_time = pygame.time.get_ticks()
        self.step_counter = 0
        self.final_step_count = 0

        while True:
            loop_start_time = pygame.time.get_ticks()
            current_time = loop_start_time
            delta_time = min(current_time - last_frame_time, 50)
            last_frame_time = current_time

            # --- Handle Events ---
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                self.maze_drawing.handle_event(event)
                self.UserInterface.handle_event(event)

            # --- Play Simulation ---
            if self.is_playing and self.maze_model.steps:
                self.accumulated_time += delta_time
                time_per_step = time_per_cell_at_1x / self.speed
                
                steps_to_apply = min(
                    int(self.accumulated_time / time_per_step),
                    len(self.maze_model.steps) - self.maze_model.current_step - 1,
                    100 
                )

                if steps_to_apply > 0:
                    self.accumulated_time -= steps_to_apply * time_per_step
                    self.step_counter += steps_to_apply

                    range_start = self.maze_model.current_step + 1
                    range_end = self.maze_model.current_step + steps_to_apply
                    self._apply_steps_in_range(range_start, range_end)
                    
                    self.maze_model.current_step += steps_to_apply
                else:
                    self.final_step_count = len(self.maze_model.steps)

            # --- Draw Frame ---
            self.screen.fill(COLOR_WINDOW_BG)
            self.maze_renderer.draw(self.screen)
            self.UserInterface.draw(self.screen)

            if self.maze_model.steps:
                self.UserInterface.set_timeline(
                    min=0,
                    max=len(self.maze_model.steps) - 1,
                    value=self.maze_model.current_step
                )
     
            pygame.display.flip()
            self.clock.tick(self.target_fps)  
            fps_counter.update(current_time, loop_start_time)

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self):
        self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions["disabled"]

        if not self.maze_model.steps:
            algorithm_name = self.UserInterface.dropdown.options[
                self.UserInterface.dropdown.selected
            ]
            self.maze_model.run_algorithm(self.solver_factory, algorithm_name)
            self.maze_renderer.update_overlay()

        if not self.is_playing:
            self.is_playing = True
            self.accumulated_time = 0

    def pause(self):
        self.is_playing = False

    def stop(self):
        self.is_playing = False
        self.step_counter = 0
        self.final_step_count = 0
        self.maze_model.current_step = -1
        self.maze_model.steps = []
        self.UserInterface.reset_timeline()
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

    def on_speed_changed(self, value: float):
        self.speed = value

    def on_algorithm_changed(self, value: str):
        if value:
            self.stop()

    def on_timeline_changed(self, slider_value: int):
        """
        Updates the maze to reflect the state at the selected step in the timeline.
        """
        if not self.maze_model.steps:
            self.play()

        new_step = max(0, min(int(round(slider_value)), len(self.maze_model.steps) - 1))
        previous_step = self.last_scrubbed_step

        if new_step > previous_step:
            self._apply_steps_forward(previous_step + 1, new_step)
        elif new_step < previous_step:
            self._rewind_to_step(new_step)

        self.maze_model.current_step = new_step
        self.last_scrubbed_step = new_step
        self.step_counter = new_step + 1
        self.final_step_count = len(self.maze_model.steps)

        self.pause()

    def _apply_steps_in_range(self, start: int, end: int):
        """
        Applies a range of maze steps (inclusive), updating both the model and the overlay.
        """
        for step_index in range(start, end + 1):
            updates = self.maze_model.steps[step_index]
            for x, y, value in updates:
                self.maze_model.current_maze[x][y] = value
            self.maze_renderer.incremental_update_overlay(updates)


    def _apply_steps_forward(self, start_step: int, end_step: int):
        """
        Applies maze updates step-by-step from start_step to end_step (inclusive),
        and updates the overlay accordingly.
        """
        for i in range(start_step, end_step + 1):
            updates = self.maze_model.steps[i]
            for x, y, value in updates:
                self.maze_model.current_maze[x][y] = value
            
            self.maze_renderer.incremental_update_overlay(updates)

    def _rewind_to_step(self, step_index: int):
        """
        Rebuilds the maze to the state at step_index, and reconstructs the overlay.
        """
        self.maze_model.rebuild_state(step_index)
        self.maze_renderer.overlay_surface.fill((0, 0, 0, 0))
        for i in range(0, step_index + 1):
            updates = self.maze_model.steps[i]
            self.maze_renderer.incremental_update_overlay(updates)

    def generate_random_maze(self):
        self.stop()
        self.maze_model.maze_generator.state = "random"
        self.maze_model.generate_new_maze(SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer.initialize_background()

    def generate_empty_maze(self):
        self.stop()
        self.maze_model.maze_generator.state = "empty"
        self.maze_model.generate_new_maze(SIZE_OF_MAZE, SIZE_OF_MAZE)
        self.maze_renderer.initialize_background()

    def disable_drawing_mode(self):
        return

    def set_draw_state(self, draw_state):
        VALID_DRAW_STATES = ["draw_walls", "remove_walls", "place_start", "place_end"]

        needs_reset = self.maze_model.current_step != -1
        if needs_reset:
            self.stop() 

        if draw_state in VALID_DRAW_STATES :
            self.drawing_state = draw_state
            self.maze_drawing.current_draw_state = self.drawing_state
            self.maze_drawing.current_draw_action = self.maze_drawing.draw_actions[self.drawing_state]
