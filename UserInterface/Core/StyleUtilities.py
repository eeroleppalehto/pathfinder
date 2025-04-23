from UserInterface.Styles.StyleEnums import StyleType
from UserInterface.Styles.StyleSheet import StyleSheet

def apply_style_to_components(style_type: int, style_sheet: StyleSheet, components: list):
    if style_type == StyleType.NORMAL:
        for component in components:
            component.set_style(style_sheet)
    else:
        for component in components:
            component.set_hover_style(style_sheet)
