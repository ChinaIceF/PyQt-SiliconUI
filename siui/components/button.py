# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QObject, QRect, QRectF, QSize, Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QFontMetrics, QIcon, QLinearGradient, QPainter, QPainterPath, QPaintEvent, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiColor, SiGlobal
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont


@dataclass
class ButtonStyleData(QObject):
    font = SiFont.tokenized(GlobalFont.S_NORMAL)

    text_color = QColor("#DFDFDF")
    idle_color = QColor("#00baadc7")
    hover_color = QColor("#1abaadc7")
    click_color = QColor("#50baadc7")
    button_color = QColor("#4C4554")
    progress_color = QColor("#806799")
    complete_color = QColor("#519868")
    background_color = QColor("#2d2932")
    toggled_text_color = QColor("#DFDFDF")
    toggled_button_color = QColor("#519868")

    border_inner_radius: int = 4
    border_radius: int = 7
    border_height: int = 3
    icon_text_gap: int = 4

    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)


@dataclass
class FlatButtonStyleData(ButtonStyleData):
    pass


@dataclass
class PushButtonStyleData(ButtonStyleData):
    background_color = QColor("#2d2932")
    border_inner_radius: int = 4
    border_height: int = 3


@dataclass
class ProgressPushButtonStyleData(PushButtonStyleData):
    progress_color = QColor("#806799")
    complete_color = QColor("#519868")


@dataclass
class LongPressButtonStyleData(PushButtonStyleData):
    progress_color = QColor("#DA3462")
    button_color = QColor("#932a48")
    background_color = QColor("#642d41")
    click_color = QColor("#40FFFFFF")


@dataclass
class ToggleButtonStyleData(ButtonStyleData):
    toggled_text_color = QColor("#DFDFDF")
    toggled_button_color = QColor("#519868")


class ABCButton(QPushButton):
    class Property:
        textColor = "textColor"
        buttonRectColor = "buttonRectColor"
        progressRectColor = "progressRectColor"
        highlightRectColor = "highlightRectColor"
        backgroundRectColor = "backgroundRectColor"
        progress = "progress"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = None
        self._progress = 0
        self._highlight_rect_color = QColor("#00FFFFFF")
        self._progress_rect_color = None
        self._background_rect_color = None
        self._button_rect_color = None
        self._text_color = None

        self.highlight_ani = SiExpAnimationRefactor(self, self.Property.highlightRectColor)
        self.highlight_ani.init(1/8, 0.2, self._highlight_rect_color, self._highlight_rect_color)

        self.clicked.connect(self._onButtonClicked)

    @pyqtProperty(QColor)
    def highlightRectColor(self):
        return self._highlight_rect_color

    @highlightRectColor.setter
    def highlightRectColor(self, value: QColor):
        self._highlight_rect_color = value
        self.update()

    @pyqtProperty(QColor)
    def buttonRectColor(self):
        return self._button_rect_color

    @buttonRectColor.setter
    def buttonRectColor(self, color: QColor):
        self._button_rect_color = color
        self.update()

    @pyqtProperty(QColor)
    def backgroundRectColor(self):
        return self._background_rect_color

    @backgroundRectColor.setter
    def backgroundRectColor(self, color: QColor):
        self._background_rect_color = color
        self.update()

    @pyqtProperty(QColor)
    def textColor(self):
        return self._text_color

    @textColor.setter
    def textColor(self, color: QColor):
        self._text_color = color
        self.update()

    @pyqtProperty(float)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value: float):
        self._progress = max(0.0, min(value, 1.0))
        self.update()

    @pyqtProperty(QColor)
    def progressRectColor(self):
        return self._progress_rect_color

    @progressRectColor.setter
    def progressRectColor(self, value: QColor):
        self._progress_rect_color = value
        self.update()

    def reloadStyle(self):
        raise NotImplementedError()

    def flash(self) -> None:
        self.highlight_ani.setCurrentValue(self.style_data.click_color)
        self.highlight_ani.start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, color: QColor | str) -> None:
        self.style_data.button_color = QColor(color)
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

    def _showToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and self.toolTip() != "":
            tool_tip_window.setNowInsideOf(self)
            tool_tip_window.show_()

    def _hideToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and self.toolTip() != "":
            tool_tip_window.setNowInsideOf(None)
            tool_tip_window.hide_()

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def _onAnimationTicked(self, _) -> None:
        raise NotImplementedError()

    def _onButtonClicked(self) -> None:
        raise NotImplementedError()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._hideToolTip()


