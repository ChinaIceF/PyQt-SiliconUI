
from siui.core.color import SiColor


class SiColorGroup:
    def __getitem__(self, item):
        return self.colors[item]

    def __init__(self,
                 overwrite=None,
                 reference=None):

        self.valid_state = True
        self.colors = {}

        if overwrite is not None:
            self.overwrite(overwrite)
            if reference is None:
                self.reference = overwrite.reference
            else:
                self.reference = reference
        else:
            self.reference = reference

    def assign(self, token, code):
        self.colors[token.name] = code

    def remove(self, token):
        if token.name in self.colors.keys():
            self.colors.pop(token.name)

    def fromToken(self, token):
        if token.name in self.colors.keys() and self.valid_state:
            return self.colors[token.name]
        if self.reference is None:
            raise ValueError(
                f"Color under token {token.name} is not assigned yet either in this group or in its reference\n"
                f"Valid state: {self.valid_state}"
            )
        else:
            return self.reference.fromToken(token)

    def isAssigned(self, token):
        if self.reference is None:
            return token.name in self.colors.keys()
        else:
            return ((token.name in self.colors.keys()) and self.valid_state) or self.reference.isAssigned(token)

    def overwrite(self, color_group):
        self.colors.update(color_group.colors)

    def setReference(self, color_group):
        self.reference = color_group

    def setValid(self, state):
        self.valid_state = state

    def isValid(self):
        return self.valid_state


class DarkColorGroup(SiColorGroup):
    def __init__(self):
        super().__init__()

        self.assign(SiColor.THEME, "#855198")
        self.assign(SiColor.THEME_TRANSITION_A, "#52389a")
        self.assign(SiColor.THEME_TRANSITION_B, "#9c4e8b")

        self.assign(SiColor.SVG_NORMAL, "#FFFFFF")
        self.assign(SiColor.SVG_THEME, "#855198")

        self.assign(SiColor.TOOLTIP_BG, "#ef413a47")

        self.assign(SiColor.INTERFACE_BG_A, "#1C191F")
        self.assign(SiColor.INTERFACE_BG_B, "#252229")
        self.assign(SiColor.INTERFACE_BG_C, "#2C2930")
        self.assign(SiColor.INTERFACE_BG_D, "#3b373f")
        self.assign(SiColor.INTERFACE_BG_E, "#49454D")

        self.assign(SiColor.TEXT_A, "#FFFFFF")
        self.assign(SiColor.TEXT_B, "#DFDFDF")
        self.assign(SiColor.TEXT_C, "#C7C7C7")
        self.assign(SiColor.TEXT_D, "#AFAFAF")
        self.assign(SiColor.TEXT_E, "#979797")

        # 标题相关
        self.assign(SiColor.TITLE_INDICATOR, "#c58bc2")
        self.assign(SiColor.TITLE_HIGHLIGHT, "#52324E")

        # 按钮
        self.assign(SiColor.BUTTON_IDLE, "#00FFFFFF")
        self.assign(SiColor.BUTTON_HOVER, "#10FFFFFF")

        # 按钮鼠标相关
        self.assign(SiColor.BUTTON_IDLE, "#00FFFFFF")
        self.assign(SiColor.BUTTON_HOVER, "#10FFFFFF")
        self.assign(SiColor.BUTTON_FLASH, "#20FFFFFF")

        # 按钮外观
        self.assign(SiColor.BUTTON_BG, "#49454D")
        self.assign(SiColor.BUTTON_SHADOW, SiColor.mix(self.fromToken(SiColor.INTERFACE_BG_C), "#000000", 0.9))

        self.assign(SiColor.BUTTON_THEMED_BG_A, "#52389a")
        self.assign(SiColor.BUTTON_THEMED_BG_B, "#9c4e8b")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_A, "#372456")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_B, "#562b49")

        # 长按按钮
        self.assign(SiColor.BUTTON_LONG_PRESS_BG, "#9F3652")
        self.assign(SiColor.BUTTON_LONG_PRESS_SHADOW, "#6a3246")
        self.assign(SiColor.BUTTON_LONG_PRESS_PROGRESS, "#DA3462")

        # 开关
        self.assign(SiColor.SWITCH_DEACTIVATE, "#D2D2D2")
        self.assign(SiColor.SWITCH_ACTIVATE, "#100912")

        # 滚动条
        self.assign(SiColor.SCROLL_BAR, "#50FFFFFF")

        # 进度条
        self.assign(SiColor.PROGRESS_BAR_LOADING, "#66CBFF")
        self.assign(SiColor.PROGRESS_BAR_PROCESSING, "#FED966")
        self.assign(SiColor.PROGRESS_BAR_PAUSED, "#7F7F7F")
        self.assign(SiColor.PROGRESS_BAR_FLASHES, "#FFFFFF")


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

    # ============= 控件 =============

    # 标题相关
    colors["TITLE_INDICATOR"] = "#c58bc2"
    colors["TITLE_HIGHLIGHT"] = "#52324E"

    # 按钮
    # 按钮鼠标相关
    colors["BUTTON_IDLE"] = "#00FFFFFF"
    colors["BUTTON_HOVER"] = "#10FFFFFF"
    colors["BUTTON_FLASH"] = "#20FFFFFF"

    # 按钮外观 - PUSHBUTTON
    colors["BUTTON_NORMAL_BG"] = colors["INTERFACE_BG_E"]
    colors["BUTTON_NORMAL_SHADOW"] = SiColor.mix(colors["INTERFACE_BG_C"], "#000000", 0.9)

    colors["BUTTON_THEMED_BG_A"] = "#52389a"
    colors["BUTTON_THEMED_BG_B"] = "#9c4e8b"
    colors["BUTTON_THEMED_SHADOW_A"] = "#372456"
    colors["BUTTON_THEMED_SHADOW_B"] = "#562b49"

    # LONGPRESSBUTTON
    colors["BUTTON_LONG_PRESS_BG"] = "#9F3652"
    colors["BUTTON_LONG_PRESS_SHADOW"] = "#6a3246"
    colors["BUTTON_LONG_PRESS_PROGRESS"] = "#DA3462"

    # 开关
    colors["SWITCH_DEACTIVATE"] = "#D2D2D2"
    colors["SWITCH_ACTIVATE"] = "#100912"

    # 滚动条
    colors["SCROLL_BAR"] = "#50FFFFFF"

    # 进度条
    colors["PROGRESS_BAR_LOADING"] = "#66CBFF"
    colors["PROGRESS_BAR_PROCESSING"] = "#FED966"
    colors["PROGRESS_BAR_PAUSED"] = "#7F7F7F"
    colors["PROGRESS_BAR_FLASHES"] = "#FFFFFF"
