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
    filter = [
        FilterToken(FilterType.BRIGHTNESS, 1.20), FilterToken(FilterType.SATURATION, 2)
    ]
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

SLIDER_HOVER_STYLE = StyleSheet(
    background_color=None,
    foreground_color=None,
    text_color=None,
    font_family=None,
    font_size=None,
    border_color=None,
    border_size=None,
    thumb_color=None,
    filter = FilterToken(FilterType.BRIGHTNESS, 0.85)
)

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
    """
    Provides default and hover styles for various UI components.
    Includes methods to retrieve styles by component name.
    """
    Default  = StyleGroup(DEFAULT_STYLE,     DEFAULT_HOVER_STYLE)  # Default style group
    Image    = StyleGroup(IMAGE_STYLE, IMAGE_HOVER_STYLE)          # Style group for images
    Button   = StyleGroup(BUTTON_STYLE,      BUTTON_HOVER_STYLE)   # Style group for buttons
    Header   = StyleGroup(HEADER_STYLE,      HEADER_HOVER_STYLE)   # Style group for headers
    Dropdown = StyleGroup(DROPDOWN_STYLE,    DROPDOWN_HOVER_STYLE) # Style group for dropdowns
    Slider   = StyleGroup(SLIDER_STYLE,      SLIDER_HOVER_STYLE)   # Style group for sliders
    Panel    = StyleGroup(PANEL_STYLE,       PANEL_HOVER_STYLE)    # Style group for panels
    
    @staticmethod
    def get_by_component_name(component_name: str = "DEFAULT") -> StyleGroup:
        """
        Retrieves the style group for a given component name.
        Defaults to the general Default style group if no match is found.
        """
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

