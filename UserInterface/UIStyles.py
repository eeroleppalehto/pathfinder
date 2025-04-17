import enum
import pygame
pygame.font.init()

class StyleType(enum.IntEnum):
    NORMAL = 0
    HOVER = 1

class StyleProperty(enum.IntFlag):
     NONE = 0
     BACKGROUND_COLOR = 1
     FOREGROUND_COLOR = 2 
     TEXT_COLOR = 4
     FONT_FAMILY = 8
     FONT_SIZE = 16
     BORDER_COLOR = 32
     BORDER_SIZE = 64
     SLIDER_THUMB_COLOR = 128
     END = 256

     def get_index(self):
         if self == StyleProperty.NONE: 
             return -1
         return self.bit_length() - 1

class StyleSheet:
    TYPE_NORMAL = 0
    TYPE_HOVER = 1

    def __init__(
        self,
        background_color: tuple[int, int, int] = (255, 255, 255),
        foreground_color: tuple[int, int, int] = (255, 255, 255),
        text_color: tuple[int, int, int] = (0, 0, 0),
        font_family: str = None,
        font_size: int = 24,
        border_color: tuple[int, int, int] = (0, 0, 0),
        border_size: int = 0,
        thumb_color: tuple[int, int, int] = (0, 0, 0)
    ):
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.text_color = text_color
        self._font_family = font_family
        self._font_size = font_size
        self.border_color = border_color
        self.border_size = border_size
        self.slider_thumb_color = thumb_color
        self._font = pygame.font.Font(self._font_family, self._font_size)

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
    def font_size(self, value:int):
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
        return (
            self.normal
            if style_type == StyleType.NORMAL
            else self.hover
        )
    
class Styleable:
    def get_style_property(self, property: StyleProperty, is_hovered: bool):
        raise NotImplementedError

    def set_style_property(self, property: StyleProperty, value, state: int | None = None):
        raise NotImplementedError
    
    @property
    def background_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(StyleProperty.BACKGROUND_COLOR, is_hovered=False)

    @background_color.setter
    def background_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(StyleProperty.BACKGROUND_COLOR, color, StyleType.NORMAL)

    @property
    def hover_background_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(StyleProperty.BACKGROUND_COLOR, is_hovered=True)

    @hover_background_color.setter
    def hover_background_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(StyleProperty.BACKGROUND_COLOR, color, StyleType.HOVER)

    @property
    def font_family(self) -> str | None:
        return self.get_style_property(StyleProperty.FONT_FAMILY, is_hovered=False)

    @font_family.setter
    def font_family(self, family: str | None):
        self.set_style_property(StyleProperty.FONT_FAMILY, family, StyleType.NORMAL)

    @property
    def hover_font_family(self) -> str | None:
        return self.get_style_property(StyleProperty.FONT_FAMILY, is_hovered=True)

    @hover_font_family.setter
    def hover_font_family(self, family: str | None):
        self.set_style_property(StyleProperty.FONT_FAMILY, family, StyleType.HOVER)

    @property
    def font_size(self) -> int | None:
        return self.get_style_property(StyleProperty.FONT_SIZE, is_hovered=False)

    @font_size.setter
    def font_size(self, size: int | None):
        self.set_style_property(StyleProperty.FONT_SIZE, size, StyleType.NORMAL)

    @property
    def hover_font_size(self) -> int | None:
        return self.get_style_property(StyleProperty.FONT_SIZE, is_hovered=True)

    @hover_font_size.setter
    def hover_font_size(self, size: int | None):
        self.set_style_property(StyleProperty.FONT_SIZE, size, StyleType.HOVER)

    @property
    def text_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(StyleProperty.TEXT_COLOR, is_hovered=False)

    @text_color.setter
    def text_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(StyleProperty.TEXT_COLOR, color, StyleType.NORMAL)

    @property
    def hover_text_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(StyleProperty.TEXT_COLOR, is_hovered=True)

    @hover_text_color.setter
    def hover_text_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(StyleProperty.TEXT_COLOR, color, StyleType.HOVER)
    
    @property
    def slider_thumb_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(
            StyleProperty.SLIDER_THUMB_COLOR,
            is_hovered=False
        )

    @slider_thumb_color.setter
    def slider_thumb_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(
            StyleProperty.SLIDER_THUMB_COLOR,
            color,
            StyleType.NORMAL
        )

    @property
    def hover_slider_thumb_color(self) -> tuple[int, int, int] | None:
        return self.get_style_property(
            StyleProperty.SLIDER_THUMB_COLOR,
            is_hovered=True
        )

    @hover_slider_thumb_color.setter
    def hover_slider_thumb_color(self, color: tuple[int, int, int] | None):
        self.set_style_property(
            StyleProperty.SLIDER_THUMB_COLOR,
            color,
            StyleType.HOVER
        )

     
