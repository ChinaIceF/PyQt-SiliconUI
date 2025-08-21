from __future__ import annotations

import math
from contextlib import contextmanager
from functools import lru_cache

from PyQt5.QtCore import QPoint, QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPaintDevice, QPainter, QPainterPath


@contextmanager
def createPainter(device: QPaintDevice,
                  render_hints: QPainter.RenderHints = QPainter.Antialiasing) -> QPainter:
    painter = QPainter(device)
    painter.setRenderHints(render_hints)
    painter.setPen(Qt.NoPen)
    painter.setBrush(Qt.NoBrush)
    try:
        yield painter
    finally:
        painter.end()


@lru_cache(maxsize=None)
def _getSuperRoundedPoints(radius_x: float, radius_y: float, power: float, quality: int):
    def _superSin(x: float, power: float = 5.0) -> float:
        return math.copysign(abs(math.sin(x)) ** (2 / power), math.sin(x))

    def _superCos(x: float, power: float = 5.0) -> float:
        return math.copysign(abs(math.cos(x)) ** (2 / power), math.cos(x))

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


def getRoundedRectPathQuad(rect: QRectF,
                       radius_tl: float, radius_tr: float,
                       radius_br: float, radius_bl: float) -> QPainterPath:
    """
    使用 quadTo 绘制不对称圆角矩形
    :param rect: QRectF 矩形区域
    :param radius_tl: 左上角半径
    :param radius_tr: 右上角半径
    :param radius_br: 右下角半径
    :param radius_bl: 左下角半径
    """
    path = QPainterPath()

    # 左上角开始
    path.moveTo(rect.left() + radius_tl, rect.top())
    path.lineTo(rect.right() - radius_tr, rect.top())
    if radius_tr > 0:
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + radius_tr)
    else:
        path.lineTo(rect.right(), rect.top())

    path.lineTo(rect.right(), rect.bottom() - radius_br)
    if radius_br > 0:
        path.quadTo(rect.right(), rect.bottom(), rect.right() - radius_br, rect.bottom())
    else:
        path.lineTo(rect.right(), rect.bottom())

    path.lineTo(rect.left() + radius_bl, rect.bottom())
    if radius_bl > 0:
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - radius_bl)
    else:
        path.lineTo(rect.left(), rect.bottom())

    path.lineTo(rect.left(), rect.top() + radius_tl)
    if radius_tl > 0:
        path.quadTo(rect.left(), rect.top(), rect.left() + radius_tl, rect.top())
    else:
        path.lineTo(rect.left(), rect.top())

    path.closeSubpath()
    return path


def getRoundedRectPathArc(rect: QRectF,
                          radius_tl: float, radius_tr: float,
                          radius_br: float, radius_bl: float) -> QPainterPath:
    """
    使用 arcTo 绘制不对称圆角矩形
    :param rect: QRectF 矩形区域
    :param radius_tl: 左上角半径
    :param radius_tr: 右上角半径
    :param radius_br: 右下角半径
    :param radius_bl: 左下角半径
    """
    path = QPainterPath()

    path.moveTo(rect.left() + radius_tl, rect.top())

    path.lineTo(rect.right() - radius_tr, rect.top())
    path.arcTo(QRectF(rect.right() - 2*radius_tr, rect.top(), 2*radius_tr, 2*radius_tr), 90, -90)

    path.lineTo(rect.right(), rect.bottom() - radius_br)
    path.arcTo(QRectF(rect.right() - 2*radius_br, rect.bottom() - 2*radius_br, 2*radius_br, 2*radius_br), 0, -90)

    path.lineTo(rect.left() + radius_bl, rect.bottom())
    path.arcTo(QRectF(rect.left(), rect.bottom() - 2*radius_bl, 2*radius_bl, 2*radius_bl), 270, -90)

    path.lineTo(rect.left(), rect.top() + radius_tl)
    path.arcTo(QRectF(rect.left(), rect.top(), 2*radius_tl, 2*radius_tl), 180, -90)

    path.closeSubpath()
    return path

@lru_cache(maxsize=None)
def _cachedGaussianLinearGradient(start_x, start_y, final_stop_x, final_stop_y, color_code, quality):

    def getInterpolationPoints(quality: int):
        def f(x):
            return math.exp(-5 * x ** 2)

        def g(x):
            return (math.sin((x - 1/2) * math.pi) + 1) / 2

        result = []

        for i in range(quality+1):
            p_x = g(i / quality)
            p_y = f(p_x)
            result.append((p_x, p_y))

        return result

    start = QPointF(start_x, start_y)
    final_stop = QPointF(final_stop_x, final_stop_y)

    r, g, b, a = QColor(color_code).getRgb()

    gradient = QLinearGradient(start, final_stop)
    points = getInterpolationPoints(quality)

    for pos, transparency in points:
        p_color = QColor(r, g, b, int(transparency * a))
        gradient.setColorAt(pos, p_color)

    return gradient


def getGaussianLinearGradient(start: QPointF | QPoint,
                              final_stop: QRectF | QPoint,
                              color: QColor,
                              quality: int = 8) -> QLinearGradient:

    start_x = start.x()
    start_y = start.y()
    final_stop_x = final_stop.x()
    final_stop_y = final_stop.y()
    color_code = color.name(QColor.NameFormat.HexArgb)

    return _cachedGaussianLinearGradient(start_x, start_y, final_stop_x, final_stop_y, color_code, quality)


__all__ = [
    "createPainter", "getSuperRoundedRectPath", "getGaussianLinearGradient"
]
