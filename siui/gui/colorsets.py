from siui.core.color import Color
from enum import Enum, auto
from typing import Union
import numpy


class SiColor(Enum):
    THEME = auto()
    THEME_TRANSITION_A = auto()
    THEME_TRANSITION_B = auto()
    # TODO: add more enum items

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
                code: str):
        """
        transform `#AARRGGBB` or `#RRGGBB` into `array(A, R, G, B, dtype=int16)`
        """
        code = cls.RGB_to_RGBA(code)
        code = code.lstrip("#")
        a, r, g, b = int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16), int(code[6:8], 16)
        return numpy.array([a, r, g, b], dtype=numpy.int16)

    @staticmethod
    def toCode(value: Union[numpy.ndarray, list]):
        """
        transform `array(A, R, G, B, dtype=int16)` into `#AARRGGBB`
        """
        if len(value) == 3:
            r, g, b = value
            a = 255
        elif len(value) == 4:
            a, r, g, b = value
        else:
            raise ValueError(f"意外的输入值形状{value.shape}")

        return f"#{int(a):02X}{int(r):02X}{int(g):02X}{int(b):02X}"

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

    @staticmethod
    def trans(code: str,
              transparency: float = 0):
        """
        Set the transparency to a color based on current color
        """
        value = Color.decodeColor(code)
        value_proceed = value * numpy.array([transparency, 1, 1, 1])
        code_proceed = Color.encodeColor(value_proceed)
        return code_proceed


class ColorsetDark:
    colors = {}

    # ============= 框架 =============
    # SVG 颜色
    colors["SVG_A"] = "#FFFFFF"

    # 主题色
    colors["THEME"] = "#855198"

    # 过渡主题色
    colors["THEME_TRANSITION_A"] = "#52389a"
    colors["THEME_TRANSITION_B"] = "#9c4e8b"

    # 工具提示
    colors["TOOLTIP_BG"] = "#ef413a47"  # 背景色

    # 界面背景色
    colors["INTERFACE_BG_A"] = "#1C191F"
    colors["INTERFACE_BG_B"] = "#252229"
    colors["INTERFACE_BG_C"] = "#2C2930"
    colors["INTERFACE_BG_D"] = "#3b373f"
    colors["INTERFACE_BG_E"] = "#49454D"

    # 文字颜色
    colors["TEXT_A"] = "#FFFFFF"
    colors["TEXT_B"] = "#DFDFDF"
    colors["TEXT_C"] = "#CFCFCF"
    colors["TEXT_D"] = "#AFAFAF"

    # 标题相关
    colors["TITLE_INDICATOR"] = "#c58bc2"
    colors["TITLE_HIGHLIGHT"] = "#52324E"


    # ============= 控件 =============
    # 按钮
    # 按钮鼠标相关
    colors["BUTTON_IDLE"] = "#00FFFFFF"
    colors["BUTTON_HOVER"] = "#10FFFFFF"
    colors["BUTTON_FLASH"] = "#20FFFFFF"

    # 按钮外观 - PUSHBUTTON
    colors["BUTTON_NORMAL_BG"] = colors["INTERFACE_BG_E"]
    colors["BUTTON_NORMAL_SHADOW"] = Color.mix(colors["INTERFACE_BG_C"], "#000000", 0.9)

    colors["BUTTON_THEMED_BG_A"] = "#52389a"
    colors["BUTTON_THEMED_BG_B"] = "#9c4e8b"
    colors["BUTTON_THEMED_SHADOW_A"] = "#372456"
    colors["BUTTON_THEMED_SHADOW_B"] = "#562b49"

    # LONGPRESSBUTTON
    colors["BUTTON_LONG_BG"] = "#9F3652"
    colors["BUTTON_LONG_SHADOW"] = "#6a3246"
    colors["BUTTON_LONG_PROGRESS"] = "#DA3462"

    # 开关
    colors["SWITCH_DEACTIVATE"] = "#D2D2D2"
    colors["SWITCH_ACTIVATE"] = "#100912"

    # 滚动条
    colors["SCROLL_BAR"] = "#50FFFFFF"

    # 进度条
    colors["PROGRESSBAR_LOADING"] = "#66CBFF"
    colors["PROGRESSBAR_PROCESSING"] = "#FED966"
    colors["PROGRESSBAR_PAUSED"] = "#7F7F7F"
    colors["PROGRESSBAR_FLASHES"] = "#FFFFFF"

class SiColorDark(Color):
    # ========== 全局颜色 ==========
    # SVG 默认颜色
    SVG_HEX = "#FFFFFF"

    # 主题色
    THEME_HEX = [
        "#52389a",
        "#9c4e8b",
    ]

    # 提示框颜色
    TOOLTIP_HEX = [
        "#FFFFFF",  # 文字颜色
        "#ef413a47"  # 背景颜色
    ]

    # 背景色的几个等级，小指数为父
    BG_GRAD_HEX = [
        "#1C191F",
        "#252229",
        "#2C2930",
        "#3b373f",
        "#49454D",
    ]

    # 文字颜色的几个等级，小指数为父
    TEXT_GRAD_HEX = [
        "#FFFFFF",
        "#DFDFDF",
        "#CFCFCF",
        "#AFAFAF",
    ]

    # ========== 控件颜色 ==========
    # 按钮
    BTN_NORM_TEXT_HEX = TEXT_GRAD_HEX[1]
    BTN_NORM_HEX = [
        BG_GRAD_HEX[4],  # 正常
        Color.mix(BG_GRAD_HEX[2], "#000000", 0.9),  # 阴影
    ]

    BTN_HL_TEXT_HEX = "#FFFFFF"
    BTN_HL_HEX = [
        "#52389a",  # 正常
        "#9c4e8b",
        "#372456",  # 阴影
        "#562b49",
    ]

    BTN_HOLD_TEXT_HEX = TEXT_GRAD_HEX[1]
    BTN_HOLD_HEX = [
        "#DA3462",  # 长按时
        "#9F3652",  # 闲置
        "#6a3246",  # 阴影
    ]

    # 开关
    SWC_HEX = [
        "#D2D2D2",  # 关闭
        "#100912",  # 开启
    ]

    # 提示框
    INF_HEX = [
        "#6b39a8",  # 提示
        "#338145",  # 已完成
        "#a87539",  # 警告
        "#a83e39",  # 错误
    ]

    # ========== GLAZE 颜色 ==========
    # 框架
    FRM_TEXT_HEX = TEXT_GRAD_HEX[0]

    # 组
    STK_TEXT_HEX = TEXT_GRAD_HEX[0]
    STK_HL_HEX = "#609c4e8b"

    # 选项
    OPT_TITLE_HEX = TEXT_GRAD_HEX[0]
    OPT_DESCRIPTION_HEX = TEXT_GRAD_HEX[3]
