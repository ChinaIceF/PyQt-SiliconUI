# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, fields

from PyQt5.QtCore import QEvent, QObject, QRect, QRectF, QSize, Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPixmap,
)
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiGlobal
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont


class SiStyleAttr:
    Font = "font"
    TextColor = "text_color"
    IdleColor = "idle_color"
    HoverColor = "hover_color"
    ClickColor = "click_color"
    ButtonColor = "button_color"
    ProgressColor = "progress_color"
    CompleteColor = "complete_color"
    BackgroundColor = "background_color"
    ToggledTextColor = "toggled_text_color"
    ToggledButtonColor = "toggled_button_color"
    BorderInnerRadius = "border_inner_radius"
    BorderRadius = "border_radius"
    BorderHeight = "border_height"
    IconTextGap = "icon_text_gap"


SA = SiStyleAttr


class GlobalStyleManager:
    class Theme:
        Bright = 0
        Dark = 1

    style_dark = {
        "Button": {
            "default": {
                SA.Font:                        SiFont.tokenized(GlobalFont.S_NORMAL),
                SA.TextColor:                   QColor("#DFDFDF"),
                SA.IdleColor:                   QColor("#00baadc7"),
                SA.HoverColor:                  QColor("#1abaadc7"),
                SA.ClickColor:                  QColor("#50baadc7"),
                SA.ButtonColor:                 QColor("#4C4554"),
                SA.ProgressColor:               QColor("#806799"),
                SA.CompleteColor:               QColor("#519868"),
                SA.BackgroundColor:             QColor("#2d2932"),
                SA.ToggledTextColor:            QColor("#DFDFDF"),
                SA.ToggledButtonColor:          QColor("#519868"),
                SA.BorderInnerRadius:           4,
                SA.BorderRadius:                7,
                SA.BorderHeight:                3,
                SA.IconTextGap:                 4,
            },
            "FlatButtonStyleData": {
                SA.ButtonColor:                 QColor("#004C4554")
            },
            "LongPressButtonStyleData": {
                SA.ProgressColor:               QColor("#DA3462"),
                SA.ButtonColor:                 QColor("#932a48"),
                SA.BackgroundColor:             QColor("#642d41"),
                SA.ClickColor:                  QColor("#40FFFFFF"),
            },
            "ToggleButtonStyleData": {},
            "PushButtonStyleData": {},
            "ProgressPushButtonStyleData": {},
        }
    }

    def updateWidgetStyleData(self, widget: QObject) -> None:
        try:
            instance = widget.style_data
        except NameError:
            return
        self.updateStyleData(instance)

    def updateStyleData(self, instance: QObject) -> None:
        style_dict = self.style_dark
        instance_class_name = instance.__class__.__name__
        for type_name, type_dict in zip(style_dict.keys(), style_dict.values()):
            if type_name not in instance.STYLE_TYPES:
                continue

            for class_name, class_dict in zip(type_dict.keys(), type_dict.values()):
                if instance_class_name == class_name or class_name == "default":
                    self._setAttribute(instance, class_dict)

    @staticmethod
    def _setAttribute(instance, class_dict: dict) -> None:
        for attr_name, value in zip(class_dict.keys(), class_dict.values()):
            setattr(instance, attr_name, value)


@dataclass
class ButtonStyleData(QObject):
    STYLE_TYPES = ["Button"]

    font: QFont

    text_color: QColor
    idle_color: QColor
    hover_color: QColor
    click_color: QColor
    button_color: QColor
    progress_color: QColor
    complete_color: QColor
    background_color: QColor
    toggled_text_color: QColor
    toggled_button_color: QColor

    border_inner_radius: int
    border_radius: int
    border_height: int
    icon_text_gap: int

    def __init__(self):
        super().__init__()
        GlobalStyleManager().updateStyleData(self)


@dataclass(init=False)
class FlatButtonStyleData(ButtonStyleData):
    pass


@dataclass(init=False)
class PushButtonStyleData(ButtonStyleData):
    pass


@dataclass(init=False)
class ProgressPushButtonStyleData(PushButtonStyleData):
    pass


@dataclass(init=False)
class LongPressButtonStyleData(PushButtonStyleData):
    pass


@dataclass(init=False)
class ToggleButtonStyleData(ButtonStyleData):
    pass


class ABCButton(QPushButton):
    class Property:
        TextColor = "textColor"
        ButtonRectColor = "buttonRectColor"
        ProgressRectColor = "progressRectColor"
        HighlightRectColor = "highlightRectColor"
        BackgroundRectColor = "backgroundRectColor"
        Progress = "progress"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = None
        self._progress = 0
        self._highlight_rect_color = QColor("#00FFFFFF")
        self._progress_rect_color = None
        self._background_rect_color = None
        self._button_rect_color = None
        self._text_color = None

        self.highlight_ani = SiExpAnimationRefactor(self, self.Property.HighlightRectColor)
        self.highlight_ani.init(1 / 8, 0.2, self._highlight_rect_color, self._highlight_rect_color)

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

    def reloadStyleData(self):
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

    def reloadStyleData(self) -> None:
        self.setFont(self.style_data.font)
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

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.Progress)
        self.progress_ani.init(1 / 6, 0.005, 0, 0)

        self.progress_color_ani = SiExpAnimationRefactor(self, self.Property.ProgressRectColor)
        self.progress_color_ani.init(1 / 8, 0.01, self._progress_rect_color, self._progress_rect_color)

    def setProgress(self, p: float, ani: bool = True) -> None:
        self._progress = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self._updateCompleteState()

    def reloadStyleData(self) -> None:
        self.setFont(self.style_data.font)
        self._updateCompleteState()
        self.update()

    def _updateProgress(self, ani: bool = True) -> None:
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

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        p = min(self._progress, 1)  # prevent progress exceeding caused by using animation.
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(p - 0.0001, self._progress_rect_color)  # use property variable
        gradient.setColorAt(p, self.style_data.button_color)
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))


class SiLongPressButtonRefactor(SiPushButtonRefactor):
    longPressed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = LongPressButtonStyleData()
        self._progress = 0

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.Progress)
        self.progress_ani.init(-1 / 16, 0.12, 0, 0)
        # self.progress_ani.valueChanged.connect(print)

        self.go_backwards_timer = QTimer(self)
        self.go_backwards_timer.setSingleShot(True)
        self.go_backwards_timer.setInterval(500)
        self.go_backwards_timer.timeout.connect(self._goBackwards)

        self.mouse_pressed_timer = QTimer(self)
        self.mouse_pressed_timer.setInterval(1000 // 60)
        self.mouse_pressed_timer.timeout.connect(self._onMousePressed)

    def setProgress(self, p: float, ani: bool = True) -> None:
        self._progress = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self.progress_ani.update()
        self.update()

    def reloadStyleData(self) -> None:
        self.setFont(self.style_data.font)
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
        gradient.setColorAt(p, self.style_data.button_color)
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

    def reloadStyleData(self) -> None:
        self.setFont(self.style_data.font)
        self.update()

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

        self.toggle_btn_color_ani = SiExpAnimationRefactor(self, self.Property.ButtonRectColor)
        self.toggle_btn_color_ani.init(1 / 8, 0.01, self._button_rect_color, self._button_rect_color)

        self.toggle_text_color_ani = SiExpAnimationRefactor(self, self.Property.TextColor)
        self.toggle_text_color_ani.init(1 / 8, 0.01, self._text_color, self._text_color)

        self.toggled.connect(self._onButtonToggled)

    def reloadStyleData(self) -> None:
        self.setFont(self.style_data.font)
        self._onButtonToggled(self.isChecked())
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
