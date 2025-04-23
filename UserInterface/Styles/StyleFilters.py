from enum import IntEnum, auto
from typing import Optional, Union

class FilterType(IntEnum):
    START = auto()
    BRIGHTNESS = auto()
    END = auto()


class FilterToken:
    def __init__(self, ftype: FilterType, value: float):
        self.type = ftype
        self.value = value

def _apply_brightness_filter(color: tuple[int, int, int], token: FilterToken) -> tuple[int, int, int]:
    if token.type != FilterType.BRIGHTNESS:
        raise ValueError("FilterToken must be of type BRIGHTNESS")

    multiplier = max(0.0, token.value) 
    red, green, blue = color
    red = min(int(red * multiplier), 255)
    green = min(int(green * multiplier), 255)
    blue = min(int(blue * multiplier), 255)
    return (red, green, blue)


_filter_functions:list[callable] = [None] * FilterType.END
_filter_functions[FilterType.BRIGHTNESS] = _apply_brightness_filter



def brightness(value: float) -> FilterToken:
    return FilterToken(FilterType.BRIGHTNESS, value)

def apply_filter(color: Optional[tuple[int, int, int]], filter_token: FilterToken):
    if (
        color == None
        or isinstance(color, tuple) == False
        or filter_token.type <= FilterType.START 
        or filter_token.type >= FilterType.END
    ):
        return color
    
    filter_function:callable | None = _filter_functions[filter_token.type] 
    return filter_function(color, filter_token)

def apply_all_filters(color: Optional[tuple[int, int, int]], filter_tokens: Optional[list[FilterToken]]):
    if(filter_tokens == None or color == None or isinstance(color, tuple) == False):
        return color
    
    computed_color = color
    for token in filter_tokens:
        if (token.type <= FilterType.START or token.type >= FilterType.END):
            return
        
        filter_function:callable = _filter_functions[token.type] 
        computed_color = filter_function(computed_color, token)

    return computed_color
