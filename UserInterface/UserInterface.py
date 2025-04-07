import os
import tkinter as tk
from tkinter import ttk

from typing import Callable
from .UIComponents import TkinterStyle, TkinterButton, TkinterGridLayout

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKING_DIR, "Assets")


class UIConfig:
    COLOR_PANEL_BG = "#d9d9d9"
    COLOR_WINDOW_BG = "#e0e0e0"
    COLOR_CANVAS_BG = "#f0f0f0"
    COLOR_BUTTON_TEXT = "white"

    SIZE_CONTROL_PANEL = (280, 180)
    GAP_DEFAULT = 10
    SIZE_MAIN_WINDOW = "950x650"

    FONT_BUTTON = ('Arial', 10, 'bold')
    FONT_LABEL = ('Arial', 12, 'bold')
    FONT_DROPDOWN = ('Arial', 10)

class MazeCanvas(tk.Canvas):
    def __init__(self, parent:tk.Widget, width:int=600, height:int=600, bg:str=UIConfig.COLOR_WINDOW_BG):
        super().__init__(
            parent, 
            width=width, 
            height=height, 
            bg=bg, 
            highlightthickness=2, 
            relief="ridge"
        )
        self.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

class ControlActions:
    def __init__(self, 
            play: Callable[[], None], pause: Callable[[], None], stop: Callable[[], None], 
            next: Callable[[], None], prev: Callable[[], None]
    ):
        self.play = play
        self.pause = pause
        self.stop = stop
        self.next = next
        self.prev = prev

class ControlPanel(tk.Frame):
    def __init__(self, parent:tk.Widget, controlActions: ControlActions):
        super().__init__(parent, bg=UIConfig.COLOR_PANEL_BG, relief="raised",
                         bd=2, width=UIConfig.SIZE_CONTROL_PANEL[0], height=UIConfig.SIZE_CONTROL_PANEL[1])
        self.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nw")
        self.grid_propagate(False)
        self.__create_drop_down_menu()
        self.__create_buttons(controlActions)

    def __create_drop_down_menu(self):
        self.top_frame = tk.Frame(self, bg=UIConfig.COLOR_PANEL_BG)
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        self.algorithm_label = tk.Label(self.top_frame, text="Algorithm:", bg=UIConfig.COLOR_PANEL_BG, font=UIConfig.FONT_LABEL)
        self.algorithm_label.pack(side="left", padx=(0, 5))
        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(self.top_frame, textvariable=self.algorithm_var, state="readonly", font=UIConfig.FONT_DROPDOWN)
        self.algorithm_dropdown["values"] = ("BFS", "DFS", "Dijkstra", "A*")
        self.algorithm_dropdown.pack(side="left")
        self.algorithm_dropdown.current(0)

    def __create_buttons(self, actions: ControlActions):
        self.bottom_frame = tk.Frame(self, bg=UIConfig.COLOR_PANEL_BG,
                                     width=UIConfig.SIZE_CONTROL_PANEL[0] - 20,
                                     height=UIConfig.SIZE_CONTROL_PANEL[1] - 50)
        self.bottom_frame.pack(side="top", fill="both", padx=5, pady=5)
        self.bottom_frame.pack_propagate(False)

        self.button_grid = TkinterGridLayout(
            self.bottom_frame,
            gap=UIConfig.GAP_DEFAULT,
            auto_resize=True
        )

        button_style = TkinterStyle(
            background_image=os.path.join(ASSETS_DIR, "button-background.png"),
            button_size=(80, 30),
            font=UIConfig.FONT_BUTTON,
            fg_color=UIConfig.COLOR_BUTTON_TEXT,
            bg_color=UIConfig.COLOR_PANEL_BG
        )

        play_button = TkinterButton(self.bottom_frame, "Play", actions.play, button_style)
        pause_button = TkinterButton(self.bottom_frame, "Pause", actions.pause, button_style)
        stop_button = TkinterButton(self.bottom_frame, "Stop", actions.stop, button_style)
        next_button = TkinterButton(self.bottom_frame, "Next", actions.next, button_style)
        prev_button = TkinterButton(self.bottom_frame, "Previous", actions.prev, button_style)

        self.button_grid.add_button(play_button, row=0, column=0)
        self.button_grid.add_button(pause_button, row=0, column=1)
        self.button_grid.add_button(stop_button, row=1, column=0)
        self.button_grid.add_button(next_button, row=1, column=1)
        self.button_grid.add_button(prev_button, row=2, column=0)

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Visualization")
        self.root.configure(bg=UIConfig.COLOR_WINDOW_BG)
        self.root.geometry(UIConfig.SIZE_MAIN_WINDOW)

        self.canvas = MazeCanvas(root)
        self.control_actions = ControlActions(self.play, self.pause, self.stop, self.next_step, self.prev_step)
        self.control_panel = ControlPanel(root, self.control_actions)

    def play(self):
        print("Play visualization")

    def pause(self):
        print("Pause visualization")

    def stop(self):
        print("Stop visualization")

    def next_step(self):
        print("Next step")

    def prev_step(self):
        print("Previous step")

