# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from PyQt5.QtCore import (
    QEvent,
    QObject,
    QPointF,
    QRect,
    QRectF,
    QSize,
    Qt,
    QTimer,
    pyqtProperty,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QPixmap,
)
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton
from typing_extensions import Self

from siui.core import GlobalFont, SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont

if TYPE_CHECKING:
    from siui.typing import T_WidgetParent


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
                SA.Font: SiFont.tokenized(GlobalFont.S_NORMAL),
                SA.TextColor: QColor("#DFDFDF"),
                SA.IdleColor: QColor("#00baadc7"),
                SA.HoverColor: QColor("#1abaadc7"),
                SA.ClickColor: QColor("#50baadc7"),
                SA.ButtonColor: QColor("#4C4554"),
                SA.ProgressColor: QColor("#806799"),
                SA.CompleteColor: QColor("#519868"),
                SA.BackgroundColor: QColor("#2d2932"),
                SA.ToggledTextColor: QColor("#DFDFDF"),
                SA.ToggledButtonColor: QColor("#519868"),
                SA.BorderInnerRadius: 5,
                SA.BorderRadius: 7,
                SA.BorderHeight: 3,
                SA.IconTextGap: 4,
            },
            "LongPressButtonStyleData": {
                SA.ProgressColor: QColor("#DA3462"),
                SA.ButtonColor: QColor("#932a48"),
                SA.BackgroundColor: QColor("#642d41"),
                SA.ClickColor: QColor("#40FFFFFF"),
            },
            "FlatButtonStyleData": {SA.ButtonColor: QColor("#004C4554")},
            "ToggleButtonStyleData": {
                SA.ButtonColor: QColor("#004C4554"),
            },
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


# @dataclass
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


# @dataclass(init=False)
class FlatButtonStyleData(ButtonStyleData):
    indicator_hover_color = QColor("#A681BF")
    indicator_selected_color = QColor("#A681BF")
    indicator_flash_color = QColor("#F5EBF9")
    indicator_idle_color = QColor("#00A681BF")


# @dataclass(init=False)
class PushButtonStyleData(ButtonStyleData):
    pass


# @dataclass(init=False)
class ProgressPushButtonStyleData(PushButtonStyleData):
    pass


# @dataclass(init=False)
class LongPressButtonStyleData(PushButtonStyleData):
    pass


# @dataclass(init=False)
class ToggleButtonStyleData(ButtonStyleData):
    pass


class ABCButton(QPushButton):
    class Property:
        ScaleFactor = "scaleFactor"
        TextColor = "textColor"
        ButtonRectColor = "buttonRectColor"
        ProgressRectColor = "progressRectColor"
        HighlightRectColor = "highlightRectColor"
        BackgroundRectColor = "backgroundRectColor"
        Progress = "progress"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = None
        self._progress = 0
        self._scale_factor = 1
        self._highlight_rect_color = QColor("#00FFFFFF")
        self._progress_rect_color = None
        self._background_rect_color = None
        self._button_rect_color = None
        self._text_color = None

        self.highlight_ani = SiExpAnimationRefactor(self, self.Property.HighlightRectColor)
        self.highlight_ani.init(1 / 8, 0.2, self._highlight_rect_color, self._highlight_rect_color)

        self.clicked.connect(self._onButtonClicked)

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value: float):
        self._scale_factor = value
        self.update()

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

    def styleData(self) -> PushButtonStyleData:
        return self.style_data

    def reloadStyleData(self):
        raise NotImplementedError()

    def _onButtonClicked(self) -> None:
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
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = PushButtonStyleData()
        self._initStyle()
        self._scale_factor = 1

        self.scale_factor_ani = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.scale_factor_ani.init(1 / 16, 0, 1, 1)

    @classmethod
    def withText(cls, text: str, parent: T_WidgetParent = None) -> Self:
        obj = cls(parent)
        obj.setText(text)
        return obj

    @classmethod
    def withIcon(cls, icon: QIcon, parent: T_WidgetParent = None) -> Self:
        obj = cls(parent)
        obj.setIcon(icon)
        return obj

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: T_WidgetParent = None) -> Self:
        obj = cls(parent)
        obj.setText(text)
        obj.setIcon(QIcon(icon))
        return obj

    def _initStyle(self):
        self.setFont(self.style_data.font)
        self.setIconSize(QSize(20, 20))

    @property
    def bottomBorderHeight(self) -> int:
        return self.style_data.border_height

    def reloadStyleData(self) -> None:
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

        text_rect = QRectF(
            (self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
            0,
            text_width,
            self.height() - self.style_data.border_height - 1,
        )
        pixmap_rect = QRect(
            (self.width() - icon_width - text_width - gap) // 2,
            ((self.height() - self.style_data.border_height) - icon_height) // 2,
            icon_width,
            icon_height,
        )

        return text_rect, pixmap_rect

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        self.scale_factor_ani.setFactor(1 / 16)
        self.scale_factor_ani.setBias(0)
        self.scale_factor_ani.setEndValue(0.9)
        self.scale_factor_ani.start()

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)
        self.scale_factor_ani.setFactor(1 / 4)
        self.scale_factor_ani.setBias(0.001)
        self.scale_factor_ani.setEndValue(1)
        self.scale_factor_ani.start()

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
        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        device_pixel_ratio = self.devicePixelRatioF()
        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        with createPainter(buffer, renderHints) as bufferPainter:
            self._drawBackgroundRect(bufferPainter, rect)
            self._drawButtonRect(bufferPainter, rect)
            self._drawHighLightRect(bufferPainter, rect)
            self._drawPixmapRect(bufferPainter, icon_rect)
            self._drawTextRect(bufferPainter, text_rect)

        a = self._scale_factor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)

        painter.drawPixmap(0, 0, buffer)


