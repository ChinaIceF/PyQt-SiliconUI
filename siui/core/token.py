from enum import Enum

from PyQt5.QtGui import QFont


class GlobalFontSize(Enum):
    """Tokenized Global Font Size"""

    S = 14
    M = 20
    L = 24
    XL = 32


class GlobalFontWeight(Enum):
    """Tokenized Global Font Weight"""

    LIGHT = QFont.Weight.Light
    NORMAL = QFont.Weight.Normal
    MEDIUM = QFont.Weight.Medium
    DEMI_BOLD = QFont.Weight.DemiBold
    BOLD = QFont.Weight.Bold


class FontStyle(Enum):
    """Tokenized Font Style"""

    REGULAR = QFont.Style.StyleNormal
    ITALIC = QFont.Style.StyleItalic
    OBLIQUE = QFont.Style.StyleOblique


class GlobalFont(Enum):
    """Tokenized Global Font"""

    S_LIGHT = GlobalFontSize.S, GlobalFontWeight.LIGHT, FontStyle.REGULAR
    M_LIGHT = GlobalFontSize.M, GlobalFontWeight.LIGHT, FontStyle.REGULAR
    L_LIGHT = GlobalFontSize.L, GlobalFontWeight.LIGHT, FontStyle.REGULAR
    XL_LIGHT = GlobalFontSize.XL, GlobalFontWeight.LIGHT, FontStyle.REGULAR

    S_LIGHT_ITALIC = GlobalFontSize.S, GlobalFontWeight.LIGHT, FontStyle.ITALIC
    M_LIGHT_ITALIC = GlobalFontSize.M, GlobalFontWeight.LIGHT, FontStyle.ITALIC
    L_LIGHT_ITALIC = GlobalFontSize.L, GlobalFontWeight.LIGHT, FontStyle.ITALIC
    XL_LIGHT_ITALIC = GlobalFontSize.XL, GlobalFontWeight.LIGHT, FontStyle.ITALIC

    S_NORMAL = GlobalFontSize.S, GlobalFontWeight.NORMAL, FontStyle.REGULAR
    M_NORMAL = GlobalFontSize.M, GlobalFontWeight.NORMAL, FontStyle.REGULAR
    L_NORMAL = GlobalFontSize.L, GlobalFontWeight.NORMAL, FontStyle.REGULAR
    XL_NORMAL = GlobalFontSize.XL, GlobalFontWeight.NORMAL, FontStyle.REGULAR

    S_NORMAL_ITALIC = GlobalFontSize.S, GlobalFontWeight.NORMAL, FontStyle.ITALIC
    M_NORMAL_ITALIC = GlobalFontSize.M, GlobalFontWeight.NORMAL, FontStyle.ITALIC
    L_NORMAL_ITALIC = GlobalFontSize.L, GlobalFontWeight.NORMAL, FontStyle.ITALIC
    XL_NORMAL_ITALIC = GlobalFontSize.XL, GlobalFontWeight.NORMAL, FontStyle.ITALIC

    S_MEDIUM = GlobalFontSize.S, GlobalFontWeight.MEDIUM, FontStyle.REGULAR
    M_MEDIUM = GlobalFontSize.M, GlobalFontWeight.MEDIUM, FontStyle.REGULAR
    L_MEDIUM = GlobalFontSize.L, GlobalFontWeight.MEDIUM, FontStyle.REGULAR
    XL_MEDIUM = GlobalFontSize.XL, GlobalFontWeight.MEDIUM, FontStyle.REGULAR

    S_MEDIUM_ITALIC = GlobalFontSize.S, GlobalFontWeight.MEDIUM, FontStyle.ITALIC
    M_MEDIUM_ITALIC = GlobalFontSize.M, GlobalFontWeight.MEDIUM, FontStyle.ITALIC
    L_MEDIUM_ITALIC = GlobalFontSize.L, GlobalFontWeight.MEDIUM, FontStyle.ITALIC
    XL_MEDIUM_ITALIC = GlobalFontSize.XL, GlobalFontWeight.MEDIUM, FontStyle.ITALIC

    S_DEMI_BOLD = GlobalFontSize.S, GlobalFontWeight.DEMI_BOLD, FontStyle.REGULAR
    M_DEMI_BOLD = GlobalFontSize.M, GlobalFontWeight.DEMI_BOLD, FontStyle.REGULAR
    L_DEMI_BOLD = GlobalFontSize.L, GlobalFontWeight.DEMI_BOLD, FontStyle.REGULAR
    XL_DEMI_BOLD = GlobalFontSize.XL, GlobalFontWeight.DEMI_BOLD, FontStyle.REGULAR

    S_DEMI_BOLD_ITALIC = GlobalFontSize.S, GlobalFontWeight.DEMI_BOLD, FontStyle.ITALIC
    M_DEMI_BOLD_ITALIC = GlobalFontSize.M, GlobalFontWeight.DEMI_BOLD, FontStyle.ITALIC
    L_DEMI_BOLD_ITALIC = GlobalFontSize.L, GlobalFontWeight.DEMI_BOLD, FontStyle.ITALIC
    XL_DEMI_BOLD_ITALIC = GlobalFontSize.XL, GlobalFontWeight.DEMI_BOLD, FontStyle.ITALIC

    S_BOLD = GlobalFontSize.S, GlobalFontWeight.BOLD, FontStyle.REGULAR
    M_BOLD = GlobalFontSize.M, GlobalFontWeight.BOLD, FontStyle.REGULAR
    L_BOLD = GlobalFontSize.L, GlobalFontWeight.BOLD, FontStyle.REGULAR
    XL_BOLD = GlobalFontSize.XL, GlobalFontWeight.BOLD, FontStyle.REGULAR

    S_BOLD_ITALIC = GlobalFontSize.S, GlobalFontWeight.BOLD, FontStyle.ITALIC
    M_BOLD_ITALIC = GlobalFontSize.M, GlobalFontWeight.BOLD, FontStyle.ITALIC
    L_BOLD_ITALIC = GlobalFontSize.L, GlobalFontWeight.BOLD, FontStyle.ITALIC
    XL_BOLD_ITALIC = GlobalFontSize.XL, GlobalFontWeight.BOLD, FontStyle.ITALIC
