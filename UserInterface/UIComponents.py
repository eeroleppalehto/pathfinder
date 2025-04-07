import os
import tkinter as tk
from PIL import Image, ImageTk
from typing import Callable

class TkinterStyle:
    def __init__(self, background_image: str, button_size: tuple, font: tuple, fg_color: str, bg_color: str):
        self.background_image = background_image
        self.button_size = button_size
        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color


class TkinterButton:
    def __init__(self, parent: tk.Widget, text: str, command: Callable[[], None], style: TkinterStyle):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.bg_image = None

        try:
            self.original_image = Image.open(self.style.background_image)
            self.button = self.create_button(self.style.button_size)
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.button = tk.Button(
                self.parent,
                text=self.text,
                command=self.command,
                font=self.style.font,
                fg=self.style.fg_color,
                bg=self.style.bg_color,
                borderwidth=0,
                highlightthickness=0,
                relief='flat'
            )

    def create_button(self, desired_size):
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS

        resized_image = self.original_image.resize(desired_size, resample)
        self.bg_image = ImageTk.PhotoImage(resized_image)

        button = tk.Button(
            self.parent,
            text=self.text,
            command=self.command,
            image=self.bg_image,
            compound='center',
            font=self.style.font,
            fg=self.style.fg_color,
            bg=self.style.bg_color,
            borderwidth=0,
            highlightthickness=0,
            relief='flat'
        )
        button.image = self.bg_image
        return button

    def resize(self, new_size):
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS

        resized_image = self.original_image.resize(new_size, resample)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.button.config(image=self.bg_image)
        self.button.image = self.bg_image


class TkinterGridLayout:
    def __init__(self, parent:tk.Widget, gap:int=0, auto_resize:bool=False):
        self.parent = parent
        self.gap = gap
        self.auto_resize = auto_resize
        self.buttons = []
        if self.auto_resize:
            self.parent.bind("<Configure>", self.on_resize)

    def add_button(self, tk_button, row, column):
        tk_button.button.place(x=0, y=0)
        self.buttons.append((tk_button, row, column))
        if self.auto_resize:
            self.on_resize(None)

    def on_resize(self, event):
        if not self.auto_resize or not self.buttons:
            return

        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        max_row = max(row for (_, row, _) in self.buttons)
        max_col = max(col for (_, _, col) in self.buttons)
        total_rows = max_row + 1
        total_cols = max_col + 1

        total_gap_x = self.gap * (total_cols - 1)
        total_gap_y = self.gap * (total_rows - 1)
        cell_width = max(1, (parent_width - total_gap_x) // total_cols)
        cell_height = max(1, (parent_height - total_gap_y) // total_rows)

        for btn, row, col in self.buttons:
            x = col * (cell_width + self.gap)
            y = row * (cell_height + self.gap)
            btn.resize((cell_width, cell_height))
            btn.button.place(x=x, y=y, width=cell_width, height=cell_height)

