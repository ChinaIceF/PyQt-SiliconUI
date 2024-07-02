from collections.abc import Sequence
from enum import Enum

from PyQt5.QtGui import QFont

# 因DPI缩放而引入的因数
scale_factor = 1  # TODO: 需要从获取缩放比例的模块中获取


class SiFont:
    @staticmethod
    def getFont(
            families: Sequence = ["Segoe UI", "PingFang SC", "Microsoft YaHei"],
            size: int = 14,
            weight: QFont.Weight = QFont.Weight.Normal,
            italic: bool = False,
    ) -> QFont:
        font = QFont()
        font.setFamilies(families)
        font.setPixelSize(SiFont.scaled_size(size))
        font.setWeight(weight)
        font.setItalic(italic)
        return font

    @staticmethod
    def scaled_size(size):
        return int(size * scale_factor)

    @staticmethod
    def fromToken(token) -> QFont:
        return GlobalFont.FONT_DICT.value[token]


class GlobalFont(Enum):
    # Normal
    S_NORMAL = SiFont.getFont(size=10, weight=QFont.Weight.Normal, italic=False)
    M_NORMAL = SiFont.getFont(size=14, weight=QFont.Weight.Normal, italic=False)
    L_NORMAL = SiFont.getFont(size=18, weight=QFont.Weight.Normal, italic=False)
    XL_NORMAL = SiFont.getFont(size=24, weight=QFont.Weight.Normal, italic=False)

    S_NORMAL_ITALIC = SiFont.getFont(size=10, weight=QFont.Weight.Normal, italic=True)
    M_NORMAL_ITALIC = SiFont.getFont(size=14, weight=QFont.Weight.Normal, italic=True)
    L_NORMAL_ITALIC = SiFont.getFont(size=18, weight=QFont.Weight.Normal, italic=True)
    XL_NORMAL_ITALIC = SiFont.getFont(size=24, weight=QFont.Weight.Normal, italic=True)

    # Bold
    S_BOLD = SiFont.getFont(size=10, weight=QFont.Weight.Bold, italic=False)
    M_BOLD = SiFont.getFont(size=14, weight=QFont.Weight.Bold, italic=False)
    L_BOLD = SiFont.getFont(size=18, weight=QFont.Weight.Bold, italic=False)
    XL_BOLD = SiFont.getFont(size=24, weight=QFont.Weight.Bold, italic=False)

    S_BOLD_ITALIC = SiFont.getFont(size=10, weight=QFont.Weight.Bold, italic=True)
    M_BOLD_ITALIC = SiFont.getFont(size=14, weight=QFont.Weight.Bold, italic=True)
    L_BOLD_ITALIC = SiFont.getFont(size=18, weight=QFont.Weight.Bold, italic=True)
    XL_BOLD_ITALIC = SiFont.getFont(size=24, weight=QFont.Weight.Bold, italic=True)

    FONT_DICT = {
        "S_NORMAL": S_NORMAL,
        "M_NORMAL": M_NORMAL,
        "L_NORMAL": L_NORMAL,
        "XL_NORMAL": XL_NORMAL,
        "S_BOLD": S_BOLD,
        "M_BOLD": M_BOLD,
        "L_BOLD": L_BOLD,
        "XL_BOLD": XL_BOLD,
        "S_NORMAL_ITALIC": S_NORMAL_ITALIC,
        "M_NORMAL_ITALIC": M_NORMAL_ITALIC,
        "L_NORMAL_ITALIC": L_NORMAL_ITALIC,
        "XL_NORMAL_ITALIC": XL_NORMAL_ITALIC,
        "S_BOLD_ITALIC": S_BOLD_ITALIC,
        "M_BOLD_ITALIC": M_BOLD_ITALIC,
        "L_BOLD_ITALIC": L_BOLD_ITALIC,
        "XL_BOLD_ITALIC": XL_BOLD_ITALIC,
    }
