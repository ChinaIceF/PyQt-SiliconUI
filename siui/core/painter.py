from __future__ import annotations

import math
from functools import lru_cache
from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPainter, QPainterPath

if TYPE_CHECKING:
    from PyQt5.QtGui import QFont, QPaintDevice

    from siui.typing import T_Brush, T_PenStyle, T_RenderHint


def createPainter(
    paintDevice: QPaintDevice,
    renderHint: T_RenderHint = QPainter.RenderHint.Antialiasing,
    penStyle: T_PenStyle = Qt.PenStyle.NoPen,
    brush: T_Brush = None,
    font: QFont | None = None,
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
        painter.setRenderHints(renderHint)

    if penStyle is not None:
        painter.setPen(penStyle)

    if brush is not None:
        painter.setBrush(brush)

    if font is not None:
        painter.setFont(font)

    return painter


def _superSin(x: float, power: float = 5.0) -> float:
    return math.copysign(abs(math.sin(x)) ** (2 / power), math.sin(x))


def _superCos(x: float, power: float = 5.0) -> float:
    return math.copysign(abs(math.cos(x)) ** (2 / power), math.cos(x))


@lru_cache(maxsize=None)
def _getSuperRoundedPoints(radius_x: float, radius_y: float, power: float, quality: int):
    points = []
    for i in range(quality + 1):
        points.append(QPointF((_superSin(2 * math.pi * i / quality, power) + 0) * radius_x,
                              (_superCos(2 * math.pi * i / quality, power) + 0) * radius_y))
    return points


@lru_cache(maxsize=None)
def _cachedGetSuperRoundedRectPath(rect_tuple: tuple,
                                   radius_x: float,
                                   radius_y: float,
                                   power: float,
                                   quality: int) -> QPainterPath:
    rect = QRectF(*rect_tuple)
    path = QPainterPath()

    if quality == -1:
        quality = max(radius_x, radius_y) // 4 * 4

    points = _getSuperRoundedPoints(radius_x, radius_y, power, quality)
    inner_rect = QRectF(rect.x() + radius_x, rect.y() + radius_y,
                        rect.width() - 2 * radius_x, rect.height() - 2 * radius_y)

    q = quality

    path.moveTo(points[q // 4 * 0] + inner_rect.bottomRight())
    delta = inner_rect.bottomRight()
    for i in range(q // 4 * 0, q // 4 * 1 + 1):
        mid_point = (points[i] + points[i + 1]) / 2 + delta
        point = points[i] + delta
        path.quadTo(point, mid_point)

    delta = inner_rect.topRight()
    for i in range(q // 4 * 1, q // 4 * 2 + 1):
        mid_point = (points[i] + points[i + 1]) / 2 + delta
        point = points[i] + delta
        path.quadTo(point, mid_point)

    delta = inner_rect.topLeft()
    for i in range(q // 4 * 2, q // 4 * 3 + 1):
        mid_point = (points[i] + points[i + 1]) / 2 + delta
        point = points[i] + delta
        path.quadTo(point, mid_point)

    delta = inner_rect.bottomLeft()
    for i in range(q // 4 * 3, q // 4 * 4):
        mid_point = (points[i] + points[i + 1]) / 2 + delta
        point = points[i] + delta
        path.quadTo(point, mid_point)

    path.lineTo(points[-1] + inner_rect.bottomLeft())  # 连接到最后一个点

    return path


def getSuperRoundedRectPath(rect: QRectF,
                            radius_x: float,
                            radius_y: float,
                            power: float = 5.0,
                            quality: int = -1) -> QPainterPath:
    """生成并返回一个超椭圆圆角矩形的路径

    参数:
        - radius_x: float 圆角的横轴半径
        - radius_y: float 圆角的纵轴半径
        - power: float 超椭圆方程的幂数
        - quality: int 采样品质，若传入 -1，则根据圆角半径自动选择品质，其他传入值应为 4 的整数倍

    返回:
        QPainterPath 对象实例

    该函数启用了缓存，密集绘制友好
    """

    rect_tuple = (rect.x(), rect.y(), rect.width(), rect.height())
    return _cachedGetSuperRoundedRectPath(rect_tuple, radius_x, radius_y, power, quality)


__all__ = [
    "createPainter", "getSuperRoundedRectPath"
]
