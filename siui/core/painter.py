from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

if TYPE_CHECKING:
    from PyQt5.QtGui import QFont, QPaintDevice

    from siui.typing import T_Brush, T_PenStyle


def createPainter(
    paintDevice: QPaintDevice,
    renderHint: Optional[QPainter.RenderHint] = QPainter.RenderHint.Antialiasing,
    penStyle: T_PenStyle = Qt.PenStyle.NoPen,
    brush: T_Brush = None,
    font: Optional[QFont] = None,
) -> QPainter:
    """构造并初始化 QPainter 对象
    应该使用 with 关键字来创建和关闭 QPainter 对象

    参数:
        - parent: QPaintDevice 的子类实例，通常是 QWidget 或 QImage
        - renderHint: 指定渲染提示，默认为 QPainter.RenderHint.Antialiasing 标准抗锯齿
        - penStyle: Qt.PenStyle 类型，指定画笔样式，默认为 Qt.PenStyle.NoPen
        - brushColor: 字符串或 QColor 对象，指定画刷颜色，默认不指定
        - font: QFont 对象，指定字体，默认不指定

    返回:
        QPainter 对象实例
    """
    painter = QPainter(paintDevice)
    if renderHint is not None:
        painter.setRenderHint(renderHint)

    if penStyle is not None:
        painter.setPen(penStyle)

    if brush is not None:
        painter.setBrush(brush)

    if font is not None:
        painter.setFont(font)

    return painter