class SiProgressPushButton(SiPushButtonRefactor):
    def __init__(self, parent: T_WidgetParent = None) -> None:
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

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = LongPressButtonStyleData()
        self._progress = 0

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.Progress)
        self.progress_ani.init(-1 / 16, 0.12, 0, 0)

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
        self.progress_ani.fromProperty()
        self.update()

    def reloadStyleData(self) -> None:
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
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = FlatButtonStyleData()
        self._initStyle()
        self._scale_factor = 1

        self.scale_factor_ani = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.scale_factor_ani.init(1 / 16, 0, 1, 1)

    def _initStyle(self):
        self.setFont(self.style_data.font)
        self.setIconSize(QSize(20, 20))

    def reloadStyleData(self) -> None:
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

        text_rect = QRectF(
            (self.width() - icon_width - text_width - gap) / 2 + icon_width + gap, 0, text_width, self.height()
        )
        pixmap_rect = QRect(
            (self.width() - icon_width - text_width - gap) // 2,
            (self.height() - icon_height) // 2,
            icon_width,
            icon_height,
        )

        return text_rect, pixmap_rect

    def _onButtonClicked(self) -> None:
        self.highlight_ani.setCurrentValue(self.style_data.click_color)
        self.highlight_ani.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        device_pixel_ratio = self.devicePixelRatioF()

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        buffer_painter = QPainter(buffer)
        buffer_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        buffer_painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        buffer_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        buffer_painter.setPen(Qt.PenStyle.NoPen)

        self._drawButtonRect(buffer_painter, rect)
        self._drawHighLightRect(buffer_painter, rect)
        self._drawPixmapRect(buffer_painter, icon_rect)
        self._drawTextRect(buffer_painter, text_rect)
        buffer_painter.end()

        a = self._scale_factor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)

        painter.drawPixmap(0, 0, buffer)

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

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.scale_factor_ani.setFactor(1 / 16)
        self.scale_factor_ani.setBias(0)
        self.scale_factor_ani.setEndValue(0.9)
        self.scale_factor_ani.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.scale_factor_ani.setFactor(1 / 4)
        self.scale_factor_ani.setBias(0.001)
        self.scale_factor_ani.setEndValue(1)
        self.scale_factor_ani.start()