NUM_STYLE_PROPERTIES = len(StyleProperty) - 1
class ComponentStyleManager:
    def __init__(self, base_style_group: StyleGroup):
        self.base_style_group = base_style_group
        self._masks = [StyleProperty.NONE, StyleProperty.NONE]
        self._values = [[None] * NUM_STYLE_PROPERTIES, [None] * NUM_STYLE_PROPERTIES]
        self._fonts = [None, None]

    def set_normal_style(self, style: StyleSheet):
        self.base_style_group.normal = style
    
    def set_hover_style(self, style:StyleSheet):
        self.base_style_group.hover = style

    def set_override(self, prop: StyleProperty, value, style_type: int | None = StyleType.NORMAL):
        if prop is StyleProperty.NONE:
            return

        states = (
            [style_type] if style_type in (StyleType.NORMAL, StyleType.HOVER)
            else [StyleType.NORMAL, StyleType.HOVER]
        )

        index = prop.get_index()
        for state in states:
            self._masks[state] |= prop
            self._values[state][index] = value
            
            if prop in (StyleProperty.FONT_FAMILY, StyleProperty.FONT_SIZE):
                self._fonts[state] = None

    def clear_overrides(self, style_type: int | None = None):
        states = (
            [style_type]
            if style_type in (StyleType.NORMAL, StyleType.HOVER)
            else [StyleType.NORMAL, StyleType.HOVER]
        )
        for state in states:
            self._masks[state] = StyleProperty.NONE
            self._values[state] = [None] * NUM_STYLE_PROPERTIES
            self._fonts[state] = None

    def get_resolved_property(self, prop: StyleProperty, style_type: int = StyleType.NORMAL):
        if prop is StyleProperty.NONE:
            return None

        index = prop.get_index()
        if self._masks[style_type] & prop:
            return self._values[style_type][index]

        sheet = self.base_style_group.get(style_type)
        return getattr(sheet, prop.name.lower(), None)

    def get_resolved_font(self, style_type: int) -> pygame.font.Font:
        cached = self._fonts[style_type]
        if cached:
            return cached

        mask = self._masks[style_type]
        values = self._values[style_type]
        base = self.base_style_group.get(style_type)

        family = (
            values[StyleProperty.FONT_FAMILY.get_index()]
            if mask & StyleProperty.FONT_FAMILY
            else base.font_family
        )
        size = (
            values[StyleProperty.FONT_SIZE.get_index()]
            if mask & StyleProperty.FONT_SIZE
            else base.font_size
        ) or base.font_size or 20

        try:
            font = pygame.font.Font(family, size)
        except Exception:
            font = base._font or pygame.font.Font(None, 20)

        self._fonts[style_type] = font
        return font


def apply_style_to_components(style_type: int, style_sheet: StyleSheet, components: list):
        if style_type == StyleType.NORMAL:
            for component in components:
                component.set_style(style_sheet)
        elif style_type == StyleType.HOVER:
            for component in components:
                component.set_hover_style(style_sheet)


