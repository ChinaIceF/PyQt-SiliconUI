from siui.core.color import Color
from siui.core.globals import TokenizedDatabase


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


colorset = TokenizedDatabase("color_temp")
colorset.color = SiColorDark()
