from __future__ import annotations

from enum import Enum, auto
from typing import Union

import numpy


class SiColor(Enum):  # Deprecated.
    THEME = auto()
    THEME_TRANSITION_A = auto()
    THEME_TRANSITION_B = auto()

    SVG_NORMAL = auto()
    SVG_THEME = auto()

    TOOLTIP_BG = auto()

    LAYER_DIM = auto()

    INTERFACE_BG_A = auto()
    INTERFACE_BG_B = auto()
    INTERFACE_BG_C = auto()
    INTERFACE_BG_D = auto()
    INTERFACE_BG_E = auto()

    TEXT_A = auto()
    TEXT_B = auto()
    TEXT_C = auto()
    TEXT_D = auto()
    TEXT_E = auto()
    TEXT_THEME = auto()

    TITLE_INDICATOR = auto()
    TITLE_HIGHLIGHT = auto()

    SIDE_MSG_FLASH = auto()
    SIDE_MSG_THEME_NORMAL = auto()
    SIDE_MSG_THEME_SUCCESS = auto()
    SIDE_MSG_THEME_INFO = auto()
    SIDE_MSG_THEME_WARNING = auto()
    SIDE_MSG_THEME_ERROR = auto()

    MENU_BG = auto()

    # 按钮
    # 按钮鼠标相关
    BUTTON_IDLE = auto()
    BUTTON_HOVER = auto()
    BUTTON_FLASH = auto()

    # 按钮外观
    BUTTON_PANEL = auto()
    BUTTON_SHADOW = auto()

    BUTTON_THEMED_BG_A = auto()
    BUTTON_THEMED_BG_B = auto()
    BUTTON_THEMED_SHADOW_A = auto()
    BUTTON_THEMED_SHADOW_B = auto()

    BUTTON_ON = auto()
    BUTTON_OFF = auto()

    BUTTON_TEXT_BUTTON_FLASH = auto()
    BUTTON_TEXT_BUTTON_HOVER = auto()
    BUTTON_TEXT_BUTTON_IDLE = auto()

    # LONG_PRESS_BUTTON
    BUTTON_LONG_PRESS_PANEL = auto()
    BUTTON_LONG_PRESS_SHADOW = auto()
    BUTTON_LONG_PRESS_PROGRESS = auto()

    RADIO_BUTTON_UNCHECKED = auto()
    RADIO_BUTTON_CHECKED = auto()

    CHECKBOX_SVG = auto()
    CHECKBOX_UNCHECKED = auto()
    CHECKBOX_CHECKED = auto()

    # 开关
    SWITCH_DEACTIVATE = auto()
    SWITCH_ACTIVATE = auto()

    # 滚动条
    SCROLL_BAR = auto()

    # 进度条
    PROGRESS_BAR_TRACK = auto()
    PROGRESS_BAR_PROCESSING = auto()
    PROGRESS_BAR_COMPLETING = auto()
    PROGRESS_BAR_PAUSED = auto()
    PROGRESS_BAR_FLASHES = auto()

    @staticmethod
    def RGB_to_RGBA(code: str):
        """
        add alpha channel to an RGB color code
        """
        code_data = code.replace("#", "")
        if len(code_data) == 6:
            return f"#FF{code_data.upper()}"
        if len(code_data) == 8:
            return code.upper()

    @classmethod
    def toArray(cls,
                code: str | tuple,
                to_format: str = "argb"):
        """
        transform `#AARRGGBB` or `#RRGGBB` into `array(A, R, G, B, dtype=int16)`
        if code is already be a list / tuple / ndarray, the method returns ndarray.
        """
        if isinstance(code, numpy.ndarray):
            return code
        if isinstance(code, (list, tuple)):
            return numpy.array(code)

        code = cls.RGB_to_RGBA(code)
        code = code.lstrip("#")
        a, r, g, b = int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16), int(code[6:8], 16)

        to_format = to_format.lower()
        if to_format not in ["rgba", "argb", "rgb"]:
            raise ValueError(f"{to_format} is not a valid format (rgba, argb, rgb)")
        if to_format == "rgba":
            return numpy.array([r, g, b, a], dtype=numpy.int16)
        if to_format == "argb":
            return numpy.array([a, r, g, b], dtype=numpy.int16)
        if to_format == "rgb":
            return numpy.array([r, g, b], dtype=numpy.int16)

    @staticmethod
    def toCode(value: Union[numpy.ndarray, list], force_rgba=False):
        """ transform `array(A, R, G, B, dtype=int16)` into `#AARRGGBB` """
        if len(value) == 3:
            r, g, b = value
            a = 255
        elif len(value) == 4:
            a, r, g, b = value
        else:
            raise ValueError(f"Unexpected shape of input: {value}, shape: {value.shape}")

        if (force_rgba is True) or (a != 255):
            return f"#{int(a):02X}{int(r):02X}{int(g):02X}{int(b):02X}"
        else:
            return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

    @classmethod
    def mix(cls,
            code_fore: str,
            code_post: str,
            weight: float = 0.5):
        """
        Mix the fore color and the post color, you can set the weight of the fore color.
        :return: color code of the mixed color
        """
        fore_array = cls.toArray(code_fore)
        post_array = cls.toArray(code_post)
        mixed_rgb = fore_array * weight + post_array * (1-weight)
        return cls.toCode(mixed_rgb)

    @classmethod
    def trans(cls,
              code: str,
              transparency: float = 0):
        """
        Set the transparency to a color based on current color
        """
        value = cls.toArray(code)
        value_proceed = value * numpy.array([transparency, 1, 1, 1])
        code_proceed = cls.toCode(value_proceed)
        return code_proceed