class SiPushButtonRefactor(ABCButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = PushButtonStyleData()
        self._initStyle()

    def _initStyle(self):
        self.setFont(self.style_data.font)
        self.setIconSize(QSize(20, 20))

    @classmethod
    def withText(cls, text: str, parent: QWidget | None = None):
        obj = cls(parent)
        obj.setText(text)
        return obj

    @classmethod
    def withIcon(cls, icon: QIcon, parent: QWidget | None = None):
        obj = cls(parent)
        obj.setIcon(icon)
        return obj

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None):
        obj = cls(parent)
        obj.setText(text)
        obj.setIcon(QIcon(icon))
        return obj

    @property
    def bottomBorderHeight(self) -> int:
        return self.style_data.border_height

    def setBackgroundColor(self, code: str) -> None:
        self.style_data.background_color = SiColor.toArray(code, "rgba")
        self.update()

    def setBorderInnerRadius(self, r: int) -> None:
        self.style_data.border_inner_radius = r
        self.update()

    def setBorderHeight(self, h: int) -> None:
        self.style_data.border_height = h
        self.update()

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_inner_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), radius, radius)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.button_color)
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._highlight_rect_color)  # use property variable
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.text_color)
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def _onButtonClicked(self) -> None:
        self.flash()

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height() - self.style_data.border_height - 1)
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            ((self.height() - self.style_data.border_height) - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setEndValue(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setEndValue(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)


class SiProgressPushButton(SiPushButtonRefactor):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = ProgressPushButtonStyleData()
        self._progress_rect_color = self.style_data.progress_color
        self._progress = 0

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.progress)
        self.progress_ani.init(1/6, 0.005, 0, 0)

        self.progress_color_ani = SiExpAnimationRefactor(self, self.Property.progressRectColor)
        self.progress_color_ani.init(1/8, 0.01, self._progress_rect_color, self._progress_rect_color)

    def setProgress(self, p: float, ani: bool = True) -> None:
        self._progress = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self._updateCompleteState()
        # self.update()

    def _updateProgress(self, ani: bool) -> None:
        if ani is True:
            self.progress_ani.setEndValue(self._progress)
            self.progress_ani.start()
        else:
            self.progress_ani.setEndValue(self._progress)
            self.progress_ani.setCurrentValue(self._progress)
            self.progress_ani.stop()

    def _updateCompleteState(self) -> None:
        if self.progress_ani.endValue() == 1.0:
            self.progress_color_ani.setEndValue(self.style_data.complete_color)
            self.progress_color_ani.start()
        else:
            self.progress_color_ani.setEndValue(self.style_data.progress_color)
            self.progress_color_ani.start()

    def setProgressColor(self, color: QColor | str) -> None:
        self.style_data.progress_color = QColor(color)
        self._updateCompleteState()
        self.update()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        p = min(self._progress, 1)  # prevent progress exceeding caused by using animation.
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(p - 0.0001, self._progress_rect_color)  # use property variable
        gradient.setColorAt(p,          self.style_data.button_color)
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))