class SiFlatButtonWithIndicator(SiFlatButton):
    class Property:
        ScaleFactor = "scaleFactor"
        TextColor = "textColor"
        ButtonRectColor = "buttonRectColor"
        HighlightRectColor = "highlightRectColor"
        BackgroundRectColor = "backgroundRectColor"
        IndicatorColor = "indicatorColor"
        IndicatorWidth = "indicatorWidth"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setCheckable(True)

        self._indicator_width = 0
        self._indicator_color = self.style_data.indicator_idle_color

        self.indi_width_ani = SiExpAnimationRefactor(self, self.Property.IndicatorWidth)
        self.indi_width_ani.init(1/3, 0.001, 0, 0)

        self.indi_color_ani = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.indi_color_ani.init(1/6, 0.001, self._indicator_color, self._indicator_color)

        self.toggled.connect(self._onButtonToggled)

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indicator_color

    @indicatorColor.setter
    def indicatorColor(self, value: QColor):
        self._indicator_color = value
        self.update()

    @pyqtProperty(float)
    def indicatorWidth(self):
        return self._indicator_width

    @indicatorWidth.setter
    def indicatorWidth(self, value: float):
        self._indicator_width = value
        self.update()

    def _onButtonToggled(self, state: bool) -> None:
        if state is True:
            self.indi_width_ani.setEndValue((self.width() - 24) * 0.618)
            self.indi_width_ani.start()

            self.indi_color_ani.setCurrentValue(self.style_data.indicator_flash_color)
            self.indi_color_ani.setEndValue(self.style_data.indicator_selected_color)
            self.indi_color_ani.start()

            if not self.underMouse():
                self.highlight_ani.setEndValue(self.style_data.hover_color)
                self.highlight_ani.start()

        else:
            self.indi_width_ani.setEndValue(0)
            self.indi_width_ani.start()

            self.indi_color_ani.setEndValue(self.style_data.indicator_idle_color)
            self.indi_color_ani.start()

            if not self.underMouse():
                self.highlight_ani.setEndValue(self.style_data.idle_color)
                self.highlight_ani.start()

    def _drawIndicatorRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, 1, 1)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._indicator_color)
        painter.drawPath(path)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)

        if not self.isChecked():
            self.indi_color_ani.setEndValue(self.style_data.indicator_hover_color)
            self.indi_color_ani.start()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)

        if not self.isChecked():
            self.indi_color_ani.setEndValue(self.style_data.indicator_idle_color)
            self.indi_color_ani.start()

            self.highlight_ani.setEndValue(self.style_data.idle_color)
            self.highlight_ani.start()

        else:
            self.highlight_ani.setEndValue(self.style_data.hover_color)
            self.highlight_ani.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        device_pixel_ratio = self.devicePixelRatioF()

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        buffer_painter = QPainter(buffer)
        buffer_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        buffer_painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        buffer_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        buffer_painter.setPen(Qt.PenStyle.NoPen)

        self._drawButtonRect(buffer_painter, rect)
        self._drawHighLightRect(buffer_painter, rect)
        self._drawPixmapRect(buffer_painter, icon_rect)
        self._drawTextRect(buffer_painter, text_rect)
        buffer_painter.end()

        a = self._scale_factor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)

        painter.drawPixmap(0, 0, buffer)

        indi_w = self._indicator_width
        indicator_rect = QRectF((self.width() - indi_w) / 2, self.height() - 2, indi_w, 2)

        self._drawIndicatorRect(painter, indicator_rect)


class SiToggleButtonRefactor(SiFlatButton):
    def __init__(self, parent: T_WidgetParent = None) -> None:
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
        self._onButtonToggled(self.isChecked())
        self.update()

    def _onButtonToggled(self, state: bool) -> None:
        sd = self.style_data
        if state:
            self.toggle_btn_color_ani.setEndValue(sd.toggled_button_color)
            self.toggle_text_color_ani.setEndValue(sd.toggled_text_color)
            self.toggle_btn_color_ani.start()
            self.toggle_text_color_ani.start()
        else:
            self.toggle_btn_color_ani.setEndValue(sd.button_color)
            self.toggle_text_color_ani.setEndValue(sd.text_color)
            self.toggle_btn_color_ani.start()
            self.toggle_text_color_ani.start()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._button_rect_color)  # use property variable
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self._text_color)  # use property variable
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())


