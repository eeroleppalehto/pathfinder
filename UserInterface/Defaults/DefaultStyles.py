from UserInterface.Styles.StyleSheet import StyleSheet, StyleGroup
from UserInterface.Styles.StyleFilters import FilterToken, FilterType

DEFAULT_STYLE = StyleSheet(
    background_color=(248, 250, 252),         # soft cool white
    foreground_color=(99, 155, 255),           # vibrant blue
    text_color=(34, 34, 34),                  # high-contrast primary text
    font_family=None,
    font_size=20,
    border_color=(225, 230, 240),             # soft cool border
    border_size=1,
    thumb_color=(99, 155, 255)
)

DEFAULT_HOVER_STYLE = StyleSheet(
    background_color=None,
    foreground_color=None,
    text_color=None,
    font_family=None,
    font_size=None,
    border_color=None,
    border_size=None,
    thumb_color=None,
    filter = None
)

BUTTON_STYLE = StyleSheet(
    background_color=(0, 120, 215),    
    foreground_color=(255, 255, 255),
    text_color=(255, 255, 255),
    font_size=20,
    border_color=(0, 105, 200),
    border_size=0,
    thumb_color=(0, 105, 200),
    filter = None
)

BUTTON_HOVER_STYLE = StyleSheet(
    background_color=None,
    foreground_color=None,
    text_color=None,
    font_family=None,
    font_size=None,
    border_color=None,
    border_size=3,
    thumb_color=(0, 90, 185),
    filter = [FilterToken(FilterType.BRIGHTNESS, 1.20), FilterToken(FilterType.SATURATION, 2)]
)

HEADER_STYLE = StyleSheet(
    background_color=None,
    foreground_color=None,
    text_color=(20, 20, 20),
    font_size=30,                             # larger header
    border_color=None,
    border_size=0,
    filter = None
)

HEADER_HOVER_STYLE = HEADER_STYLE

DROPDOWN_STYLE = StyleSheet(
    background_color=(255, 255, 255),
    foreground_color=None,
    text_color=(50, 50, 50),
    font_size=20,
    border_color=(215, 220, 230),
    border_size=1,
    thumb_color=(0, 120, 215),
    filter = None
)

DROPDOWN_HOVER_STYLE = DEFAULT_HOVER_STYLE

SLIDER_STYLE = StyleSheet(
    background_color=(225, 230, 240),
    foreground_color=(99, 155, 255),
    text_color=(0, 0, 0),
    font_size=20,
    border_color=(200, 210, 225),
    border_size=2,
    thumb_color=(0, 120, 215),
    filter = None
)

SLIDER_HOVER_STYLE = DEFAULT_HOVER_STYLE

PANEL_STYLE = StyleSheet(
    background_color=(250, 251, 253),
    foreground_color=None,
    text_color=None,
    font_size=20,
    border_color=(220, 225, 235),
    border_size=1,
    filter = None
)

PANEL_HOVER_STYLE = DEFAULT_HOVER_STYLE

IMAGE_STYLE = StyleSheet(
    background_color=None,
    foreground_color=None,
    text_color=None,
    font_family=None,
    font_size=0,
    border_color=None,
    border_size=0,
    thumb_color=None,
    filter =  None
)

IMAGE_HOVER_STYLE = DEFAULT_HOVER_STYLE

class DefaultStyles:
    Default  = StyleGroup(DEFAULT_STYLE,     DEFAULT_HOVER_STYLE)
    Image    = StyleGroup(IMAGE_STYLE, IMAGE_HOVER_STYLE)
    Button   = StyleGroup(BUTTON_STYLE,      BUTTON_HOVER_STYLE)
    Header   = StyleGroup(HEADER_STYLE,      HEADER_HOVER_STYLE)
    Dropdown = StyleGroup(DROPDOWN_STYLE,    DROPDOWN_HOVER_STYLE)
    Slider   = StyleGroup(SLIDER_STYLE,      SLIDER_HOVER_STYLE)
    Panel    = StyleGroup(PANEL_STYLE,       PANEL_HOVER_STYLE)
    
    @staticmethod
    def get_by_component_name(component_name: str = "DEFAULT") -> StyleGroup:
        if component_name == "BUTTON":
            return DefaultStyles.Button
        if component_name == "HEADER":
            return DefaultStyles.Header
        if component_name == "DROPDOWN" or component_name == "DROPDOWN ITEM":
            return DefaultStyles.Dropdown
        if component_name == "SLIDER":
            return DefaultStyles.Slider
        if component_name == "PANEL":
            return DefaultStyles.Panel
        if component_name == "IMAGE":
            return DefaultStyles.Image
        
        return DefaultStyles.Default

