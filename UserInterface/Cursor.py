import pygame

class Cursor:
    def __init__(self):
        self._default = pygame.cursors.arrow
        self._cross = pygame.cursors.broken_x
        self._rect = pygame.cursors.load_xbm("xbms/tool-rect-select.xbm", "xbms/tool-rect-select-mask.xbm")
        self._eraser = pygame.cursors.load_xbm("xbms/tool-eraser.xbm", "xbms/tool-eraser-mask.xbm")
        self._current_cursor = "default"
        self.set_default_cursor()

    def set_default_cursor(self):
        if self._current_cursor != "default":
            self._current_cursor = "default"
            pygame.mouse.set_cursor(self._default)

    def set_cross_cursor(self):
        if self._current_cursor != "cross":
            self._current_cursor = "cross"
            pygame.mouse.set_cursor(self._cross)
    
    def set_wand_cursor(self):
        if self._current_cursor != "wand":
            self._current_cursor = "wand"
            pygame.mouse.set_cursor(*self._rect)