# @dataclass
class SwitchStyleData(QObject):
    STYLE_TYPES = ["Switch"]

    background_color_starting: QColor = QColor("#cea6ea")
    background_color_ending: QColor = QColor("#cea6ea")
    frame_color: QColor = QColor("#D1CBD4")
    thumb_color_checked: QColor = QColor("#0f0912")
    thumb_color_unchecked: QColor = QColor("#D1CBD4")


class SiSwitchRefactor(QPushButton):
    class Property:
        Progress = "progress"
        ScaleFactor = "scaleFactor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)

        self.style_data = SwitchStyleData()
        self._progress = 0
        self._scale_factor = 1

        self._initStyle()

        self.scale_factor_ani = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.scale_factor_ani.init(1 / 16, 0, 1, 1)

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.Progress)
        self.progress_ani.init(1 / 4, 0.01, 0, 0)

        self.clicked.connect(self._onClicked)

    def _initStyle(self) -> None:
        self.setFixedSize(40, 20)

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value: float):
        self._scale_factor = value
        self.update()

    @pyqtProperty(float)
    def progress(self) -> float:
        return self._progress

    @progress.setter
    def progress(self, value: float) -> None:
        self._progress = value
        self.update()

    def _onClicked(self):
        if self.isChecked():
            self.progress_ani.setEndValue(1)
            self.progress_ani.start()
        else:
            self.progress_ani.setEndValue(0)
            self.progress_ani.start()

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = rect.height() / 2
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawFramePath(self, rect: QRect) -> QPainterPath:
        width = 0.5
        radius = rect.height() / 2
        path = QPainterPath()
        path.addRoundedRect(QRectF(width, width, rect.width() - 2 * width, rect.height() - 2 * width), radius, radius)
        return path

    def _drawThumbPath(self, rect: QRect) -> QPainterPath:
        p = self._progress
        radius = rect.height() / 2 - 3
        width = radius * 2 + (p * (1 - p)) ** 1 * 16
        height = radius * 2
        track_length = rect.width() - width - 6
        x = 3 + track_length * p
        y = 3
        path = QPainterPath()
        path.addRoundedRect(QRectF(x, y, width, height), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        if self._progress > 0.5:
            gradient = QLinearGradient(0, 0, rect.width(), rect.height())
            gradient.setColorAt(0, self.style_data.background_color_starting)
            gradient.setColorAt(1, self.style_data.background_color_ending)

            painter.setBrush(gradient)
            painter.drawPath(self._drawBackgroundPath(rect))

    def _drawFrameRect(self, painter: QPainter, rect: QRect) -> None:
        if self._progress <= 0.5:
            pen = QPen(self.style_data.frame_color)
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawPath(self._drawFramePath(rect))
            painter.setPen(Qt.NoPen)

    def _drawThumbRect(self, painter: QPainter, rect: QRect) -> None:
        color = self.style_data.thumb_color_checked if self._progress > 0.5 else self.style_data.thumb_color_unchecked
        painter.setBrush(color)
        painter.drawPath(self._drawThumbPath(rect))

    def paintEvent(self, a0) -> None:
        rect = self.rect()
        device_pixel_ratio = self.devicePixelRatioF()

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        buffer_painter = QPainter(buffer)
        buffer_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        buffer_painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        buffer_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        buffer_painter.setPen(Qt.PenStyle.NoPen)

        self._drawBackgroundRect(buffer_painter, rect)
        self._drawFrameRect(buffer_painter, rect)
        self._drawThumbRect(buffer_painter, rect)
        buffer_painter.end()

        a = self._scale_factor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)

        painter.drawPixmap(0, 0, buffer)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.scale_factor_ani.setFactor(1 / 16)
        self.scale_factor_ani.setBias(0)
        self.scale_factor_ani.setEndValue(0.9)
        self.scale_factor_ani.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.scale_factor_ani.setFactor(1 / 4)
        self.scale_factor_ani.setBias(0.001)
        self.scale_factor_ani.setEndValue(1)
        self.scale_factor_ani.start()


