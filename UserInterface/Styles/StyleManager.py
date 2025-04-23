import pygame
from typing import Optional, Union
from .StyleEnums import StyleProperty, StyleType
from .StyleSheet import StyleGroup, StyleSheet, DEFAULT
from UserInterface.Defaults.DefaultStyles import DefaultStyles

INHERITABLE_STYLE_PROPERTIES = (
    "background_color",
    "foreground_color",
    "text_color",
    "font_family",
    "font_size",
    "border_color",
    "border_size",
    "slider_thumb_color",
    "text_align",
)

NUM_STYLE_PROPERTIES = len(StyleProperty) - 1


class InlineStyle:
    """Mixin for adding inline style overrides (normal state only)."""
    def get_style_property(self, prop: StyleProperty, is_hovered: bool):
        style_type = StyleType.HOVER if is_hovered else StyleType.NORMAL
        return self._style_manager.get_resolved_property(prop, style_type)

    def set_style_property(self, prop: StyleProperty, value):
        self._style_manager.set_override(prop, value)

    @property
    def background_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.BACKGROUND_COLOR, False)

    @background_color.setter
    def background_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.BACKGROUND_COLOR, color)

    @property
    def font_family(self) -> Optional[str]:
        return self.get_style_property(StyleProperty.FONT_FAMILY, False)

    @font_family.setter
    def font_family(self, family: Optional[str]):
        self.set_style_property(StyleProperty.FONT_FAMILY, family)

    @property
    def font_size(self) -> Optional[int]:
        return self.get_style_property(StyleProperty.FONT_SIZE, False)

    @font_size.setter
    def font_size(self, size: Optional[int]):
        self.set_style_property(StyleProperty.FONT_SIZE, size)

    @property
    def text_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.TEXT_COLOR, False)

    @text_color.setter
    def text_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.TEXT_COLOR, color)

    @property
    def slider_thumb_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.SLIDER_THUMB_COLOR, False)

    @slider_thumb_color.setter
    def slider_thumb_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.SLIDER_THUMB_COLOR, color)

    @property
    def text_align(self) -> Optional[str]:
        return self.get_style_property(StyleProperty.TEXT_ALIGN, False)

    @text_align.setter
    def text_align(self, align: Optional[str]):
        self.set_style_property(StyleProperty.TEXT_ALIGN, align)

class ComponentStyleManager:
    """Manages base and inline style overrides (normal state only)."""
    def __init__(self, base_style_group: StyleGroup):
        self.base_style_group = base_style_group
        self._default_style_group = None
        self._inline_mask = StyleProperty.NONE
        self._inline_values = [None] * NUM_STYLE_PROPERTIES
        self._inline_font = None
        

    def set_normal_style(self, style: StyleSheet, component_name: str):
        if self._default_style_group is None:
            self._default_style_group = DefaultStyles.get_by_component_name(component_name)

        default_sheet = self._default_style_group.normal
        
        for property in INHERITABLE_STYLE_PROPERTIES:
            val = getattr(style, property)
            if val is DEFAULT:
                setattr(style, property, getattr(default_sheet, property))

        self.base_style_group = StyleGroup(style, self.base_style_group.hover)

    def set_hover_style(self, style: StyleSheet, component_name: str):
        if self._default_style_group is None:
            self._default_style_group = DefaultStyles.get_by_component_name(component_name)
        
        default_sheet = self._default_style_group.hover

        for property in INHERITABLE_STYLE_PROPERTIES:
            val = getattr(style, property)
            if val is DEFAULT:
                setattr(style, property, getattr(default_sheet, property))

        self.base_style_group = StyleGroup(self.base_style_group.normal, style)

    def set_override(self, prop: StyleProperty, value):
        if prop is StyleProperty.NONE:
            return
        idx = prop.get_index()
        self._inline_mask |= prop
        self._inline_values[idx] = value
        if prop in (StyleProperty.FONT_FAMILY, StyleProperty.FONT_SIZE):
            self._inline_font = None

    def clear_overrides(self):
        self._inline_mask = StyleProperty.NONE
        self._inline_values = [None] * NUM_STYLE_PROPERTIES
        self._inline_font = None

    def get_resolved_property(self, prop: StyleProperty, style_type: int = StyleType.NORMAL):
        if prop is StyleProperty.NONE:
            return None
        idx = prop.get_index()
        if style_type == StyleType.NORMAL:
            if self._inline_mask & prop:
                return self._inline_values[idx]
            return getattr(self.base_style_group.normal, prop.name.lower())
        else:
            value = getattr(self.base_style_group.hover, prop.name.lower())
            if value:
                return value
            return getattr(self.base_style_group.normal, prop.name.lower())


    def get_resolved_font(self, style_type: int) -> pygame.font.Font:
        if self._inline_font:
            return self._inline_font
        base = self.base_style_group.get(style_type)
        family = base.font_family
        size = base.font_size or 20
        try:
            font = pygame.font.Font(family, size)
        except Exception:
            font = pygame.font.Font(None, size)
        self._inline_font = font
        return font
