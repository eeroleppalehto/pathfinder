
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import copy
if TYPE_CHECKING:
    from MazeRenderer import MazeRenderer
    from UserInterface.Cursor import Cursor

class MazeDrawing:
    """
    Handles mouse events to draw on the maze and pushes incremental updates
    to the renderer's overlay, avoiding full surface redraws.
    """
    def __init__(self, maze_renderer: MazeRenderer, cursor: Cursor):
        self.maze_renderer = maze_renderer
        self.maze_model = maze_renderer.maze_model
        self.cursor = cursor
        self.needs_initialization = False

        self.draw_actions = {
            "disabled": lambda r, c: None,
            "draw_walls": self.draw_wall,
            "remove_walls": self.remove_wall,
            "place_start": self.place_start,
            "place_end": self.place_end,
        }
        self.current_draw_state = "disabled"
        self.current_draw_action = self.draw_actions["disabled"]

        # Last cell drawn during a drag, to make continuous lines
        self._prev_cell: tuple[int, int] | None = None

    
    def is_on_canvas(self, x, y) -> bool:
        if 0 <= x < self.maze_renderer.surface_width and 0 <= y < self.maze_renderer.surface_height:
            return True
        return False

    def mouse_position(self, event: pygame.event) -> tuple[int, int]:
        x, y = event.pos
        maze_x = x - self.maze_renderer.offset_x
        maze_y = y - self.maze_renderer.offset_y
        return maze_x, maze_y


    def handle_event(self, event: pygame.event):
        if event.type not in (pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP,
                              pygame.MOUSEMOTION):
            return

        mx, my = self.mouse_position(event)
        if not self.is_on_canvas(mx, my):
            self.cursor.set_default_cursor()
            if event.type == pygame.MOUSEBUTTONUP:
                self._prev_cell = None
            return

        col = mx // self.maze_renderer.cell_size
        row = my // self.maze_renderer.cell_size


        if event.type == pygame.MOUSEBUTTONUP:
            self._prev_cell = None
            self.reset_steps()
            self.maze_renderer.initialize_background()
     
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_val = self.current_draw_action(row, col)
            if new_val is not None:
                self.needs_initialization = True
                self.maze_renderer.incremental_update_overlay([(row, col, new_val)])

            if self.current_draw_state in ("draw_walls", "remove_walls"):
                self._prev_cell = (row, col)
                
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if self.current_draw_state not in ("draw_walls", "remove_walls"):
                return
            current = (row, col)
            if self._prev_cell is None:
                self._prev_cell = current

            changes: list[tuple[int, int, int]] = []
            line = self.draw_line(self._prev_cell, current)

            for r, c in line:
                new_val = self.current_draw_action(r, c)
                if new_val is not None:
                    changes.append((r, c, new_val))
                    
            if changes:
                self.maze_renderer.incremental_update_overlay(changes)
            self._prev_cell = current

        if self.current_draw_state != "disabled":
            self.cursor.set_cross_cursor()

    def draw_line(self, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        # (same Bresenham list-based implementation as before)
        start_row, start_col = start
        end_row, end_col = end
        delta_row = abs(end_row - start_row)
        delta_col = abs(end_col - start_col)
        step_row = 1 if end_row >= start_row else -1
        step_col = 1 if end_col >= start_col else -1
        cells: list[tuple[int, int]] = []
        row, col = start_row, start_col
        if delta_col > delta_row:
            err = delta_col // 2
            for _ in range(delta_col + 1):
                cells.append((row, col))
                col += step_col
                err -= delta_row
                if err < 0:
                    row += step_row
                    err += delta_col
        else:
            err = delta_row // 2
            for _ in range(delta_row + 1):
                cells.append((row, col))
                row += step_row
                err -= delta_col
                if err < 0:
                    col += step_col
                    err += delta_row
        return cells

    def draw_wall(self, row: int, col: int) -> int | None:
        if self.maze_model.original_maze[row][col] in ('S', 'E'):
            return None
        self.maze_model.original_maze[row][col] = 1
        self.maze_model.current_maze[row][col] = 1
        self.reset_steps()
        return 1

    def remove_wall(self, row: int, col: int) -> int | None:
        if self.maze_model.original_maze[row][col] in ('S', 'E'):
            return None
        self.maze_model.original_maze[row][col] = 0
        self.maze_model.current_maze[row][col] = 0
        self.reset_steps()
        return 0

    def place_start(self, row: int, col: int) -> int | None:
        old_r, old_c = self.maze_model.start
        if (row, col) == (old_r, old_c):
            return None
        # clear old start cell
        self.maze_model.original_maze[old_r][old_c] = 0
        self.maze_model.current_maze[old_r][old_c] = 0

        # set new start
        self.maze_model.original_maze[row][col] = 'S'
        self.maze_model.current_maze[row][col] = 'S'
        self.maze_model.start = (row, col)
        self.reset_steps()
        
        return 'S'

    def place_end(self, row: int, col: int) -> int | None:
        old_r, old_c = self.maze_model.end
        if (row, col) == (old_r, old_c):
            return None
        self.maze_model.original_maze[old_r][old_c] = 0
        self.maze_model.current_maze[old_r][old_c] = 0

        self.maze_model.original_maze[row][col] = 'E'
        self.maze_model.current_maze[row][col] = 'E'
        self.maze_model.end = (row, col)
        self.reset_steps()
        return 'E'

    def reset_steps(self):
        self.maze_model.current_step = -1
        if self.maze_model.steps:
            self.maze_model.steps.clear()