# @dataclass
class RadioButtonStyleData(QObject):
    STYLE_TYPES = ["Button"]

    text_color = QColor("#D1CBD4")
    description_color = QColor("#918497")

    indicator_border_radius: float = 9.5
    indicator_allocated_width: int = 60
    indicator_hover_additional_width: int = 2
    indicator_height: int = 19

    avatar_width: int = 36
    avatar_height: int = 36
    avatar_border_radius: int = 18

    highlight_idle_color: QColor = QColor("#00baadc7")
    highlight_flash_color: QColor = QColor("#90baadc7")
    highlight_hover_color: QColor = QColor("#40baadc7")

    unchecked_indicator_color: QColor = QColor("#25222A")
    unchecked_indicator_width: float = 33

    checked_indicator_color: QColor = QColor("#a681bf")
    checked_indicator_width: float = 51


class RadioButtonStyleDataR:
    text_color = QColor("#D1CBD4")
    indicator_idle_color = QColor("#332e38")
    indicator_idle_strike_color = QColor("#25222A")

    indicator_hover_strike_color = QColor("#4c4453")

    indicator_flash_color = QColor("#4c4453")
    indicator_flash_strike_color = QColor("#FFFFFF")

    indicator_selected_color = QColor("#332E38")
    indicator_selected_strike_color = QColor("#cea6ea")


