from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import qApp

from siui.core.token import FontStyle, GlobalFont, GlobalFontSize, GlobalFontWeight

if TYPE_CHECKING:
    from collections.abc import Sequence


class SiFont:
    """SiUI Font Class

    You can use low-level API to customize fonts details,
    or use tokenized global fonts to quickly create fonts.
    """
    Weight = QFont.Weight

    @staticmethod
    def getFont(
        families=None,
        size: int = 14,
        weight: QFont.Weight = QFont.Weight.Normal,
        italic: bool = False,
        hinting_preference: QFont.HintingPreference = QFont.PreferFullHinting
    ) -> QFont:
        """Low-level API for creating font instance

        Application-level configuration takes the highest priority,
        and it is recommended to use the tokenized Hier-level API.

        Args:
            - families: 字体族列表，如果指定了应用程序级别的全局配置，则会覆盖默认字体家族
            - size: 字体大小
            - weight: 字体粗细
            - italic: 是否斜体
            - hinting_preference: 字体 Hinting 偏好， 默认为 PreferFullHinting

        Returns:
            - QFont: 字体实例

        """
        if families is None:
            families = (
                    qApp.font().families() or
                    ["Segoe UI", "Microsoft YaHei", "San Francisco Fonts", ".PingFang TC", "PingFang SC"]
            )

        font = QFont()
        font.setFamilies(families)
        font.setPixelSize(size)
        font.setWeight(weight)
        font.setItalic(italic)
        font.setHintingPreference(hinting_preference)
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
