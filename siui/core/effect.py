from typing import Tuple, Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QWidget


class SiQuickEffect:
    @staticmethod
    def applyDropShadowOn(widget: QWidget,
                          color: Union[Tuple[int, int, int, int], None],
                          offset: Union[Tuple[int, int], None] = None,
                          blur_radius: int = 16):
        if color is None:
            color = (0, 0, 0, 255)
        if offset is None:
            offset = (0, 0)

        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setColor(QColor(*color))
        shadow.setOffset(*offset)
        shadow.setBlurRadius(blur_radius)
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def applyOpacityOn(widget: QWidget,
                       opacity: float):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        widget.setGraphicsEffect(opacity_effect)