class SiRadioButtonR(QRadioButton):
    class Property:
        ScaleFactor = "scaleFactor"
        IndicatorColor = "indicatorColor"
        IndicatorSpinProg = "indicatorSpinProg"
        IndicatorStrikeColor = "indicatorStrikeColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = RadioButtonStyleDataR()

        self._scale_factor = 1
        self._indi_spin_prog = 1
        self._indi_color = self.style_data.indicator_idle_color
        self._indi_strike_color = self.style_data.indicator_idle_strike_color

        self.scale_factor_ani = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.scale_factor_ani.init(1/16, 0, 1, 1)

        self.indi_spin_prog_ani = SiExpAnimationRefactor(self, self.Property.IndicatorSpinProg)
        self.indi_spin_prog_ani.init(1/5, 0.0001, 1, 1)

        self.indi_color_ani = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.indi_color_ani.init(1/8, 0.001, self._indi_color, self._indi_color)

        self.indi_strike_color_ani = SiExpAnimationRefactor(self, self.Property.IndicatorStrikeColor)
        self.indi_strike_color_ani.init(1/4, 0.001, self._indi_strike_color, self._indi_strike_color)

        self._initStyle()
        self.toggled.connect(self._onToggled)

    def _initStyle(self):
        self.setFont(SiFont.getFont(size=14))
        self.setStyleSheet(
            "QRadioButton::indicator { width: 0px; height: 0px; }"
            "QRadioButton {"
            f"    color: {self.style_data.text_color.name()};"
            "     margin: 7px 0px 8px 24px"
            "}"
        )

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value: float):
        self._scale_factor = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indi_color

    @indicatorColor.setter
    def indicatorColor(self, value: QColor):
        self._indi_color = value
        self.update()

    @pyqtProperty(float)
    def indicatorSpinProg(self):
        return self._indi_spin_prog

    @indicatorSpinProg.setter
    def indicatorSpinProg(self, value: float):
        self._indi_spin_prog = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorStrikeColor(self):
        return self._indi_strike_color

    @indicatorStrikeColor.setter
    def indicatorStrikeColor(self, value: QColor):
        self._indi_strike_color = value
        self.update()

    def _onToggled(self, state):
        if state:
            self.indi_spin_prog_ani.setCurrentValue(0)
            self.indi_spin_prog_ani.setEndValue(1)
            self.indi_spin_prog_ani.start()

            self.indi_color_ani.setCurrentValue(self.style_data.indicator_flash_color)
            self.indi_color_ani.setEndValue(self.style_data.indicator_selected_color)
            self.indi_color_ani.start()

            self.indi_strike_color_ani.setCurrentValue(self.style_data.indicator_flash_strike_color)
            self.indi_strike_color_ani.setEndValue(self.style_data.indicator_selected_strike_color)
            self.indi_strike_color_ani.start()

        else:
            self.indi_color_ani.setEndValue(self.style_data.indicator_idle_color)
            self.indi_color_ani.start()

            self.indi_strike_color_ani.setEndValue(self.style_data.indicator_idle_strike_color)
            self.indi_strike_color_ani.start()

    def _drawIndicatorBackgroundEllipse(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addEllipse(rect)

        painter.setBrush(self._indi_color)
        painter.drawPath(path)

    def _drawIndicatorStrike(self, painter: QPainter, rect: QRectF) -> None:
        rect.adjust(2.5, 2.5, -2.5, -2.5)

        start_angle = 360 * 16 + 120 * 16 * self._indi_spin_prog
        span_angle = 360 * 16 * self._indi_spin_prog

        pen = QPen(self._indi_strike_color, 5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)
        painter.drawArc(rect, int(start_angle), int(span_angle))

    def _drawBufferToSelf(self, painter: QPainter,
                          buffer_rect: QRectF,
                          target_rect: QRectF,
                          buffer: QPixmap) -> None:
        br = buffer_rect.toRect()
        tr = target_rect.toRect()
        a = self._scale_factor

        painter.translate(QPointF(tr.width() * (1 - a) / 2, tr.height() * (1 - a) / 2))
        painter.scale(a, a)

        painter.drawPixmap((tr.width() - br.width()) // 2 + tr.x(),
                           (tr.height() - br.height()) // 2 + tr.y(), buffer)

    def paintEvent(self, a0):
        super().paintEvent(a0)

        device_pixel_ratio = self.devicePixelRatioF()
        indicator_rect = QRectF(0, 0, 24, 24)
        buffer_rect = QRectF(0, 0, 24, 24)
        buffer_target_rect = QRectF(0, (self.height() - 24) / 2, 24, 24)

        buffer = QPixmap(buffer_rect.size().toSize() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(buffer) as painter:
            self._drawIndicatorBackgroundEllipse(painter, indicator_rect)
            self._drawIndicatorStrike(painter, indicator_rect)

        with createPainter(self, renderHints) as painter:
            self._drawBufferToSelf(painter, buffer_rect, buffer_target_rect, buffer)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        self.scale_factor_ani.setFactor(1 / 16)
        self.scale_factor_ani.setBias(0)
        self.scale_factor_ani.setEndValue(0.8)
        self.scale_factor_ani.start()

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)
        self.scale_factor_ani.setFactor(1 / 4)
        self.scale_factor_ani.setBias(0.001)
        self.scale_factor_ani.setEndValue(1)
        self.scale_factor_ani.start()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        if self.isChecked() is False:
            self.indi_strike_color_ani.setEndValue(self.style_data.indicator_hover_strike_color)
            self.indi_strike_color_ani.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        if self.isChecked() is False:
            self.indi_strike_color_ani.setEndValue(self.style_data.indicator_idle_strike_color)
            self.indi_strike_color_ani.start()


class SiRadioButtonRefactor(QRadioButton):
    class Property:
        IndicatorWidthProg = "indicatorWidthProg"
        IndicatorHoverWidth = "indicatorHoverWidth"
        IndicatorColor = "indicatorColor"
        HighlightRectColor = "highlightRectColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = RadioButtonStyleData()
        self._description = ""
        self._indi_hover_width = 0
        self._indi_width_prog = 0
        self._indi_color = self.style_data.unchecked_indicator_color
        self._hl_color = self.style_data.highlight_idle_color

        self.indi_width_ani = SiExpAnimationRefactor(self, self.Property.IndicatorWidthProg)
        self.indi_width_ani.init(1 / 6, 0.015, 0, 0)

        self.indi_hover_width_ani = SiExpAnimationRefactor(self, self.Property.IndicatorHoverWidth)
        self.indi_hover_width_ani.init(1 / 4, 0.01, 0, 0)

        self.indi_color_ani = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.indi_color_ani.init(1 / 3, 1, self._indi_color, self._indi_color)

        self.highlight_color_ani = SiExpAnimationRefactor(self, self.Property.HighlightRectColor)
        self.highlight_color_ani.init(1 / 8, 0.1, self._hl_color, self._hl_color)

        self.toggled.connect(self._onButtonToggled)

        self._initStyle()

    def _initStyle(self) -> None:
        self.setFont(SiFont.getFont(size=13))

    @pyqtProperty(float)
    def indicatorWidthProg(self):
        return self._indi_width_prog

    @indicatorWidthProg.setter
    def indicatorWidthProg(self, value: float):
        self._indi_width_prog = value
        self.update()

    @pyqtProperty(float)
    def indicatorHoverWidth(self):
        return self._indi_hover_width

    @indicatorHoverWidth.setter
    def indicatorHoverWidth(self, value: float):
        self._indi_hover_width = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indi_color

    @indicatorColor.setter
    def indicatorColor(self, value: QColor):
        self._indi_color = value
        self.update()

    @pyqtProperty(QColor)
    def highlightRectColor(self):
        return self._hl_color

    @highlightRectColor.setter
    def highlightRectColor(self, value: QColor):
        self._hl_color = value
        self.update()

    def _indicatorWidthInterpolation(self, p: float) -> float:
        start = self.style_data.unchecked_indicator_width
        end = self.style_data.checked_indicator_width
        return start + (end - start) * 3 * p / (2 * p ** 2 + 1)

    def _drawIndicatorPath(self, rect: QRect) -> QPainterPath:
        alloc_width = self.style_data.indicator_allocated_width
        radius = self.style_data.indicator_border_radius
        width = (self._indicatorWidthInterpolation(self._indi_width_prog) +
                 self._indi_hover_width * ((self._indi_width_prog + 1) / 2))
        path = QPainterPath()
        path.addRoundedRect(QRectF(alloc_width - width, rect.y(), width, rect.height()), radius, radius)
        return path

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._indi_color)
        painter.drawPath(self._drawIndicatorPath(rect))

    def _drawHighlightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setCompositionMode(QPainter.CompositionMode_Plus)
        painter.setBrush(self._hl_color)
        painter.drawPath(self._drawIndicatorPath(rect))
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    def _drawIndicatorInnerPath(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(28.5, 8, self.style_data.unchecked_indicator_width - 6, rect.height() - 8), 6, 6)
        return path

    def _drawIndicatorInnerRect(self, painter: QPainter, rect: QRect) -> None:
        if self.isChecked():
            painter.setBrush(self.style_data.unchecked_indicator_color)
            painter.drawPath(self._drawIndicatorInnerPath(rect))

    def _drawNameTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.text_color)
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())
        painter.setPen(Qt.NoPen)

    def _onButtonToggled(self) -> None:
        sd = self.style_data
        if self.isChecked():
            self.indi_width_ani.setEndValue(1)
            self.indi_color_ani.setEndValue(sd.checked_indicator_color)
            self.indi_color_ani.setCurrentValue(sd.checked_indicator_color)
            self.setProperty(self.Property.IndicatorColor, sd.checked_indicator_color)
        else:
            self.indi_width_ani.setEndValue(0)
            self.indi_width_ani.setCurrentValue(0.5)
            self.indi_color_ani.setEndValue(sd.unchecked_indicator_color)

        self.indi_width_ani.start()
        self.indi_color_ani.start()

    def sizeHint(self) -> QSize:
        return QSize(super().sizeHint().width() + self.style_data.indicator_allocated_width, 24)

    def paintEvent(self, a0) -> None:
        rect = self.rect()
        indi_rect = QRect(0, 4, self.style_data.indicator_allocated_width, self.style_data.indicator_height)
        text_rect = QRect(indi_rect.width() + 22, 0, rect.width() - indi_rect.width() - 22, 26)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawIndicatorRect(painter, indi_rect)
            self._drawHighlightRect(painter, indi_rect)
            self._drawIndicatorInnerRect(painter, indi_rect)
            self._drawNameTextRect(painter, text_rect)

    def enterEvent(self, a0) -> None:
        super().enterEvent(a0)
        self.indi_hover_width_ani.setEndValue(self.style_data.indicator_hover_additional_width)
        self.indi_hover_width_ani.start()
        self.highlight_color_ani.setCurrentValue(self.style_data.highlight_flash_color)
        self.highlight_color_ani.setEndValue(self.style_data.highlight_hover_color)
        self.highlight_color_ani.start()

    def leaveEvent(self, a0) -> None:
        super().leaveEvent(a0)
        self.indi_hover_width_ani.setEndValue(0)
        self.indi_hover_width_ani.start()
        self.highlight_color_ani.setEndValue(self.style_data.highlight_idle_color)
        self.highlight_color_ani.start()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.click()


