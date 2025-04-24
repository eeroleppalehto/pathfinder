import pygame
from typing import Optional, Union
from .StyleEnums import StyleProperty, StyleType
from .StyleSheet import StyleGroup, StyleSheet, DEFAULT
from .StyleFilters import FilterToken, apply_all_filters, apply_filter

from UserInterface.Defaults.DefaultStyles import DefaultStyles

INHERITABLE_STYLE_PROPERTIES = (
    "background_color",
    "foreground_color",
    "text_color",
    "font_family",
    "font_size",
    "border_color",
    "border_size",
    "thumb_color",
    "text_align",
    "filter"
)

COMPUTED_STYLE_PROPERTIES = (
    StyleProperty.BACKGROUND_COLOR,
    StyleProperty.FOREGROUND_COLOR,
    StyleProperty.TEXT_COLOR,
    StyleProperty.BORDER_COLOR,
    StyleProperty.THUMB_COLOR
)

NUM_COMPUTED_STYLE_PROPERTIES = len(COMPUTED_STYLE_PROPERTIES) - 1
NUM_STYLE_PROPERTIES = len(StyleProperty) - 1


class InlineStyle:
    """Mixin for adding inline style overrides (normal state only)."""
    def get_style_property(self, prop: StyleProperty, is_hovered: bool):
        style_type = StyleType.HOVER if is_hovered else StyleType.NORMAL
        return self.style_manager.get_resolved_property(prop, style_type)

    def set_style_property(self, prop: StyleProperty, value):
        self.style_manager.set_override(prop, value)

    def set_computed_style_property(self, prop: StyleProperty, value: tuple[int, int, int] | None):
        self.style_manager.set_computed_override(prop, value)
        print("Set computed style property called!")

    @property
    def filter(self) -> list[FilterToken]:
        return self.get_style_property(StyleProperty.FILTER, is_hovered=False)

    @filter.setter
    def filter(self, token: Union[FilterToken, list[FilterToken]]):
        if(isinstance(token, list) == False):
            token = [token]

        self.set_style_property(StyleProperty.FILTER, token)
        self.style_manager.update_normal_computed_styles()


    @property
    def background_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.BACKGROUND_COLOR, False)
    
    @background_color.setter
    def background_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.BACKGROUND_COLOR, color)
        self.set_computed_style_property(StyleProperty.BACKGROUND_COLOR, color)

    @property
    def foreground_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.FOREGROUND_COLOR, False)
    
    @foreground_color.setter
    def foreground_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.FOREGROUND_COLOR, color)
        self.set_computed_style_property(StyleProperty.FOREGROUND_COLOR, color)

    @property
    def border_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.BORDER_COLOR, False)
    
    @border_color.setter
    def border_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.BORDER_COLOR, color)
        self.set_computed_style_property(StyleProperty.BORDER_COLOR, color)

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
        self.set_computed_style_property(StyleProperty.TEXT_COLOR, color)

    @property
    def thumb_color(self) -> Optional[tuple[int, int, int]]:
        return self.get_style_property(StyleProperty.THUMB_COLOR, False)

    @thumb_color.setter
    def slider_thumb_color(self, color: Optional[tuple[int, int, int]]):
        self.set_style_property(StyleProperty.THUMB_COLOR, color)
        self.set_computed_style_property(StyleProperty.THUMB_COLOR, color)

    @property
    def text_align(self) -> Optional[str]:
        return self.get_style_property(StyleProperty.TEXT_ALIGN, False)

    @text_align.setter
    def text_align(self, align: Optional[str]):
        self.set_style_property(StyleProperty.TEXT_ALIGN, align)

