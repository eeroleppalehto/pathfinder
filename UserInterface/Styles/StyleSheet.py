from __future__ import annotations
import typing

import pygame
from .StyleEnums import StyleType
from typing import Optional, Union
from .StyleFilters import FilterToken, FilterType, brightness, apply_filter, apply_all_filters
from .StyleEnums import StyleProperty

if typing.TYPE_CHECKING:
    from .StyleManager import ComponentStyleManager


pygame.font.init()

class _Default:
    pass

DEFAULT = _Default()



class StyleSheet:
    """
    Represents a collection of style properties for UI components.
    Allows customization of colors, fonts, borders, and filters.
    Provides methods to update and manage style properties dynamically.
    """
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
        text_align: Optional[str] = "left",
        filter: Optional[Union[list[FilterToken], FilterToken]] = DEFAULT
    ):
        filter_is_not_in_list = filter != None and filter != DEFAULT and not isinstance(filter, list)
        if(filter_is_not_in_list):
            self._filter = [filter]
        else:
            self._filter = filter
    

        self._font_family = font_family
        self._font_size = font_size
        
        self._background_color = background_color
        self._foreground_color = foreground_color
        self._text_color = text_color
        self._border_color = border_color
        self._thumb_color = thumb_color
        self.border_size = border_size
        self.text_align = text_align
        self._objects_using_this_style = []
        
        if self._font_size != None and self._font_size > 0:
            family = None if self._font_family is DEFAULT else self._font_family
            self._font = pygame.font.Font(family, self._font_size)

    
    
    def update_style_property(self, stylesheet, style_property: StyleProperty, value: tuple[int, int, int]):
        """
        Updates a specific style property for all objects using this stylesheet.
        Notifies the associated style manager of the change.
        """
        for object in self._objects_using_this_style:
            style_manager: ComponentStyleManager = object.style_manager
            style_manager.update_computed_style(stylesheet, style_property, value)

    def add_to_object_references(self, object):
        """
        Adds a reference to an object that uses this stylesheet.
        """
        if object not in self._objects_using_this_style:
            self._objects_using_this_style.append(object)

    def remove_from_object_refereces(self, object):
        """
        Removes a reference to an object that uses this stylesheet.
        """
        if object in self._objects_using_this_style:
            self._objects_using_this_style.remove(object)

    def computed_styles_exist(self):
        return self._filter != None
     # —— filter property —— #
    @property
    def filter(self) -> list[FilterToken] | None:
        return self._filter
    
    @filter.setter
    def filter(self, filter_token: Optional[Union[list[FilterToken], FilterToken]] = DEFAULT):
        """
        Sets the filter property. If a single filter token is provided, wraps it in a list.
        Triggers a recomputation of colors based on the new filter.
        """
        if filter_token == None or filter_token == DEFAULT:
            return
        
        if isinstance(filter_token, list):
            self._filter = FilterToken
        else:
            self._filter = [filter_token]

        return self._compute_colors()
        
    # —— background_color property —— #
    @property
    def background_color(self) -> Optional[tuple[int, int, int]]:
        return self._background_color
    
    @background_color.setter
    def background_color(self, value: Optional[tuple[int, int, int]]):
        self._background_color = value
        self.update_style_property(self, StyleProperty.BACKGROUND_COLOR, value)

    # —— thumb_color property —— #
    @property
    def thumb_color(self) -> Optional[tuple[int, int, int]]:
        return self._thumb_color

    @thumb_color.setter
    def thumb_color(self, value: Optional[tuple[int,int,int]]):
        self._thumb_color = value
        self.update_style_property(self, StyleProperty.THUMB_COLOR, value)
        
    # —— foreground_color property —— #
    @property
    def foreground_color(self) -> Optional[tuple[int, int, int]]:
        return self._foreground_color
    
    @foreground_color.setter
    def foreground_color(self, value: Optional[tuple[int, int, int]]):
        self._foreground_color = value
        self.update_style_property(self, StyleProperty.FOREGROUND_COLOR, value)
        
   
    # —— text_color property —— #
    @property
    def text_color(self) -> Optional[tuple[int, int, int]]:
        return self._text_color
    
    @text_color.setter
    def text_color(self, value: Optional[tuple[int, int, int]]):
        self._text_color = value
        self.update_style_property(self, StyleProperty.TEXT_COLOR, value)
        
   
    # —— border_color property —— #
    @property
    def border_color(self) -> Optional[tuple[int, int, int]]:
        return self._border_color
    
    @border_color.setter
    def border_color(self, value: Optional[tuple[int, int, int]]):
        self._border_color = value
        self.update_style_property(self, StyleProperty.BORDER_COLOR, value)
        
   
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
    """
    Represents a group of styles for different states of a UI component.
    Typically includes styles for normal and hover states.
    """
    def __init__(self, normal: StyleSheet, hover: StyleSheet):
        self.normal = normal
        self.hover = hover

    def get(self, style_type: int) -> StyleSheet:
        return self.normal if style_type == StyleType.NORMAL else self.hover
