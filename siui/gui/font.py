from collections.abc import Sequence
from enum import Enum

from PyQt5.QtGui import QFont

# 因DPI缩放而引入的因数
scale_factor = 1  # TODO: 需要从获取缩放比例的模块中获取


class SiFont:
    @staticmethod
    def getFont(
        families: Sequence[str] = ["Microsoft YaHei"],
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
    def scaled_size(size: int) -> int:
        return int(size * scale_factor)

    @staticmethod
    def fromToken(token) -> QFont:
        try:
            return token.value
        except KeyError:
            raise ValueError(f"Invalid token: {token}")


class GlobalFont(Enum):
    # Normal
    S_NORMAL = SiFont.getFont(size=14, weight=QFont.Weight.Normal, italic=False)
    M_NORMAL = SiFont.getFont(size=20, weight=QFont.Weight.Normal, italic=False)
    L_NORMAL = SiFont.getFont(size=24, weight=QFont.Weight.Normal, italic=False)
    XL_NORMAL = SiFont.getFont(size=32, weight=QFont.Weight.Normal, italic=False)

    S_NORMAL_ITALIC = SiFont.getFont(size=14, weight=QFont.Weight.Normal, italic=True)
    M_NORMAL_ITALIC = SiFont.getFont(size=20, weight=QFont.Weight.Normal, italic=True)
    L_NORMAL_ITALIC = SiFont.getFont(size=24, weight=QFont.Weight.Normal, italic=True)
    XL_NORMAL_ITALIC = SiFont.getFont(size=32, weight=QFont.Weight.Normal, italic=True)

    # Bold
    S_BOLD = SiFont.getFont(size=14, weight=QFont.Weight.Bold, italic=False)
    M_BOLD = SiFont.getFont(size=20, weight=QFont.Weight.Bold, italic=False)
    L_BOLD = SiFont.getFont(size=24, weight=QFont.Weight.Bold, italic=False)
    XL_BOLD = SiFont.getFont(size=32, weight=QFont.Weight.Bold, italic=False)

    S_BOLD_ITALIC = SiFont.getFont(size=14, weight=QFont.Weight.Bold, italic=True)
    M_BOLD_ITALIC = SiFont.getFont(size=20, weight=QFont.Weight.Bold, italic=True)
    L_BOLD_ITALIC = SiFont.getFont(size=24, weight=QFont.Weight.Bold, italic=True)
    XL_BOLD_ITALIC = SiFont.getFont(size=32, weight=QFont.Weight.Bold, italic=True)
