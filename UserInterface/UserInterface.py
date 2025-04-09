# UserInterface.py
import os
import pygame
from .UIComponents import Button, Dropdown, Slider, UIColors

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "Assets")

class ControlPanel:
    def __init__(self, app, panel_x, panel_width, screen_height):
        self.app = app
        self.panel_x = panel_x
        self.panel_width = panel_width
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
        self.dropdown.draw(surface)

    def handle_event(self, event):
        dropdown_changed, algorithm = self.dropdown.handle_event(event)
        if dropdown_changed and algorithm:
            self.app.maze_state.steps = []
        self.play_button.handle_event(event)
        self.pause_button.handle_event(event)
        self.stop_button.handle_event(event)
        self.next_button.handle_event(event)
        self.prev_button.handle_event(event)
        self.slider.handle_event(event)
