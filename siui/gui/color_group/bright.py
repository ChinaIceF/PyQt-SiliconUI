
from siui.core import SiColor

from .color_group import SiColorGroup


class BrightColorGroup(SiColorGroup):
    def __init__(self):
        super().__init__()

        self.assign(SiColor.THEME, "#2accb3")
        self.assign(SiColor.THEME_TRANSITION_A, "#2abed8")
        self.assign(SiColor.THEME_TRANSITION_B, "#2ad98e")

        self.assign(SiColor.SVG_NORMAL, "#494f4d")
        self.assign(SiColor.SVG_THEME, "#53857d")

        self.assign(SiColor.LAYER_DIM, "#60000000")

        self.assign(SiColor.TOOLTIP_BG, "#eff9f9f9")

        self.assign(SiColor.INTERFACE_BG_A, "#d6d6d6")
        self.assign(SiColor.INTERFACE_BG_B, "#dddddd")
        self.assign(SiColor.INTERFACE_BG_C, "#e5e5e5")
        self.assign(SiColor.INTERFACE_BG_D, "#eeeeee")
        self.assign(SiColor.INTERFACE_BG_E, "#f6f6f6")

        self.assign(SiColor.TEXT_A, "#171d1b")
        self.assign(SiColor.TEXT_B, "#2e3432")
        self.assign(SiColor.TEXT_C, "#363d3b")
        self.assign(SiColor.TEXT_D, "#3f4644")
        self.assign(SiColor.TEXT_E, "#494f4d")
        self.assign(SiColor.TEXT_THEME, "#237165")

        self.assign(SiColor.SIDE_MSG_FLASH, "#90FFFFFF")
        self.assign(SiColor.SIDE_MSG_THEME_NORMAL, "#242027")
        self.assign(SiColor.SIDE_MSG_THEME_SUCCESS, "#519868")
        self.assign(SiColor.SIDE_MSG_THEME_INFO, "#855198")
        self.assign(SiColor.SIDE_MSG_THEME_WARNING, "#986351")
        self.assign(SiColor.SIDE_MSG_THEME_ERROR, "#98515b")

        self.assign(SiColor.MENU_BG, "#e5e5e5")

        # 标题相关
        self.assign(SiColor.TITLE_INDICATOR, "#2accb3")
        self.assign(SiColor.TITLE_HIGHLIGHT, "#b4ceca")

        # 按钮鼠标相关
        self.assign(SiColor.BUTTON_IDLE, "#00FFFFFF")
        self.assign(SiColor.BUTTON_HOVER, "#10FFFFFF")
        self.assign(SiColor.BUTTON_FLASH, "#20FFFFFF")

        # 按钮外观
        self.assign(SiColor.BUTTON_PANEL, "#f6f6f6")
        self.assign(SiColor.BUTTON_SHADOW, SiColor.mix(self.fromToken(SiColor.INTERFACE_BG_C), "#000000", 0.9))

        self.assign(SiColor.BUTTON_THEMED_BG_A, "#2abed8")
        self.assign(SiColor.BUTTON_THEMED_BG_B, "#2ad98e")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_A, "#1d8699")
        self.assign(SiColor.BUTTON_THEMED_SHADOW_B, "#1d9963")

        self.assign(SiColor.BUTTON_ON, "#372456")
        self.assign(SiColor.BUTTON_OFF, "#562b49")

        self.assign(SiColor.RADIO_BUTTON_UNCHECKED, "#211F25")
        self.assign(SiColor.RADIO_BUTTON_CHECKED, "#9c65ae")

        self.assign(SiColor.CHECKBOX_SVG, "#1C191F")
        self.assign(SiColor.CHECKBOX_UNCHECKED, "#979797")
        self.assign(SiColor.CHECKBOX_CHECKED, "#9c65ae")

        self.assign(SiColor.BUTTON_TEXT_BUTTON_IDLE, "#237165")
        self.assign(SiColor.BUTTON_TEXT_BUTTON_FLASH, "#237165")
        self.assign(SiColor.BUTTON_TEXT_BUTTON_HOVER, "#fabef8")

        # 长按按钮
        self.assign(SiColor.BUTTON_LONG_PRESS_PANEL, "#E76856")
        self.assign(SiColor.BUTTON_LONG_PRESS_SHADOW, "#a64a3d")
        self.assign(SiColor.BUTTON_LONG_PRESS_PROGRESS, "#ff836f")

        # 开关
        self.assign(SiColor.SWITCH_DEACTIVATE, "#D2D2D2")
        self.assign(SiColor.SWITCH_ACTIVATE, "#100912")

        # 滚动条
        self.assign(SiColor.SCROLL_BAR, "#50FFFFFF")

        # 进度条
        self.assign(SiColor.PROGRESS_BAR_TRACK, "#d4d4d4")
        self.assign(SiColor.PROGRESS_BAR_PROCESSING, "#4183a3")
        self.assign(SiColor.PROGRESS_BAR_COMPLETING, "#e3c15b")
        self.assign(SiColor.PROGRESS_BAR_PAUSED, "#a8a8a8")
        self.assign(SiColor.PROGRESS_BAR_FLASHES, "#9fFFFFFF")
