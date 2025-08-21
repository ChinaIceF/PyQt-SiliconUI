
from PyQt5.QtCore import QTimer, QRect, QRectF, Qt, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QProgressBar

from siui.core import createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.event_filter import WidgetToolTipRedirectEventFilter
from siui.core.globals import toolTipWindow
from siui.typing import T_WidgetParent


class ProgressBarStyleData:
    background_color = QColor("#25222a")
    loading_color = QColor("#66cbff")
    processing_color = QColor("#fed966")
    paused_color = QColor("#7f7f7f")
    error_color = QColor("#ed716c")
    flash_start_color = QColor("#FFFFFF")
    flash_end_color = QColor("#00FFFFFF")


class SiProgressBarRefactor(QProgressBar):
    stateChanged = pyqtSignal(int)

    class State:
        Loading = 0
        Processing = 1
        Paused = 2
        Error = 3

    class Property:
        ProgressColor = "progressColor"
        ProgressValue = "progressValue"
        FlashColor = "flashColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = ProgressBarStyleData()
        self._is_flashing = False
        self._state = self.State.Loading
        self._prog_to_str_func = self._defaultProgressToToolTipFunc

        self._prog_color = self.style_data.loading_color
        self._prog_value = self.minimum()
        self._flash_color = self.style_data.flash_end_color

        self.ani_prog_color = SiExpAnimationRefactor(self, self.Property.ProgressColor)
        self.ani_prog_color.init(1/4, 0.001, self._prog_color, self._prog_color)

        self.ani_prog_value = SiExpAnimationRefactor(self, self.Property.ProgressValue)
        self.ani_prog_value.init(1/4, 0.001, self._prog_value, self._prog_value)

        self.ani_flash_color = SiExpAnimationRefactor(self, self.Property.FlashColor)
        self.ani_flash_color.init(1/16, 1, self._flash_color, self._flash_color)

        self.flash_timer = QTimer()
        self.flash_timer.setInterval(1000)

        self._initStyle()
        self._initSignal()
        self._initToolTipRedirectEventFilter()

    def _initStyle(self) -> None:
        self.setContentsMargins(0, 8, 0, 8)
        self.setFixedHeight(8 + 4 + 8)

    def _initSignal(self) -> None:
        self.flash_timer.timeout.connect(self.flash)
        self.valueChanged.connect(self._onValueChanged)
        self.stateChanged.connect(self._onStateChanged)

    def _initToolTipRedirectEventFilter(self) -> None:
        self._manager = WidgetToolTipRedirectEventFilter()
        self.installEventFilter(self._manager)

    @pyqtProperty(QColor)
    def progressColor(self):
        return self._prog_color

    @progressColor.setter
    def progressColor(self, value: QColor):
        self._prog_color = value
        self.update()

    @pyqtProperty(float)
    def progressValue(self):
        return self._prog_value

    @progressValue.setter
    def progressValue(self, value: float):
        self._prog_value = value
        self.update()

    @pyqtProperty(QColor)
    def flashColor(self):
        return self._flash_color

    @flashColor.setter
    def flashColor(self, value: QColor):
        self._flash_color = value
        self.update()

    @staticmethod
    def _defaultProgressToToolTipFunc(progress: float) -> str:
        return str(round(progress * 100, 2)) + "%"

    def setProgressToToolTipFunc(self, func) -> None:
        self._prog_to_str_func = func

    def setFlashing(self, state: bool) -> None:
        self._is_flashing = state
        if state:
            self.flash_timer.start()
        else:
            self.flash_timer.stop()

    def isFlashing(self) -> bool:
        return self._is_flashing

    def flash(self) -> None:
        self.ani_flash_color.setCurrentValue(self.style_data.flash_start_color)
        self.ani_flash_color.setEndValue(self.style_data.flash_end_color)
        self.ani_flash_color.start()

    def state(self) -> int:
        return self._state

    def setState(self, state: int) -> None:
        self._state = state
        self.stateChanged.emit(state)
        self.update()

    def _getProgressColor(self) -> QColor:
        if self._state == self.State.Loading:
            return self.style_data.loading_color
        elif self._state == self.State.Processing:
            return self.style_data.processing_color
        elif self._state == self.State.Paused:
            return self.style_data.paused_color
        elif self._state == self.State.Error:
            return self.style_data.error_color
        else:
            raise ValueError(f"Unexpected state {self._state}")

    def _onStateChanged(self, state: int) -> None:
        self.ani_prog_color.setEndValue(self._getProgressColor())
        self.ani_prog_color.start()

    def _onValueChanged(self) -> None:
        self.ani_prog_value.setEndValue(self._valueToProgress(self.value()))
        self.ani_prog_value.start()
        self.flash()

        new_tooltip = self._prog_to_str_func(self._valueToProgress(self.value()))
        self.setToolTip(new_tooltip)

        if self._manager.isEntered():
            self._manager.setTooltip(new_tooltip)

    def _valueToProgress(self, value: float) -> float:
        return (value - self.minimum()) / (self.maximum() - self.minimum())

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 2, 2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(path)

    def _drawProgressRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 2, 2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._prog_color)
        painter.drawPath(path)

    def _drawFlashRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 2, 2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._flash_color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        rect = self.contentsRect()
        progress_rect = QRectF(rect.x(), rect.y(), rect.width() * self._prog_value, rect.height())

        with createPainter(self) as painter:
            self._drawBackgroundRect(painter, rect)
            self._drawProgressRect(painter, progress_rect)
            self._drawFlashRect(painter, progress_rect)


