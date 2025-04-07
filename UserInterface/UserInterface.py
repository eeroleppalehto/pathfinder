# UserInterface.py
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
    def __init__(self, parent: tk.Widget, width: int = 600, height: int = 600, bg: str = UIConfig.COLOR_WINDOW_BG):
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
    def __init__(self, play: Callable[[], None], pause: Callable[[], None],
                 stop: Callable[[], None], next: Callable[[], None], prev: Callable[[], None]):
        self.play = play
        self.pause = pause
        self.stop = stop
        self.next = next
        self.prev = prev

class ControlPanel(tk.Frame):
    def __init__(self, parent: tk.Widget, controlActions: ControlActions):
        super().__init__(parent, bg=UIConfig.COLOR_PANEL_BG, relief="raised",
                         bd=2, width=UIConfig.SIZE_CONTROL_PANEL[0], height=UIConfig.SIZE_CONTROL_PANEL[1])
        self.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nw")
        self.grid_propagate(False)
        self.__create_drop_down_menu()
        self.__create_buttons(controlActions)

    def __create_drop_down_menu(self):
        self.top_frame = tk.Frame(self, bg=UIConfig.COLOR_PANEL_BG)
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        # Algorithm dropdown
        self.algorithm_label = tk.Label(self.top_frame, text="Algorithm:", bg=UIConfig.COLOR_PANEL_BG, font=UIConfig.FONT_LABEL)
        self.algorithm_label.pack(side="left", padx=(0, 5))
        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(self.top_frame, textvariable=self.algorithm_var, state="readonly", font=UIConfig.FONT_DROPDOWN)
        self.algorithm_dropdown["values"] = ("BFS", "DFS", "Dijkstra", "A*")
        self.algorithm_dropdown.pack(side="left")
        self.algorithm_dropdown.current(0)
        # Speed slider
        self.speed_label = tk.Label(self.top_frame, text="Speed:", bg=UIConfig.COLOR_PANEL_BG, font=UIConfig.FONT_LABEL)
        self.speed_label.pack(side="left", padx=(10, 5))
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_slider = ttk.Scale(
            self.top_frame,
            from_=0.1,
            to=2.0,
            variable=self.speed_var,
            orient='horizontal',
            length=100
        )
        self.speed_slider.pack(side="left")

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
    def __init__(self, root, maze_generator, solver_factory):
        """
        Initialize the UI with injected maze_generator and solver_factory.
        - maze_generator: an object with a generate_maze() method.
        - solver_factory: a function that accepts an algorithm name and returns a MazeSolver instance.
        """
        self.root = root
        self.root.title("Maze Solver Visualization")
        self.root.configure(bg=UIConfig.COLOR_WINDOW_BG)
        self.root.geometry(UIConfig.SIZE_MAIN_WINDOW)

        self.maze_generator = maze_generator
        self.solver_factory = solver_factory

        self.maze = self.maze_generator.generate_maze()
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.steps = []
        self.current_step = 0
        self.is_playing = False
        self.after_id = None

        self.canvas = MazeCanvas(self.root)
        self.control_actions = ControlActions(self.play, self.pause, self.stop, self.next_step, self.prev_step)
        self.control_panel = ControlPanel(self.root, self.control_actions)

        self.draw_initial_maze()

    def draw_initial_maze(self):
        """Display the initial maze."""
        self.display_grid(self.maze)

    def display_grid(self, grid):
        """Render the provided grid state on the canvas."""
        self.canvas.delete("all")
        cell_size = 40
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = self.get_cell_color(grid[i][j])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def get_cell_color(self, value):
        return {
            'S': "green",
            'E': "red",
            1: "black",
            0: "white",
            'V': "blue",    # Visited cells during exploration
            'P': "magenta"  # Correct final path (different color)
        }.get(value, "white")

    def get_start_end(self):
        start = end = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == 'S':
                    start = (i, j)
                elif self.maze[i][j] == 'E':
                    end = (i, j)
        return start, end

    def run_algorithm(self):
        """Use the injected solver_factory to solve the maze using the selected algorithm.
        This method retrieves both the final path and all intermediate steps.
        """
        algorithm_name = self.control_panel.algorithm_var.get()
        solver = self.solver_factory(algorithm_name)
        start, end = self.get_start_end()
        import copy
        maze_copy = copy.deepcopy(self.maze)
        final_path, steps = solver.solve(maze_copy, start, end)
        
        # Mark the final correct path (except for start and end) with 'P'
        if final_path:
            final_snapshot = copy.deepcopy(steps[-1])
            for (x, y) in final_path:
                if final_snapshot[x][y] not in ('S', 'E'):
                    final_snapshot[x][y] = 'P'
            steps.append(final_snapshot)
        
        self.steps = steps


    def display_step(self, step_idx):
        if 0 <= step_idx < len(self.steps):
            self.current_step = step_idx
            self.display_grid(self.steps[step_idx])

    def play(self):
        if not self.steps:
            self.run_algorithm()
        if not self.is_playing:
            self.is_playing = True
            self.schedule_next_step()

    def schedule_next_step(self):
        if self.is_playing and self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_step(self.current_step)
            delay = int(1000 / (self.control_panel.speed_var.get() * 10))
            self.after_id = self.root.after(delay, self.schedule_next_step)
        else:
            self.is_playing = False

    def pause(self):
        if self.is_playing:
            self.root.after_cancel(self.after_id)
            self.is_playing = False

    def stop(self):
        self.pause()
        self.current_step = 0
        self.display_step(0)

    def next_step(self):
        self.pause()
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_step(self.current_step)

    def prev_step(self):
        self.pause()
        if self.current_step > 0:
            self.current_step -= 1
            self.display_step(self.current_step)
