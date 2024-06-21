
import colorsys
import numpy
import random

fps = 60

class Color(object):

    def decodeColor(code):
        # code      STR     颜色色号 形如 #RRGGBB
        code = code.lstrip('#')
        r, g, b = int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16)
        return numpy.array([r, g, b], dtype = numpy.int64)

    def encodeColor(rgb):
        # rgb       NDARRAY 色值
        r, g, b = rgb
        return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

    def mix(fore, post, weight = 0.5):
        # fore      STR     前色
        # post      STR     后色
        # weight    FLOAT   前色的权重
        fore_rgb = Color.decodeColor(fore)
        post_rgb = Color.decodeColor(post)
        mixed_rgb = fore_rgb * weight + post_rgb * (1-weight)
        return Color.encodeColor(mixed_rgb)

    def random():
        random_color = Color.encodeColor([255 * random.random(), 255 * random.random(), 255 * random.random()])
        return random_color


class SiColorDark(Color):

    # ========== 全局颜色 ==========
    # SVG 默认颜色
    SVG_HEX = '#FFFFFF'

    # 主题色
    THEME_HEX = [
        '#52389a',
        '#9c4e8b',
    ]

    # 提示框颜色
    HINT_HEX = [
        '#FFFFFF',   # 文字颜色
        '#ef413a47'  # 背景颜色
    ]

    # 背景色的几个等级，小指数为父
    BG_GRAD_HEX = [
        '#1C191F',
        '#252229',
        '#2C2930',
        '#342F39',
        '#49454D',
    ]

    # 文字颜色的几个等级，小指数为父
    TEXT_GRAD_HEX = [
        '#FFFFFF',
        '#DFDFDF',
        '#CFCFCF',
        '#AFAFAF',
    ]

    # ========== 控件颜色 ==========
    # 按钮
    BTN_NORM_TEXT_HEX = TEXT_GRAD_HEX[1]
    BTN_NORM_HEX = [
        BG_GRAD_HEX[4], # 正常
        BG_GRAD_HEX[2], # 阴影
    ]

    BTN_HL_TEXT_HEX = '#FFFFFF'
    BTN_HL_HEX = [
        '#52389a',  # 正常
        '#9c4e8b',
        '#372456',  # 阴影
        '#562b49',
    ]

    BTN_HOLD_TEXT_HEX = TEXT_GRAD_HEX[1]
    BTN_HOLD_HEX = [
        '#DA3462',  # 长按时
        '#9F3652',  # 闲置
        '#6a3246',  # 阴影
    ]

    # 开关
    SWC_HEX = [
        '#D2D2D2',  # 关闭
        '#100912',  # 开启
    ]

    # 提示框
    INF_HEX = [
        '#6b39a8',  # 提示
        '#338145',  # 已完成
        '#a87539',  # 警告
        '#a83e39',  # 错误
    ]


    # ========== GLAZE 颜色 ==========
    # 框架
    FRM_TEXT_HEX = TEXT_GRAD_HEX[0]

    # 组
    STK_TEXT_HEX = TEXT_GRAD_HEX[0]
    STK_HL_HEX = '#609c4e8b'

    # 选项
    OPT_TITLE_HEX = TEXT_GRAD_HEX[0]
    OPT_DISCRIPTION_HEX = TEXT_GRAD_HEX[3]


class SiColorBright(Color):

    # ========== 全局颜色 ==========
    # SVG 默认颜色
    SVG_HEX = '#466055'

    # 主题色
    THEME_HEX = [
        '#2ad98e',
        '#2abed8',
    ]

    # 提示框颜色
    HINT_HEX = [
        '#466055',   # 文字颜色
        '#efFFFFFF'  # 背景颜色
    ]

    # 背景色的几个等级，小指数为父
    BG_GRAD_HEX = [
        '#e2f1ec',
        '#f0fffa',
        '#FFFFFF',
        '#F8FCFB',
        '#EAF9F4',
    ]

    # 文字颜色的几个等级，小指数为父
    TEXT_GRAD_HEX = [
        '#466055',
        '#6D8178',
        '#8C9B94',
        '#AAB5AF',
    ]

    # ========== 控件颜色 ==========
    # 按钮
    BTN_NORM_TEXT_HEX = TEXT_GRAD_HEX[0]
    BTN_NORM_HEX = [
        BG_GRAD_HEX[0], # 正常
        Color.mix(BG_GRAD_HEX[0], '#000000', 0.9), # 阴影
    ]

    BTN_HL_TEXT_HEX = '#FFFFFF'
    BTN_HL_HEX = [
        THEME_HEX[0],  # 正常
        THEME_HEX[1],
        Color.mix(THEME_HEX[0], '#000000', 0.8),  # 阴影
        Color.mix(THEME_HEX[1], '#000000', 0.8),
    ]

    BTN_HOLD_TEXT_HEX = '#FFFFFF'
    BTN_HOLD_HEX = [
        '#C6301B',  # 长按时
        '#E76856',  # 闲置
        Color.mix('#C6301B', '#000000', 0.9),  # 阴影
    ]

    # 开关
    SWC_HEX = [
        '#466055',  # 关闭
        Color.mix(THEME_HEX[0], '#000000', 0.2),  # 开启
    ]

    # 提示框
    INF_HEX = [
        '#6b39a8',  # 提示
        '#338145',  # 已完成
        '#a87539',  # 警告
        '#a83e39',  # 错误
    ]


    # ========== GLAZE 颜色 ==========
    # 框架
    FRM_TEXT_HEX = TEXT_GRAD_HEX[0]

    # 组
    STK_TEXT_HEX = TEXT_GRAD_HEX[0]
    STK_HL_HEX = '#602abed8'

    # 选项
    OPT_TITLE_HEX = TEXT_GRAD_HEX[0]
    OPT_DISCRIPTION_HEX = TEXT_GRAD_HEX[3]


colorset = SiColorDark()
