from enum import IntEnum, auto
from typing import Optional

class FilterType(IntEnum):
    START      = auto()
    BRIGHTNESS = auto()
    CONTRAST   = auto()
    SATURATION = auto()
    TINT       = auto()
    END        = auto()


class FilterToken:
    def __init__(self, filter_type: FilterType, value: float):
        self.type  = filter_type
        self.value = value


def _apply_brightness_filter(color: tuple[int, int, int], filter_token: FilterToken) -> tuple[int, int, int]:
    if filter_token.type is not FilterType.BRIGHTNESS:
        raise ValueError("FilterToken must be of type BRIGHTNESS")

    brightness = filter_token.value
    if brightness < 0.0:
        brightness = 0.0

    if brightness == 1.0:
        return color

    red, green, blue = color

    if brightness < 1.0:
        new_red   = int(red   * brightness)
        new_green = int(green * brightness)
        new_blue  = int(blue  * brightness)
    else:
        amount = brightness - 1.0
        new_red   = int(red   + (255 - red)   * amount)
        new_green = int(green + (255 - green) * amount)
        new_blue  = int(blue  + (255 - blue)  * amount)

    return (min(255, max(0, new_red)), min(255, max(0, new_green)), min(255, max(0, new_blue)))


def _apply_contrast_filter( color: tuple[int, int, int], filter_token: FilterToken) -> tuple[int, int, int]:
    if filter_token.type is not FilterType.CONTRAST:
        raise ValueError("FilterToken must be of type CONTRAST")
    
    contrast = filter_token.value
    if contrast < 0.0:
        contrast = 0.0
    if contrast == 1.0:
        return color

    red, green, blue = color
    midpoint = 128

    new_red   = int(midpoint + (red   - midpoint)   * contrast)
    new_green = int(midpoint + (green - midpoint)   * contrast)
    new_blue  = int(midpoint + (blue  - midpoint)   * contrast)

    return (min(255, max(0, new_red)), min(255, max(0, new_green)), min(255, max(0, new_blue)))

def _apply_saturation_filter(
    color: tuple[int, int, int],
    filter_token: FilterToken
) -> tuple[int, int, int]:
    if filter_token.type is not FilterType.SATURATION:
        raise ValueError("FilterToken must be of type SATURATION")

    saturation_factor = filter_token.value
    if saturation_factor < 0.0:
        saturation_factor = 0.0

    if saturation_factor == 1.0:
        return color

    red, green, blue = color

    # Rec. 709 luminance
    luminance = int(
        0.2126 * red +
        0.7152 * green +
        0.0722 * blue
    )

    new_red   = int(luminance + (red   - luminance)   * saturation_factor)
    new_green = int(luminance + (green - luminance)   * saturation_factor)
    new_blue  = int(luminance + (blue  - luminance)   * saturation_factor)

    return (min(255, max(0, new_red)), min(255, max(0, new_green)), min(255, max(0, new_blue)))


def _apply_tint_filter(
    color: tuple[int, int, int],
    filter_token: FilterToken
) -> tuple[int, int, int]:
    if filter_token.type is not FilterType.TINT:
        raise ValueError("FilterToken must be of type TINT")

    tint_color, tint_factor = filter_token.value
    if tint_factor < 0.0:
        tint_factor = 0.0

    if tint_factor == 0.0:
        return color
    if tint_factor >= 1.0:
        return tint_color

    red, green, blue = color
    tint_red, tint_green, tint_blue = tint_color

    new_red   = int(red   + (tint_red   - red)   * tint_factor)
    new_green = int(green + (tint_green - green) * tint_factor)
    new_blue  = int(blue  + (tint_blue  - blue)  * tint_factor)

    return (min(255, max(0, new_red)), min(255, max(0, new_green)), min(255, max(0, new_blue)))


# --- wire up the filters ---
filter_functions: list[Optional[callable]] = [None] * FilterType.END
filter_functions[FilterType.BRIGHTNESS] = _apply_brightness_filter
filter_functions[FilterType.CONTRAST]   = _apply_contrast_filter
filter_functions[FilterType.SATURATION] = _apply_saturation_filter
filter_functions[FilterType.TINT] = _apply_tint_filter


def brightness(value: float) -> FilterToken:
    return FilterToken(FilterType.BRIGHTNESS, value)

def contrast(value: float) -> FilterToken:
    return FilterToken(FilterType.CONTRAST, value)

def saturation(value: float) -> FilterToken:
    return FilterToken(FilterType.SATURATION, value)

def tint(tint_color: tuple[int, int, int], tint_amount: float) -> FilterToken:
    return FilterToken(FilterType.TINT, (tint_color, tint_amount))


def apply_filter(color: Optional[tuple[int, int, int]], filter_token: FilterToken) -> Optional[tuple[int, int, int]]:
    if (
        color is None
        or not isinstance(color, tuple)
        or filter_token.type <= FilterType.START
        or filter_token.type >= FilterType.END
    ):
        return color

    filter_function = filter_functions[filter_token.type]
    return filter_function(color, filter_token)


def apply_all_filters(color: Optional[tuple[int, int, int]],filter_tokens: Optional[list[FilterToken]]) -> Optional[tuple[int, int, int]]:
    if color is None or not isinstance(color, tuple) or not filter_tokens:
        return color

    result_color = color
    for current_token in filter_tokens:
        if current_token.type <= FilterType.START or current_token.type >= FilterType.END:
            continue
        filter_function = filter_functions[current_token.type]
        result_color = filter_function(result_color, current_token)

    return result_color
