import os
import pygame
from .Components.UIComponents import Button, Dropdown, Header, Slider, Panel
from .Core.UIRoot import UIRoot
from .Styles.StyleSheet import StyleSheet
from .Styles.StyleFilters import brightness, contrast, saturation, tint, hue_rotate
from .Styles.StyleEnums import StyleType
from .Core.StyleUtilities import apply_style_to_components


class UserInterface:
    def __init__(self, app, panel_x, panel_width, screen_height):
        self.app = app
        self.control_panel_x = panel_x
        self.control_panel_width = panel_width
        self.screen_height = screen_height
        self._create_components()
        self._update_component_styles()

    def _update_component_styles(self):
        self.draw_start_button.background_color = (76, 175, 80)
        self.draw_end_button.background_color = (244, 67, 54)
        self.draw_empty_button.background_color = (200, 220, 240)  # very light blue
        self.draw_wall_button.background_color = (60, 60, 66)
        components = [self.draw_start_button, self.draw_end_button,  self.draw_empty_button, self.draw_wall_button]
        hover_style = StyleSheet(
            filter = [brightness(0.75), saturation(2), hue_rotate(-10)]
        )

        apply_style_to_components(StyleType.HOVER, hover_style, components)

    def _create_components(self):
        self.root = UIRoot()
        self.control_panel = Panel((self.control_panel_x, 0), (self.control_panel_width, self.screen_height))
        self.dropdown = Dropdown((20, 20), (200, 30), ["BFS", "DFS", "Dijkstra", "A*"], 0, self.app.on_algorithm_changed)
        self.speed_slider = Slider((20, 85), (200, 15), (10, 20), 0.1, self.app.max_speed, self.app.speed, self.app.on_speed_changed)
        self.play_button = Button((20, 160), (100, 30), "Play", self.app.play)
        self.pause_button = Button((130, 160), (100, 30), "Pause", self.app.pause)
        self.stop_button = Button((20, 200), (100, 30), "Stop", self.app.stop)
        self.next_button = Button((130, 200), (100, 30), "Next", self.app.next_step)
        self.prev_button = Button((20, 240), (100, 30), "Prev", self.app.prev_step)
        self.generate_empty_button = Button((20, 520), (100, 30), "Empty", self.app.generate_empty_maze)
        self.generate_maze_button = Button((130, 520), (100, 30), "Random", self.app.generate_random_maze)
        self.timeline_slider = Slider((20, 305), (200, 15), (10, 20), 0, 0, 0, self.app.on_timeline_changed)
        self.speed_header = Header((20, 58), f"Speed: {self.speed_slider.value:.1f}x")
        self.timeline_header = Header((20, 280), "Timeline")
        self.steps_header = Header((20, 340), "Steps")

        self.step_counter_header = Header((30, 370), f"Total: {self.app.step_counter}")
        self.step_counter_header.text_color = (0,0,255)
        self.final_step_count_header = Header((30, 400), f"Path: {self.app.final_step_count}")
        self.final_step_count_header.text_color = (255, 0, 255)
        self.drawing_tools_header = Header((20, 560), "Drawing tools")
        self.drawing_tools_panel = Panel((20, 590), (210, 40))

        self.draw_start_button = Button((5, 5), (30, 30), "", self.app.set_draw_state, value="place_start")
        self.draw_end_button = Button((40, 5), (30, 30), "", self.app.set_draw_state, value="place_end")
        self.draw_wall_button = Button((75, 5), (30, 30), "", self.app.set_draw_state, value="draw_walls")
        self.draw_empty_button = Button((110, 5), (30, 30), "", self.app.set_draw_state, value="remove_walls")

        # The order you add the children is the draw order of them.
        self.buttons = [self.play_button, self.pause_button, self.stop_button, self.next_button, self.prev_button, self.generate_empty_button, self.generate_maze_button, self.dropdown]
        self.sliders = [self.speed_slider, self.timeline_slider]
        self.headers = [self.speed_header, self.timeline_header, self.drawing_tools_header]
        self.panels = [self.drawing_tools_panel]
        self.draw_buttons = [self.draw_start_button, self.draw_end_button, self.draw_wall_button, self.draw_empty_button]
        
        self.drawing_tools_panel.add_children(self.draw_buttons)
        self.control_panel.add_children(self.sliders)
        self.control_panel.add_children(self.headers)
        self.control_panel.add_children(self.buttons)
        self.control_panel.add_children(self.panels)
        self.control_panel.add_children([self.steps_header, self.step_counter_header, self.final_step_count_header])
        self.root.add_component(self.control_panel)

    def draw(self, surface):
        self.speed_header.text = f"Speed: {self.speed_slider.value:.1f}x"
        self.step_counter_header.text = f"Total: {self.app.step_counter}"
        self.final_step_count_header.text = f"Path: {self.app.final_step_count}"
        self.root.draw(surface)

    def set_timeline(self, min, max, value):
        self.timeline_slider.min = min
        self.timeline_slider.max = max
        if not self.timeline_slider.dragging:
                self.timeline_slider.value = value

    def reset_timeline(self):
        self.timeline_slider.value = 0

    def handle_event(self, event):
        self.root.handle_event(event)

    