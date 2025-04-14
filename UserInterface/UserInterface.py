# UserInterface.py
import os
import pygame
from .UIComponents import Button, Dropdown, Slider, UIColors, DrawOptionButtonGroup

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "Assets")

class ControlPanel:
    def __init__(self, app, panel_x, panel_width, screen_height):
        self.app = app
        self.panel_x = panel_x # The width of the maze panel
        self.panel_width = panel_width # width of 
        self.screen_height = screen_height

        self.dropdown = Dropdown(panel_x + 20, 20, 200, 30, ["BFS", "DFS", "Dijkstra", "A*"])
        self.slider = Slider(panel_x + 20, 70, 200, 15, 0.1, 20.0, 1.0)
        button_width = 100
        button_height = 30
        self.play_button = Button(panel_x + 20, 160, button_width, button_height, "Play", self.app.play)
        self.pause_button = Button(panel_x + 20 + 110, 160, button_width, button_height, "Pause", self.app.pause)
        self.stop_button = Button(panel_x + 20, 200, button_width, button_height, "Stop", self.app.stop)
        self.next_button = Button(panel_x + 20 + 110, 200, button_width, button_height, "Next", self.app.next_step)
        self.prev_button = Button(panel_x + 20, 240, button_width, button_height, "Prev", self.app.prev_step)
    
        self.generate_button = Button(panel_x + 20 + 110, 520, button_width, button_height, "Random", self.app.generate_random_maze)
        self.draw_button = Button(panel_x + 20, 520, button_width, button_height, "Empty", self.app.generate_empty_maze)
        self.draw_option_buttons = DrawOptionButtonGroup(app, panel_x, 560)

        self.timeline_slider = Slider(panel_x + 20, 280, 200, 15, 0, 0, 0)


    def draw(self, surface):
        panel_rect = pygame.Rect(self.app.canvas_width, 0, self.panel_width, self.screen_height)
        pygame.draw.rect(surface, UIColors.PANEL_BG, panel_rect)
        font = pygame.font.Font(None, 24)
        speed_label = font.render(f"Speed: {self.slider.value:.1f}x", True, UIColors.BLACK)
        surface.blit(speed_label, (self.app.canvas_width + 20, 50))
        self.slider.draw(surface)
        self.play_button.draw(surface)
        self.pause_button.draw(surface)
        self.stop_button.draw(surface)
        self.next_button.draw(surface)
        self.prev_button.draw(surface)
        self.generate_button.draw(surface)
        self.draw_button.draw(surface)
        self.draw_option_buttons.draw(surface)
        self.dropdown.draw(surface)

        if self.app.maze_model.steps:
            max_step = len(self.app.maze_model.steps) - 1
            self.timeline_slider.min = 0
            self.timeline_slider.max = max_step

            if not self.timeline_slider.dragging:
                self.timeline_slider.value = self.app.maze_model.current_step
                
            font = pygame.font.Font(None, 24)
            timeline_label = font.render("Timeline", True, UIColors.BLACK)
            surface.blit(timeline_label, (self.panel_x + 20, 260))
            self.timeline_slider.draw(surface)


    def handle_event(self, event):
        dropdown_changed, algorithm = self.dropdown.handle_event(event)
        if dropdown_changed and algorithm:
            self.app.maze_model.steps = []
        self.play_button.handle_event(event)
        self.pause_button.handle_event(event)
        self.stop_button.handle_event(event)
        self.next_button.handle_event(event)
        self.prev_button.handle_event(event)
        self.generate_button.handle_event(event)
        self.draw_button.handle_event(event)
        self.slider.handle_event(event)
        self.draw_option_buttons.handle_event(event)

        if self.app.maze_model.steps:
            timeline_changed = self.timeline_slider.handle_event(event)
            if timeline_changed:
                new_step = int(round(self.timeline_slider.value))
                new_step = max(0, min(new_step, len(self.app.maze_model.steps) - 1))
                self.app.maze_model.display_step(new_step)
                self.app.maze_renderer.update_overlay()
                self.app.pause()
