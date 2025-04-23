import enum

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
    TEXT_ALIGN = 256
    END = 512

    def get_index(self):
        if self == StyleProperty.NONE:
            return -1
        return self.bit_length() - 1
