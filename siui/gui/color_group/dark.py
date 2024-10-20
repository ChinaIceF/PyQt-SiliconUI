
from siui.core import SiColor

from .color_group import SiColorGroup


class DarkColorGroup(SiColorGroup):
    def __init__(self):
        super().__init__()

        self.assign(SiColor.THEME, "#855198")
        self.assign(SiColor.THEME_TRANSITION_A, "#52389a")
        self.assign(SiColor.THEME_TRANSITION_B, "#9c4e8b")

        self.assign(SiColor.SVG_NORMAL, "#DFDFDF")
        self.assign(SiColor.SVG_THEME, "#855198")

        self.assign(SiColor.LAYER_DIM, "#60000000")

        self.assign(SiColor.TOOLTIP_BG, "#ef4C4554")

        self.assign(SiColor.INTERFACE_BG_A, "#1C191F")
        self.assign(SiColor.INTERFACE_BG_B, "#25222A")
        self.assign(SiColor.INTERFACE_BG_C, "#332E38")
        self.assign(SiColor.INTERFACE_BG_D, "#403a46")
        self.assign(SiColor.INTERFACE_BG_E, "#4C4554")

        self.assign(SiColor.TEXT_A, "#E5E5E5")
        self.assign(SiColor.TEXT_B, "#DFDFDF")
        self.assign(SiColor.TEXT_C, "#C7C7C7")
        self.assign(SiColor.TEXT_D, "#AFAFAF")
        self.assign(SiColor.TEXT_E, "#979797")
        self.assign(SiColor.TEXT_THEME, "#c58bc2")

        self.assign(SiColor.SIDE_MSG_FLASH, "#90FFFFFF")
        self.assign(SiColor.SIDE_MSG_THEME_NORMAL, "#4C4554")
        self.assign(SiColor.SIDE_MSG_THEME_SUCCESS, "#519868")
        self.assign(SiColor.SIDE_MSG_THEME_INFO, "#855198")
        self.assign(SiColor.SIDE_MSG_THEME_WARNING, "#986351")
        self.assign(SiColor.SIDE_MSG_THEME_ERROR, "#98515b")

        self.assign(SiColor.MENU_BG, "#332E38")

        # 标题相关
        self.assign(SiColor.TITLE_INDICATOR, "#c58bc2")
        self.assign(SiColor.TITLE_HIGHLIGHT, "#52324E")

        # 按钮鼠标相关
        self.assign(SiColor.BUTTON_IDLE, "#00FFFFFF")
        self.assign(SiColor.BUTTON_HOVER, "#10FFFFFF")
        self.assign(SiColor.BUTTON_FLASH, "#20FFFFFF")

        # 按钮外观
        self.assign(SiColor.BUTTON_PANEL, "#4C4554")
        self.assign(SiColor.BUTTON_SHADOW, SiColor.mix(self.fromToken(SiColor.INTERFACE_BG_C), "#000000", 0.9))

        self.assign(SiColor.BUTTON_THEMED_BG_A, "#52389a")
        self.assign(SiColor.BUTTON_THEMED_BG_B, "#9c4e8b")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_A, "#372456")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_B, "#562b49")

        self.assign(SiColor.BUTTON_ON, "#372456")
        self.assign(SiColor.BUTTON_OFF, "#562b49")

        self.assign(SiColor.RADIO_BUTTON_UNCHECKED, "#211F25")
        self.assign(SiColor.RADIO_BUTTON_CHECKED, "#9c65ae")

        self.assign(SiColor.CHECKBOX_SVG, "#1C191F")
        self.assign(SiColor.CHECKBOX_UNCHECKED, "#979797")
        self.assign(SiColor.CHECKBOX_CHECKED, "#9c65ae")

        self.assign(SiColor.BUTTON_TEXT_BUTTON_IDLE, "#c58bc2")
        self.assign(SiColor.BUTTON_TEXT_BUTTON_FLASH, "#c58bc2")
        self.assign(SiColor.BUTTON_TEXT_BUTTON_HOVER, "#fabef8")

        # 长按按钮
        self.assign(SiColor.BUTTON_LONG_PRESS_PANEL, "#932a48")
        self.assign(SiColor.BUTTON_LONG_PRESS_SHADOW, "#642d41")
        self.assign(SiColor.BUTTON_LONG_PRESS_PROGRESS, "#DA3462")

        # 开关
        self.assign(SiColor.SWITCH_DEACTIVATE, "#D2D2D2")
        self.assign(SiColor.SWITCH_ACTIVATE, "#100912")

        # 滚动条
        self.assign(SiColor.SCROLL_BAR, "#50FFFFFF")

        # 进度条
        self.assign(SiColor.PROGRESS_BAR_TRACK, "#252229")
        self.assign(SiColor.PROGRESS_BAR_PROCESSING, "#66CBFF")
        self.assign(SiColor.PROGRESS_BAR_COMPLETING, "#FED966")
        self.assign(SiColor.PROGRESS_BAR_PAUSED, "#7F7F7F")
        self.assign(SiColor.PROGRESS_BAR_FLASHES, "#FFFFFF")
