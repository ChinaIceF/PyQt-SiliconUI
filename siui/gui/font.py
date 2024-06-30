from collections.abc import Sequence
from enum import Enum

from PyQt5.QtGui import QFont


class GlobalFont(Enum):
    # TODO: 全局 tokenized font
    ...


class SFont:
    @staticmethod
    def getFont(
        families: Sequence[str] = ["Segoe UI", "PingFang SC", "Microsoft YaHei"],
        size: int = 14,
        weight: QFont.Weight = QFont.Weight.Normal,
        italic: bool = False,
    ) -> QFont:
        font = QFont()
        font.setFamilies(families)
        font.setPixelSize(size)
        font.setWeight(weight)
        font.setItalic(italic)
        return font

    @staticmethod
    def fromToken() -> QFont:
        # TODO: 返回全局预设的字体
        raise NotImplementedError
