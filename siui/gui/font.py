from collections.abc import Sequence
from enum import Enum

from PyQt5.QtGui import QFont
from siui.core.globals import SiGlobal

# 因DPI缩放而引入的因数
scale_factor = 1  # TODO: 需要从获取缩放比例的模块中获取


class SiFont:
    @staticmethod
    def getFont(
            families: Sequence = ["Microsoft YaHei"],
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


class GlobalFontDict:
    fonts = {}

    fonts["S_NORMAL"] = GlobalFont.S_NORMAL.value
    fonts["M_NORMAL"] = GlobalFont.M_NORMAL.value
    fonts["L_NORMAL"] = GlobalFont.L_NORMAL.value
    fonts["XL_NORMAL"] = GlobalFont.XL_NORMAL.value

    fonts["S_NORMAL_ITALIC"] = GlobalFont.S_NORMAL_ITALIC.value
    fonts["M_NORMAL_ITALIC"] = GlobalFont.M_NORMAL_ITALIC.value
    fonts["L_NORMAL_ITALIC"] = GlobalFont.L_NORMAL_ITALIC.value
    fonts["XL_NORMAL_ITALIC"] = GlobalFont.XL_NORMAL_ITALIC.value

    fonts["S_BOLD"] = GlobalFont.S_BOLD.value
    fonts["M_BOLD"] = GlobalFont.M_BOLD.value
    fonts["L_BOLD"] = GlobalFont.L_BOLD.value
    fonts["XL_BOLD"] = GlobalFont.XL_BOLD.value

    fonts["S_BOLD_ITALIC"] = GlobalFont.S_BOLD_ITALIC.value
    fonts["M_BOLD_ITALIC"] = GlobalFont.M_BOLD_ITALIC.value
    fonts["L_BOLD_ITALIC"] = GlobalFont.L_BOLD_ITALIC.value
    fonts["XL_BOLD_ITALIC"] = GlobalFont.XL_BOLD_ITALIC.value


# 合并到全局字体
SiGlobal.siui.fonts.update(GlobalFontDict.fonts)