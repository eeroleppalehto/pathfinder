import pygame
from .StyleEnums import StyleType
from typing import Optional

pygame.init()
pygame.font.init()

class _Default:
    pass

DEFAULT = _Default()

class StyleSheet:
    def __init__(
        self,
        background_color: Optional[tuple[int, int, int]] = DEFAULT,
        foreground_color: Optional[tuple[int, int, int]] = DEFAULT,
        text_color: Optional[tuple[int, int, int]] = DEFAULT,
        font_family: Optional[str] = DEFAULT,
        font_size: Optional[int] = 24,
        border_color: Optional[tuple[int, int, int]] = DEFAULT,
        border_size: Optional[int] = 0,
        thumb_color: Optional[tuple[int, int, int]] = DEFAULT,
        text_align: Optional[str] = "left"
    ):
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.text_color = text_color
        self._font_family = font_family
        self._font_size = font_size
        self.border_color = border_color
        self.border_size = border_size
        self.slider_thumb_color = thumb_color
        self.text_align = text_align
        if self._font_size != None and self._font_size > 0:
            family = None if self._font_family is DEFAULT else self._font_family
            self._font = pygame.font.Font(family, self._font_size)
    
    @property
    def font_family(self):
        return self._font_family
    
    @property
    def font_size(self):
        return self._font_size
    
    @font_family.setter
    def font_family(self, value: str):
        if value != self._font_family:
            self._font_family = value
            self._recalculate_font()

    @font_size.setter
    def font_size(self, value: int):
        if value != self._font_size:
            self._font_size = value
            self._recalculate_font()

    def _recalculate_font(self):
        self._font = pygame.font.Font(self._font_family, self._font_size)

    def get_font(self):
        return self._font

class StyleGroup:
    def __init__(self, normal: StyleSheet, hover: StyleSheet):
        self.normal = normal
        self.hover = hover

    def get(self, style_type: int) -> StyleSheet:
        return self.normal if style_type == StyleType.NORMAL else self.hover
