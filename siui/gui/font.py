from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtGui import QFont

from siui.core.token import FontStyle, GlobalFont, GlobalFontSize, GlobalFontWeight

if TYPE_CHECKING:
    from collections.abc import Sequence


class SiFont:
    @staticmethod
    def getFont(
        size: int = 14,
        weight: QFont.Weight = QFont.Weight.Normal,
        italic: bool = False,
    ) -> QFont:
        font = QFont()
        font.defaultFamily()
        font.setPixelSize(size)
        font.setWeight(weight)
        font.setItalic(italic)
        return font

    @staticmethod
    def fromToken(size: GlobalFontSize, weight: GlobalFontWeight, style: FontStyle) -> QFont:
        """通过已经令牌化的字体属性构造字体"""

        return SiFont.getFont(size=size.value, weight=weight.value, italic=style == FontStyle.ITALIC)

    @staticmethod
    def tokenized(token: GlobalFont) -> QFont:
        """返回一个已经被令牌化的全局字体"""

        try:
            return SiFont.fromToken(*token.value)
        except KeyError:
            raise ValueError(f"Invalid token: {token}")
