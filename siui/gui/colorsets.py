from siui.core.color import Color


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