class SiRadioButtonWithDescription(SiRadioButtonRefactor):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.desc_label = QLabel(self)
        self.desc_label.setStyleSheet("color: #918497")
        self.desc_label.setFont(SiFont.getFont(size=12))
        self.desc_label.setWordWrap(True)
        self.desc_label.setFixedWidth(180)
        self.desc_label.move(self.style_data.indicator_allocated_width + 22, 24)

    def setDescription(self, desc: str) -> None:
        self.desc_label.setText(desc)

    def setDescriptionWidth(self, width: int) -> None:
        self.desc_label.setFixedWidth(width)

    def sizeHint(self) -> QSize:
        sd = self.style_data
        width = max(self.desc_label.width(), super().sizeHint().width()) + sd.indicator_allocated_width + 22
        height = self.desc_label.sizeHint().height() + 24
        return QSize(width, height)

    def adjustSize(self) -> None:
        super().adjustSize()
        self.desc_label.adjustSize()


class SiRadioButtonWithAvatar(SiRadioButtonRefactor):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self._description = ""
        self._description_font = SiFont.getFont(size=12)

    def _initStyle(self) -> None:
        self.setFont(SiFont.getFont(size=14))

    def setDescription(self, text: str) -> None:
        self._description = text
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(super().sizeHint().width() + self.style_data.avatar_width + 12, 36)

    def _drawIndicatorInnerPath(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(28.5, 12, self.style_data.unchecked_indicator_width - 6, rect.height() - 8), 6, 6)
        return path

    def _drawDescriptionTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.description_color)
        painter.setFont(self._description_font)
        painter.drawText(rect, Qt.AlignTop | Qt.AlignLeft, self._description)
        painter.setPen(Qt.NoPen)

    def _drawAvatarIcon(self, painter: QPainter, rect: QRect) -> None:
        device_pixel_ratio = self.devicePixelRatioF()

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        buffer_painter = QPainter(buffer)
        buffer_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        buffer_painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        buffer_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        buffer_painter.setPen(Qt.PenStyle.NoPen)

        width = self.style_data.avatar_width
        height = self.style_data.avatar_height
        border_radius = self.style_data.avatar_border_radius
        x = (rect.width() - width) // 2
        y = (rect.height() - height) // 2
        target_rect = QRect(x, y, width, height)
        size = QSize(width, height) * device_pixel_ratio

        path = QPainterPath()
        path.addRoundedRect(x, y,
                            width, height,
                            border_radius, border_radius)

        buffer_painter.setClipPath(path)
        buffer_painter.drawPixmap(target_rect, self.icon().pixmap(size))
        buffer_painter.end()

        painter.drawPixmap(rect, buffer)

    def paintEvent(self, a0) -> None:
        rect = self.rect()
        sd = self.style_data
        indi_rect = QRect(0, 8, sd.indicator_allocated_width, sd.indicator_height)
        avatar_rect = QRect(indi_rect.width() + 22, 0, sd.avatar_width, sd.avatar_height)
        text_rect = QRect(indi_rect.width() + 22 + sd.avatar_width + 12, 3, rect.width() - indi_rect.width() - 22, 14)
        desc_rect = QRect(indi_rect.width() + 22 + sd.avatar_width + 12, 19, rect.width() - indi_rect.width() - 22, 18)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawIndicatorRect(painter, indi_rect)
            self._drawHighlightRect(painter, indi_rect)
            self._drawIndicatorInnerRect(painter, indi_rect)
            self._drawAvatarIcon(painter, avatar_rect)
            self._drawNameTextRect(painter, text_rect)
            self._drawDescriptionTextRect(painter, desc_rect)