class SiLongPressButtonRefactor(SiPushButtonRefactor):
    longPressed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = LongPressButtonStyleData()
        self._progress = 0

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.progress)
        self.progress_ani.init(-1/16, 0.12, 0, 0)
        # self.progress_ani.valueChanged.connect(print)

        self.go_backwards_timer = QTimer(self)
        self.go_backwards_timer.setSingleShot(True)
        self.go_backwards_timer.setInterval(500)
        self.go_backwards_timer.timeout.connect(self._goBackwards)

        self.mouse_pressed_timer = QTimer(self)
        self.mouse_pressed_timer.setInterval(1000//60)
        self.mouse_pressed_timer.timeout.connect(self._onMousePressed)

    def setProgress(self, p: float, ani: bool = True) -> None:
        self._progress = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self.progress_ani.update()
        self.update()

    def _stepLength(self) -> float:
        return (1 - self._progress) / 16 + 0.001

    def _onMousePressed(self) -> None:
        self.setProgress(self._progress + self._stepLength(), ani=False)

    def _onButtonClicked(self) -> None:
        pass  # disable flashes on mouse click

    def _updateProgress(self, ani: bool) -> None:
        if ani is True:
            self.progress_ani.setEndValue(self._progress)
            self.progress_ani.start()
        else:
            self.progress_ani.setEndValue(self._progress)
            self.progress_ani.setCurrentValue(self._progress)
            self.progress_ani.stop()

        if self._progress == 1.0:
            self.mouse_pressed_timer.stop()
            self.go_backwards_timer.stop()
            self.longPressed.emit()
            self._onLongPressed()
            self._goBackwards(200)

    def _onLongPressed(self) -> None:
        self.highlight_ani.setCurrentValue(self.style_data.click_color)
        self.highlight_ani.start()

    def _goBackwards(self, delay: int = 0) -> None:
        self.progress_ani.setEndValue(0)
        self.progress_ani.startAfter(delay)

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        p = min(self._progress, 1)  # prevent progress exceeding caused by using animation.
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(p - 0.0001, self.style_data.progress_color)
        gradient.setColorAt(p,          self.style_data.button_color)
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        if self.progress_ani.state() != self.progress_ani.State.Running and not self.mouse_pressed_timer.isActive():
            self.mouse_pressed_timer.start()
            self.go_backwards_timer.stop()

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)
        self.mouse_pressed_timer.stop()
        self.go_backwards_timer.start()


class SiFlatButton(ABCButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = FlatButtonStyleData()
        self._initStyle()

    def _initStyle(self):
        self.setFont(self.style_data.font)
        self.setIconSize(QSize(20, 20))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.button_color)
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._highlight_rect_color)  # use property variable
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.text_color)
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height())
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            (self.height() - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.highlight_ani.setCurrentValue(self.style_data.click_color)
        self.highlight_ani.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setEndValue(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setEndValue(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()


class SiToggleButtonRefactor(SiFlatButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)

        self.style_data = ToggleButtonStyleData()
        self._button_rect_color = self.style_data.button_color
        self._text_color = self.style_data.text_color

        self.toggle_btn_color_ani = SiExpAnimationRefactor(self, self.Property.buttonRectColor)
        self.toggle_btn_color_ani.init(1/8, 0.01, self._button_rect_color, self._button_rect_color)

        self.toggle_text_color_ani = SiExpAnimationRefactor(self, self.Property.textColor)
        self.toggle_text_color_ani.init(1/8, 0.01, self._text_color, self._text_color)

        self.toggled.connect(self._onButtonToggled)

    def setToggledButtonColor(self, color: QColor | str) -> None:
        self.style_data.toggled_button_color = QColor(color)
        self.update()

    def setToggledTextColor(self, color: QColor | str) -> None:
        self.style_data.toggled_text_color = QColor(color)
        self.update()

    def _onButtonToggled(self, state: bool) -> None:
        if state:
            self.toggle_btn_color_ani.setEndValue(self.style_data.toggled_button_color)
            self.toggle_text_color_ani.setEndValue(self.style_data.toggled_text_color)
            self.toggle_btn_color_ani.start()
            self.toggle_text_color_ani.start()
        else:
            self.toggle_btn_color_ani.setEndValue(self.style_data.button_color)
            self.toggle_text_color_ani.setEndValue(self.style_data.text_color)
            self.toggle_btn_color_ani.start()
            self.toggle_text_color_ani.start()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._button_rect_color)  # use property variable
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self._text_color)  # use property variable
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())