class ComponentStyleManager:
    """Manages base and inline style overrides (normal state only)."""
    def __init__(self, component_name, normal_style, hover_style):
        self.base_style_group = StyleGroup(None, None)
        self._default_style_group = DefaultStyles.get_by_component_name(component_name)
        self._inline_mask = StyleProperty.NONE
        self._inline_values = [None] * NUM_STYLE_PROPERTIES
        self._computed_normal_style_values = [None] * NUM_STYLE_PROPERTIES
        self._computed_hover_style_values = [None] * NUM_STYLE_PROPERTIES
        self._inline_font = None

        self.set_normal_style(normal_style, component_name)
        self.set_hover_style(hover_style, component_name)

    def set_normal_style(self, style: StyleSheet, component_name: str):
        default_sheet = self._default_style_group.normal
        
        for property in INHERITABLE_STYLE_PROPERTIES:
            val = getattr(style, property)
            if val is DEFAULT:
                default_value = getattr(default_sheet, property)
                setattr(style, property, default_value)


        self.base_style_group = StyleGroup(style, self.base_style_group.hover)
        filter = self._inline_values[(StyleProperty.FILTER).get_index()]
        
        if filter == None:
            filter = style._filter
            if(filter == None):
                return
    
        for property in COMPUTED_STYLE_PROPERTIES:
            idx = property.get_index()
            value = self._inline_values[idx]

            if(value == None):
                value = getattr(style, property.name.lower())
                if(value == None):
                    continue
            
            computed_value = value
            for token in filter:
                computed_value = apply_filter(computed_value, token)

            self._computed_normal_style_values[idx] = computed_value


      
    def set_hover_style(self, style: StyleSheet, component_name: str):
        if self._default_style_group is None:
            self._default_style_group = DefaultStyles.get_by_component_name(component_name)
        
        default_sheet = self._default_style_group.hover

        for property in INHERITABLE_STYLE_PROPERTIES:
            val = getattr(style, property)
            if val is DEFAULT:
                setattr(style, property, getattr(default_sheet, property))
        
        self.base_style_group = StyleGroup(self.base_style_group.normal, style)

        if style._filter == None:
            return

        for property in COMPUTED_STYLE_PROPERTIES:
            property_name = property.name.lower()
            value = getattr(style, property_name)
            idx = property.get_index()

            if(value == None):
                value = self._inline_values[idx]

                if value == None:
                    value = getattr(self.base_style_group.normal, property_name)

                    if(value == None):
                        continue

            for token in style._filter:
                value = apply_filter(value, token)

            self._computed_hover_style_values[idx] = value

    def update_normal_computed_styles(self):
        FILTER_PROPERTY = StyleProperty.FILTER
        filter = self._inline_values[FILTER_PROPERTY.get_index()]

        if filter == None:
            normal_style = self.base_style_group.normal
            if(normal_style == None):
                return
            filter = normal_style.filter
            if(filter == None):
                return
    

        for property in COMPUTED_STYLE_PROPERTIES:
            idx = property.get_index()
            value = self._inline_values[idx]
            if(value == None):
                normal_style = self.base_style_group.normal
                value = getattr(normal_style, property.name.lower())
                if(value == None):
                    continue
            
            for token in filter:
                value = apply_filter(value, token)

            idx = property.get_index()
            self._computed_normal_style_values[idx] = value

    def normal_style_exists(self):
        return self.base_style_group != None and self.base_style_group.normal != None
    
    def hover_style_exists(self):
        return self.base_style_group != None and self.base_style_group.hover != None
    
    def get_normal_style(self):
        if self.base_style_group != None:
            return self.base_style_group.normal
        return None
    
    def get_hover_style(self):
        if self.base_style_group != None:
            return self.base_style_group.hover
        return None
    
    def set_computed_override(self, prop:StyleProperty, value: tuple[int, int, int] | None):
        if prop is StyleProperty.NONE or value == None:
            return
        
        if(prop not in COMPUTED_STYLE_PROPERTIES):
            return 
      
        normal_filter = self._inline_values[StyleProperty.FILTER.get_index()]
        if(normal_filter == None):
            normal_filter = self.base_style_group.normal._filter

        
        if(normal_filter != None):
            computed_color = value
            for token in normal_filter:
                computed_color = apply_filter(computed_color, token)
                
            idx = prop.get_index()
            self._computed_normal_style_values[idx] = computed_color

        hover_filter_exists = self.base_style_group.hover and self.base_style_group.hover._filter
        if (hover_filter_exists):
            hover_filter = self.base_style_group.hover._filter
            computed_color = getattr(self.base_style_group.hover, prop.name.lower())

            if computed_color == None:
                computed_color = self._inline_values[prop.get_index()]
            if computed_color == None:
                computed_color = getattr(self.base_style_group.normal, prop.name.lower())
                if computed_color == None:
                    return

            for token in hover_filter:
                computed_color = apply_filter(computed_color, token)
                
            idx = prop.get_index()
            self._computed_hover_style_values[idx] = computed_color



    def update_computed_style(self, stylesheet, prop:StyleProperty, value: tuple[int, int, int] | None):
        is_normal_stylesheet = stylesheet == self.base_style_group.normal
        if is_normal_stylesheet and self._inline_mask & prop:
            return
        
        if prop is StyleProperty.NONE or value == None:
            return
        
        if(prop not in COMPUTED_STYLE_PROPERTIES):
            return 
            
        filter = stylesheet._filter
        if(filter == None):
            return
        
        computed_color = value
        for token in filter:
            computed_color = apply_filter(computed_color, token)
            
        idx = prop.get_index()
        if is_normal_stylesheet:
            self._computed_normal_style_values[idx] = computed_color
        else:
            self._computed_hover_style_values[idx] = computed_color


    def set_override(self, prop: StyleProperty, value):
        if prop is StyleProperty.NONE:
            return
        
        if value is None:
            self._inline_mask &= ~prop
            self._inline_values[idx] = None
        else:
            idx = prop.get_index()
            self._inline_mask |= prop
            self._inline_values[idx] = value

        if prop in (StyleProperty.FONT_FAMILY, StyleProperty.FONT_SIZE):
            self._inline_font = None

    def clear_overrides(self):
        self._inline_mask = StyleProperty.NONE
        self._inline_values = [None] * NUM_STYLE_PROPERTIES
        self._inline_font = None

    def get_resolved_property(self, prop: StyleProperty, style_type: int = StyleType.NORMAL, is_computed = False):
        if is_computed:
            if(prop not in COMPUTED_STYLE_PROPERTIES):
                return self._get_non_computed_style_property(prop, style_type)
            else:
                return self._get_computed_style_property(prop, style_type)
            
        else:
            return self._get_non_computed_style_property(prop, style_type)
        
    def _get_computed_style_property(self, prop: StyleProperty, style_type: int = StyleType.NORMAL):
        if style_type == StyleType.NORMAL:
            value = self._computed_normal_style_values[prop.get_index()]
            if(value):
                return value
        else:
            value = self._computed_hover_style_values[prop.get_index()]
            if(value):
                return value
        
        return self._get_non_computed_style_property(prop, style_type)
    
    def _get_non_computed_style_property(self, prop: StyleProperty, style_type: int = StyleType.NORMAL):
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
