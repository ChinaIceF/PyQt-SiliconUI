# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtCore import (
    QEvent,
    QMargins,
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
    QTextOption,
    QTransform,
)
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QAbstractButton, QLabel, QPushButton, QRadioButton, QSizePolicy
from typing_extensions import Self

from siui.core import GlobalFont, SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.event_filter import ScaleOnPressEventFilter, WidgetToolTipRedirectEventFilter
from siui.core.painter import getGaussianLinearGradient, getRoundedRectPathArc
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
                SA.BorderInnerRadius: 8,
                SA.BorderRadius: 11,
                SA.BorderHeight: 3,
                SA.IconTextGap: 4,
            },
            "LongPressButtonStyleData": {
                SA.ProgressColor: QColor("#DA3462"),
                SA.ButtonColor: QColor("#932a48"),
                SA.BackgroundColor: QColor("#642d41"),
                SA.ClickColor: QColor("#40FFFFFF"),
            },
            "FlatButtonStyleData": {
                SA.ButtonColor: QColor("#004C4554"),
                SA.BorderRadius: 7,
            },
            "ToggleButtonStyleData": {
                SA.ButtonColor: QColor("#004C4554"),
                SA.BorderRadius: 7,
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
    indicator_hover_color = QColor("#D087DF")
    indicator_selected_color = QColor("#D087DF")
    indicator_flash_color = QColor("#F5EBF9")
    indicator_idle_color = QColor("#00D087DF")


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
        preferred_height = max(36, text_height, icon_height)
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
            self.height() - self.style_data.border_height - 2,
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

    checked_indicator_color: QColor = QColor("#D087DF")
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


class TransparentButtonStyleData:
    hover_overlay_color_idle = QColor("#00baadc7")
    hover_overlay_color_hovered = QColor("#1abaadc7")
    hover_overlay_color_flash = QColor("#50baadc7")


class SiTransparentButton(QAbstractButton):
    class Property:
        HoverOverlayColor = "hoverOverlayColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = TransparentButtonStyleData()

        self._is_pressed = False
        self._border_radius = 4
        self._hover_overlay_color = self.style_data.hover_overlay_color_idle

        self.ani_hover_overlay_color = SiExpAnimationRefactor(self, self.Property.HoverOverlayColor)
        self.ani_hover_overlay_color.init(1/8, 1, self._hover_overlay_color, self._hover_overlay_color)

    @pyqtProperty(QColor)
    def hoverOverlayColor(self):
        return self._hover_overlay_color

    @hoverOverlayColor.setter
    def hoverOverlayColor(self, value):
        self._hover_overlay_color = value
        self.update()

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.HoverOverlayColor: self.ani_hover_overlay_color,
        }.get(prop_name)

    def setBorderRadius(self, r: int) -> None:
        self._border_radius = r
        self.update()

    def borderRadius(self) -> int:
        return self._border_radius

    def flash(self) -> None:
        self.ani_hover_overlay_color.setCurrentValue(self.style_data.hover_overlay_color_flash)
        self.ani_hover_overlay_color.start()

    def hover(self) -> None:
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_color_hovered)
        self.ani_hover_overlay_color.start()

    def leave(self) -> None:
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_color_idle)
        self.ani_hover_overlay_color.start()

    def _drawHoverOverlayRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), self._border_radius, self._border_radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._hover_overlay_color)
        painter.drawPath(path)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.hover()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.leave()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self._is_pressed = True

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._is_pressed = False

        if self.rect().contains(e.pos()):
            self.flash()

    def paintEvent(self, e):
        rect = self.rect()

        with createPainter(self) as painter:
            self._drawHoverOverlayRect(painter, rect)


class CheckBoxStyleData:
    flash_start_color = QColor("#50baadc7")
    flash_end_color = QColor("#00baadc7")
    hover_idle_color = QColor("#00baadc7")
    hover_active_color = QColor("#1abaadc7")
    title_normal_color = QColor("#D1CBD4")
    title_bold_color = QColor("#FFFFFF")
    description_color = QColor("#918497")
    indicator_deactivated_color = QColor("#25222A")
    indicator_activated_color = QColor("#D087DF")


class SiCheckBoxRefactor(QAbstractButton):
    class Property:
        FlashColor = "flashColor"
        HoverColor = "hoverColor"
        ScaleFactor = "scaleFactor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = CheckBoxStyleData()

        self._font_title_bold = SiFont.getFont(size=14, weight=SiFont.Weight.Bold)
        self._font_title_normal = SiFont.getFont(size=14)
        self._font_description = SiFont.getFont(size=12)

        self._flash_color = self.style_data.flash_end_color
        self._hover_color = self.style_data.hover_idle_color
        self._scale_factor = 1
        self._description_text = ""

        self.ani_flash_color = SiExpAnimationRefactor(self, self.Property.FlashColor)
        self.ani_flash_color.init(1/8, 1, self._flash_color, self._flash_color)

        self.ani_hover_color = SiExpAnimationRefactor(self, self.Property.HoverColor)
        self.ani_hover_color.init(1/8, 1, self._hover_color, self._hover_color)

        self.ani_scale_factor = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.ani_scale_factor.init(1/8, 0.001, self._scale_factor, self._scale_factor)

        self._title_label = QLabel(self)
        self._description_label = QLabel(self)
        self._title_label.setVisible(False)
        self._description_label.setVisible(False)

        self.resize(274, 64)
        self.setMinimumHeight(64)
        self.setCheckable(True)
        self._initStyle()
        self._initToolTipRedirectEventFilter()
        self._initScaleOnPressEventFilter()

    def _initStyle(self) -> None:
        self._title_label.setFont(self._font_title_normal)
        self._title_label.setStyleSheet(f"color: {self.style_data.title_normal_color.name()}")

        self._description_label.setFont(self._font_description)
        self._description_label.setStyleSheet(f"color: {self.style_data.description_color.name()}")
        self._description_label.setWordWrap(True)

    def _initToolTipRedirectEventFilter(self) -> None:
        self._tooltip_manager = WidgetToolTipRedirectEventFilter()
        self.installEventFilter(self._tooltip_manager)

    def _initScaleOnPressEventFilter(self) -> None:
        self._scale_manager = ScaleOnPressEventFilter(self)
        self._scale_manager.setMinScaleFactor(0.95)
        self.installEventFilter(self._scale_manager)

    @pyqtProperty(QColor)
    def flashColor(self):
        return self._flash_color

    @flashColor.setter
    def flashColor(self, value):
        self._flash_color = value
        self.update()

    @pyqtProperty(QColor)
    def hoverColor(self):
        return self._hover_color

    @hoverColor.setter
    def hoverColor(self, value):
        self._hover_color = value
        self.update()

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value):
        self._scale_factor = value
        self.update()

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, w: int) -> int:
        margins = QMargins(64, 12, 28, 12)
        content_width = w - margins.left() - margins.right()  # 最小宽度为 300

        # 计算标题高度
        title_metrics = QFontMetrics(self._font_title_normal)
        title_rect = title_metrics.boundingRect(
            QRect(0, 0, content_width, 10000),  # 高度足够大以容纳多行
            Qt.TextWordWrap,
            self.text()
        )
        title_height = title_rect.height()

        # 间距 + 描述文字高度
        description_metrics = QFontMetrics(self._font_description)
        desc_rect = description_metrics.boundingRect(
            QRect(0, 0, content_width, 10000),
            Qt.TextWordWrap,
            self._description_text
        )
        description_height = desc_rect.height()

        spacing_between = 4
        content_height = title_height + spacing_between + description_height

        total_height = content_height + margins.top() + margins.bottom()

        return total_height

    def sizeHint(self):
        return QSize(self.width(), self.heightForWidth(self.width()))

    def resizeEvent(self, a0):
        self.updateGeometry()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.ani_hover_color.setEndValue(self.style_data.hover_active_color)
        self.ani_hover_color.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.ani_hover_color.setEndValue(self.style_data.hover_idle_color)
        self.ani_hover_color.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.ani_flash_color.setCurrentValue(self.style_data.flash_start_color)
        self.ani_flash_color.setEndValue(self.style_data.flash_end_color)
        self.ani_flash_color.start()

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.FlashColor: self.ani_flash_color,
            self.Property.HoverColor: self.ani_hover_color,
            self.Property.ScaleFactor: self.ani_scale_factor,
        }.get(prop_name)

    def setDescription(self, text) -> None:
        self._description_text = text

    def description(self) -> str:
        return self._description_text

    def _getCheckmarkPath(self) -> QPainterPath:
        points = [QPointF(x, y) for x, y in [
            (9.76497, 3.20474), (10.0661, 3.48915), (9.79526, 4.26497),
            (5.54526, 8.76497), (5.40613, 8.91228), (5.01071, 8.99993),
            (4.8081, 9.00282), (4.46967, 8.78033), (2.21967, 6.53033),
            (1.92678, 6.23744), (2.21967, 5.46967), (2.51256, 5.17678),
            (3.28033, 5.46967), (4.98463, 7.17397), (8.70474, 3.23503),
            (8.98915, 2.9339), (9.76497, 3.20474)
        ]]

        quad_control_end_pairs = [
            (1, 2), (2, 3), (4, 5), (6, 7), (7, 8),
            (9, 10), (11, 12), (12, 13), (13, 14), (15, 16)
        ]

        path = QPainterPath()
        path.moveTo(points[0])
        for control_idx, end_idx in quad_control_end_pairs:
            path.quadTo(points[control_idx], points[end_idx])
        path.closeSubpath()

        transform = QTransform()
        transform.scale(1.75, 1.75)

        return transform.map(path)

    def _drawHoverRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 12, 12)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._hover_color)
        painter.drawPath(path)

    def _drawFlashRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 12, 12)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._flash_color)
        painter.drawPath(path)

    def _drawTitleText(self, painter: QPainter, rect: QRect) -> None:
        option = QTextOption()
        option.setWrapMode(QTextOption.WordWrap)
        painter.setFont(self._font_title_normal)
        painter.setPen(self.style_data.title_normal_color)
        painter.drawText(QRectF(rect), self.text(), option)

    def _drawDescriptionText(self, painter: QPainter, rect: QRect) -> None:
        option = QTextOption()
        option.setWrapMode(QTextOption.WordWrap)
        painter.setFont(self._font_description)
        painter.setPen(self.style_data.description_color)
        painter.drawText(QRectF(rect), self._description_text, option)

    def _drawIndicator(self, painter: QPainter, rect: QRect) -> None:
        checkmark_path = self._getCheckmarkPath()
        checkmark_path.translate(rect.center() - QPointF(9.5, 9.25))

        if self.autoExclusive():
            outer_path = QPainterPath()
            outer_path.addEllipse(QRectF(rect))
            inner_path = QPainterPath()
            inner_path.addEllipse(QRectF(rect.marginsRemoved(QMargins(5, 5, 5, 5))))

        else:
            outer_path = QPainterPath()
            outer_path.addRoundedRect(QRectF(rect), 8, 8)
            inner_path = QPainterPath()
            inner_path.addRoundedRect(QRectF(rect.marginsRemoved(QMargins(5, 5, 5, 5))), 3, 3)

        if self.isChecked():
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.style_data.indicator_activated_color)
            painter.drawPath(outer_path - checkmark_path)

        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.style_data.indicator_deactivated_color)
            painter.drawPath(outer_path - inner_path)

    def _drawBuffer(self, painter: QPainter, buffer: QPixmap, rect: QRect):
        a = self._scale_factor
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)
        painter.drawPixmap(rect, buffer)

    def paintEvent(self, e):
        full_rect = self.rect()
        margin = QMargins(64, 12, 28, 12)
        content_rect = full_rect.marginsRemoved(margin)

        # Indicator 固定位置
        indicator_rect = QRect(20, 20, 24, 24)

        # Title 占一行（定高）
        title_height = 18
        title_rect = QRect(content_rect.left(), content_rect.top(),
                           content_rect.width(), title_height)

        # Description 从 title 底下开始，占剩下空间
        spacing = 4
        description_rect = QRect(content_rect.left(),
                                 title_rect.bottom() + spacing,
                                 content_rect.width(),
                                 content_rect.bottom() - (title_rect.bottom() + spacing))

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        buffer = QPixmap(full_rect.size() * self.devicePixelRatioF())
        buffer.setDevicePixelRatio(self.devicePixelRatioF())
        buffer.fill(Qt.transparent)

        with createPainter(buffer) as painter:
            self._drawHoverRect(painter, full_rect)
            self._drawIndicator(painter, indicator_rect)
            self._drawTitleText(painter, title_rect)
            self._drawDescriptionText(painter, description_rect)
            self._drawFlashRect(painter, full_rect)

        with createPainter(self, renderHints) as painter:
            self._drawBuffer(painter, buffer, full_rect)


class CapsuleButtonStyleData:
    label_background_color = QColor("#29252E")
    label_text_color = QColor("#D1CBD4")
    value_background_color_deactivated = QColor("#201D24")
    value_background_color_flash = QColor("#FFFFFF")
    value_background_color_activated = QColor("#78E09A")
    value_text_color_deactivated = QColor("#D1CBD4")
    value_text_color_activated = QColor("#000000")
    hover_overlay_idle = QColor("#00202020")
    hover_overlay_hovered = QColor("#202020")
    hover_overlay_flash = QColor("#7F7F7F")
    indicator_color = QColor("#519868")


class SiCapsuleButton(QAbstractButton):
    class Property:
        LabelBackgroundColor = "labelBackgroundColor"
        LabelTextColor = "labelTextColor"
        ValueBackgroundColor = "valueBackgroundColor"
        ValueTextColor = "valueTextColor"
        HoverOverlayColor = "hoverOverlayColor"
        ValueYOffset = "valueYOffset"
        ScaleFactor = "scaleFactor"

    class Theme:
        Green = QColor("#78E09A")
        Yellow = QColor("#FFD467")
        Red = QColor("#FF6767")

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setFont(SiFont.getFont(size=14))
        self.setCheckable(True)

        self._value = 0
        self._label_margin = QMargins(18, 0, 18, 0)
        self._value_margin = QMargins(16, 0, 16, 0)
        self._indicator_margin = QMargins(12, 0, 12, 0)

        self.style_data = CapsuleButtonStyleData()

        self._label_bg_color = self.style_data.label_background_color
        self._label_text_color = self.style_data.label_text_color
        self._value_bg_color = self.style_data.value_background_color_deactivated
        self._value_text_color = self.style_data.value_text_color_deactivated
        self._hover_overlay_color = self.style_data.hover_overlay_idle
        self._value_y_offset = 0.0
        self._scale_factor = 1

        self.ani_label_bg_color = SiExpAnimationRefactor(self, self.Property.LabelBackgroundColor)
        self.ani_label_bg_color.init(1/8, 1, self._label_bg_color, self._label_bg_color)

        self.ani_label_text_color = SiExpAnimationRefactor(self, self.Property.LabelTextColor)
        self.ani_label_text_color.init(1/8, 1, self._label_text_color, self._label_text_color)

        self.ani_value_bg_color = SiExpAnimationRefactor(self, self.Property.ValueBackgroundColor)
        self.ani_value_bg_color.init(1/8, 1, self._value_bg_color, self._value_bg_color)

        self.ani_value_text_color = SiExpAnimationRefactor(self, self.Property.ValueTextColor)
        self.ani_value_text_color.init(1/8, 1, self._value_text_color, self._value_text_color)

        self.ani_hover_overlay_color = SiExpAnimationRefactor(self, self.Property.HoverOverlayColor)
        self.ani_hover_overlay_color.init(1/8, 1, self._hover_overlay_color, self._hover_overlay_color)

        self.ani_value_y_offset = SiExpAnimationRefactor(self, self.Property.ValueYOffset)
        self.ani_value_y_offset.init(1/8, 0.001, self._value_y_offset, self._value_y_offset)

        self.ani_scale_factor = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.ani_scale_factor.init(1/8, 0.001, self._scale_factor, self._scale_factor)

        self._initScaleOnPressEventFilter()
        self._initToolTipRedirectEventFilter()
        self.toggled.connect(self._onToggled)

    def _initToolTipRedirectEventFilter(self) -> None:
        self._tooltip_manager = WidgetToolTipRedirectEventFilter()
        self.installEventFilter(self._tooltip_manager)

    def _initScaleOnPressEventFilter(self) -> None:
        self._scale_manager = ScaleOnPressEventFilter(self)
        self._scale_manager.setMinScaleFactor(0.95)
        self.installEventFilter(self._scale_manager)

    # region Properties

    @pyqtProperty(QColor)
    def labelBackgroundColor(self):
        return self._label_bg_color

    @labelBackgroundColor.setter
    def labelBackgroundColor(self, value):
        self._label_bg_color = value
        self.update()

    @pyqtProperty(QColor)
    def labelTextColor(self):
        return self._label_text_color

    @labelTextColor.setter
    def labelTextColor(self, value):
        self._label_text_color = value
        self.update()

    @pyqtProperty(QColor)
    def valueBackgroundColor(self):
        return self._value_bg_color

    @valueBackgroundColor.setter
    def valueBackgroundColor(self, value):
        self._value_bg_color = value
        self.update()

    @pyqtProperty(QColor)
    def valueTextColor(self):
        return self._value_text_color

    @valueTextColor.setter
    def valueTextColor(self, value):
        self._value_text_color = value
        self.update()

    @pyqtProperty(QColor)
    def hoverOverlayColor(self):
        return self._hover_overlay_color

    @hoverOverlayColor.setter
    def hoverOverlayColor(self, value):
        self._hover_overlay_color = value
        self.update()

    @pyqtProperty(float)
    def valueYOffset(self):
        return self._value_y_offset

    @valueYOffset.setter
    def valueYOffset(self, value):
        self._value_y_offset = value
        self.update()

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value):
        self._scale_factor = value
        self.update()

    # endregion

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.LabelBackgroundColor: self.ani_label_bg_color,
            self.Property.LabelTextColor: self.ani_label_text_color,
            self.Property.ValueBackgroundColor: self.ani_value_bg_color,
            self.Property.ValueTextColor: self.ani_value_text_color,
            self.Property.HoverOverlayColor: self.ani_hover_overlay_color,
            self.Property.ValueYOffset: self.ani_value_y_offset,
            self.Property.ScaleFactor: self.ani_scale_factor,
        }.get(prop_name)

    def sizeHint(self) -> QSize:
        label_font = self.font()
        value_font = self.font()

        label_metrics = QFontMetrics(label_font)
        value_metrics = QFontMetrics(value_font)

        label_text_width = label_metrics.horizontalAdvance(self.text())
        value_text_width = value_metrics.horizontalAdvance(str(self._value))

        total_width = (
            label_text_width + self._label_margin.left() + self._label_margin.right() +
            value_text_width + self._value_margin.left() + self._value_margin.right()
        )

        total_height = 36
        return QSize(total_width, total_height)

    def value(self):
        return self._value

    def setValue(self, v):
        self._value = v
        self.updateGeometry()

    def setThemeColor(self, color: QColor) -> None:
        h, s, v, _ = color.getHsv()
        self.style_data.value_background_color_activated = QColor.fromHsv(h, s, v)
        self.style_data.indicator_color = QColor.fromHsv(h, s, v - 71)
        self.update()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_hovered)
        self.ani_hover_overlay_color.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_idle)
        self.ani_hover_overlay_color.start()

    def _onToggled(self, checked: bool) -> None:
        self.ani_hover_overlay_color.setCurrentValue(self.style_data.hover_overlay_flash)
        self.ani_hover_overlay_color.start()

        if checked:
            self.ani_value_bg_color.setCurrentValue(self.style_data.value_background_color_flash)
            self.ani_value_bg_color.setEndValue(self.style_data.value_background_color_activated)
            self.ani_value_bg_color.start()

            self.ani_value_text_color.setEndValue(self.style_data.value_text_color_activated)
            self.ani_value_text_color.start()

        else:
            self.ani_value_bg_color.setEndValue(self.style_data.value_background_color_deactivated)
            self.ani_value_bg_color.start()

            self.ani_value_text_color.setEndValue(self.style_data.value_text_color_deactivated)
            self.ani_value_text_color.start()

    def _drawBodyBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._value_bg_color)
        painter.drawPath(path)

    def _drawLabelBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.label_background_color)
        painter.drawPath(path)

        if self.isChecked() is False:
            return

        color = QColor(self.style_data.value_background_color_activated)
        color.setAlpha(int(0.2 * 255))
        gradient = getGaussianLinearGradient(rect.topRight(), rect.topLeft(), color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(path)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:
        if self.isChecked():
            return

        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 1, 1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.indicator_color)
        painter.drawPath(path)

    def _drawLabelText(self, painter: QPainter, rect: QRect) -> None:
        option = QTextOption()
        option.setAlignment(Qt.AlignCenter)
        painter.setFont(self.font())
        painter.setPen(self.style_data.label_text_color)
        painter.drawText(QRectF(rect), self.text(), option)

    def _drawValueText(self, painter: QPainter, rect: QRect) -> None:
        option = QTextOption()
        option.setAlignment(Qt.AlignCenter)
        painter.setFont(self.font())
        painter.setPen(self._value_text_color)
        painter.drawText(QRectF(rect), str(self._value), option)

    def _drawHoverOverlayRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)
        painter.setCompositionMode(QPainter.CompositionMode_Plus)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._hover_overlay_color)
        painter.drawPath(path)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    def _drawBuffer(self, painter: QPainter, buffer: QPixmap, rect: QRect):
        a = self._scale_factor
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)
        painter.drawPixmap(rect, buffer)

    def paintEvent(self, e):
        full_rect = self.rect()

        label_font = self.font()
        value_font = self.font()

        label_metrics = QFontMetrics(label_font)
        value_metrics = QFontMetrics(value_font)

        label_text_width = label_metrics.horizontalAdvance(self.text())
        value_text_width = value_metrics.horizontalAdvance(str(self._value))

        label_rect_width = label_text_width + self._label_margin.left() + self._label_margin.right()
        value_rect_width = value_text_width + self._value_margin.left() + self._value_margin.right()

        body_rect = full_rect.marginsRemoved(QMargins(10, 0, 0, 0))
        label_rect = QRect(0, 0, label_rect_width, full_rect.height())
        value_rect = QRect(label_rect_width, 0, value_rect_width, full_rect.height())
        indicator_rect = value_rect.marginsRemoved(QMargins(0, full_rect.height() - 2, 0, 0)).marginsRemoved(self._indicator_margin)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        buffer = QPixmap(full_rect.size() * self.devicePixelRatioF())
        buffer.setDevicePixelRatio(self.devicePixelRatioF())
        buffer.fill(Qt.transparent)

        with createPainter(buffer) as painter:
            self._drawBodyBackgroundRect(painter, body_rect)
            self._drawLabelBackgroundRect(painter, label_rect)
            self._drawIndicatorRect(painter, indicator_rect)
            self._drawLabelText(painter, label_rect)
            self._drawValueText(painter, value_rect)
            self._drawHoverOverlayRect(painter, full_rect)

        with createPainter(self, renderHints) as painter:
            self._drawBuffer(painter, buffer, full_rect)


class OptionButtonStyleData:
    hover_overlay_idle = QColor("#00202020")
    hover_overlay_hovered = QColor("#202020")
    hover_overlay_flash = QColor("#7F7F7F")
    indicator_deactivated = QColor("#201D24")
    indicator_flash = QColor("#FFFFFF")
    indicator_activated = QColor("#D087DF")
    glyph_color = QColor("#201D24")
    text_color = QColor("#D1CBD4")
    body_background_color = QColor("#29252E")


class SiOptionButton(QAbstractButton):
    class Property:
        ScaleFactor = "scaleFactor"
        IndicatorColor = "indicatorColor"
        HoverOverlayColor = "hoverOverlayColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFont(SiFont.getFont(size=14))
        self.setCheckable(True)

        self.style_data = OptionButtonStyleData()

        self._text_margins = QMargins(16, 0, 16, 2)

        self._scale_factor = 1.0
        self._indicator_color = self.style_data.indicator_deactivated
        self._hover_overlay_color = self.style_data.hover_overlay_idle

        self.ani_scale_factor = SiExpAnimationRefactor(self, self.Property.ScaleFactor)
        self.ani_scale_factor.init(1/8, 0.001, self._scale_factor, self._scale_factor)

        self.ani_indicator_color = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.ani_indicator_color.init(1/16, 0.1, self._indicator_color, self._indicator_color)

        self.ani_hover_overlay_color = SiExpAnimationRefactor(self, self.Property.HoverOverlayColor)
        self.ani_hover_overlay_color.init(1/8, 1, self._hover_overlay_color, self._hover_overlay_color)

        self._initScaleOnPressEventFilter()
        self._initToolTipRedirectEventFilter()
        self.toggled.connect(self._onToggled)
        self.clicked.connect(self._onClicked)

    def _initToolTipRedirectEventFilter(self) -> None:
        self._tooltip_manager = WidgetToolTipRedirectEventFilter()
        self.installEventFilter(self._tooltip_manager)

    def _initScaleOnPressEventFilter(self) -> None:
        self._scale_manager = ScaleOnPressEventFilter(self)
        self._scale_manager.setMinScaleFactor(0.95)
        self.installEventFilter(self._scale_manager)

    # region animation property

    @pyqtProperty(float)
    def scaleFactor(self):
        return self._scale_factor

    @scaleFactor.setter
    def scaleFactor(self, value):
        self._scale_factor = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indicator_color

    @indicatorColor.setter
    def indicatorColor(self, value):
        self._indicator_color = value
        self.update()

    @pyqtProperty(QColor)
    def hoverOverlayColor(self):
        return self._hover_overlay_color

    @hoverOverlayColor.setter
    def hoverOverlayColor(self, value):
        self._hover_overlay_color = value
        self.update()

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.ScaleFactor: self.ani_scale_factor,
            self.Property.IndicatorColor: self.ani_indicator_color,
            self.Property.HoverOverlayColor: self.ani_hover_overlay_color,
        }.get(prop_name)

    # endregion

    def _onToggled(self, checked: bool) -> None:
        if checked:
            self.ani_indicator_color.setCurrentValue(self.style_data.indicator_flash)
            self.ani_indicator_color.setEndValue(self.style_data.indicator_activated)
            self.ani_indicator_color.start()

        else:
            self.ani_indicator_color.setCurrentValue(self.style_data.indicator_deactivated)
            self.ani_indicator_color.setEndValue(self.style_data.indicator_deactivated)
            self.ani_indicator_color.toProperty()

    def _onClicked(self, _) -> None:
        self.ani_hover_overlay_color.setCurrentValue(self.style_data.hover_overlay_flash)
        self.ani_hover_overlay_color.start()

    def _calcTextWidth(self) -> int:
        metrics = QFontMetrics(self.font())
        text_width = metrics.horizontalAdvance(self.text())
        return text_width

    def _calcIndicatorRect(self) -> QRect:
        return QRect(0, 0, 36, self.height())

    def _calcTextAreaRect(self) -> QRect:
        return QRect(36, 0, self.width() - 36, self.height())

    def sizeHint(self) -> QSize:
        width = self._calcTextWidth() + self._text_margins.left() + self._text_margins.right() + 36
        height = 36
        return QSize(width, height)

    def _getGlyphPath(self) -> QPainterPath:
        points = [QPointF(x, y) for x, y in [
            (9.76497, 3.20474), (10.0661, 3.48915), (9.79526, 4.26497),
            (5.54526, 8.76497), (5.40613, 8.91228), (5.01071, 8.99993),
            (4.8081, 9.00282), (4.46967, 8.78033), (2.21967, 6.53033),
            (1.92678, 6.23744), (2.21967, 5.46967), (2.51256, 5.17678),
            (3.28033, 5.46967), (4.98463, 7.17397), (8.70474, 3.23503),
            (8.98915, 2.9339), (9.76497, 3.20474)
        ]]

        quad_control_end_pairs = [
            (1, 2), (2, 3), (4, 5), (6, 7), (7, 8),
            (9, 10), (11, 12), (12, 13), (13, 14), (15, 16)
        ]

        path = QPainterPath()
        path.moveTo(points[0])
        for control_idx, end_idx in quad_control_end_pairs:
            path.quadTo(points[control_idx], points[end_idx])
        path.closeSubpath()

        transform = QTransform()
        transform.scale(1.75, 1.75)

        return transform.map(path)

    def _drawBodyRect(self, painter: QPainter, rect: QRect) -> None:
        if self.autoExclusive():
            path = getRoundedRectPathArc(QRectF(rect), 18, 10, 10, 18)
        else:
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.body_background_color)
        painter.drawPath(path)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:
        if self.autoExclusive():
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 18, 18)
        else:
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._indicator_color)
        painter.drawPath(path)

    def _drawGlyph(self, painter: QPainter, rect: QRect) -> None:
        glyph_path = self._getGlyphPath()
        glyph_path.translate(rect.center() - QPointF(9.5, 9.25))
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.glyph_color)
        painter.drawPath(glyph_path)

    def _drawText(self, painter: QPainter, rect: QRect) -> None:
        shrunk_rect = rect.marginsRemoved(self._text_margins)
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.ElideRight, shrunk_rect.width())

        painter.setPen(self.style_data.text_color)
        painter.setBrush(Qt.NoBrush)
        painter.setFont(self.font())
        painter.drawText(shrunk_rect, Qt.AlignVCenter | Qt.AlignLeft, elided)

    def _drawHoverOverlayRect(self, painter: QPainter, rect: QRect) -> None:
        if self.autoExclusive():
            path = getRoundedRectPathArc(QRectF(rect), 18, 10, 10, 18)
        else:
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)

        painter.setCompositionMode(QPainter.CompositionMode_Plus)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._hover_overlay_color)
        painter.drawPath(path)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    def _drawBuffer(self, painter: QPainter, buffer: QPixmap, rect: QRect):
        a = self._scale_factor
        painter.translate(QPointF(rect.width() * (1 - a) / 2, rect.height() * (1 - a) / 2))
        painter.scale(a, a)
        painter.drawPixmap(rect, buffer)

    def paintEvent(self, e):
        full_rect = self.rect()
        body_rect = self.rect()
        indicator_rect = self._calcIndicatorRect()
        text_area_rect = self._calcTextAreaRect()

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        buffer = QPixmap(full_rect.size() * self.devicePixelRatioF())
        buffer.setDevicePixelRatio(self.devicePixelRatioF())
        buffer.fill(Qt.transparent)

        with createPainter(buffer) as painter:
            self._drawBodyRect(painter, body_rect)
            self._drawIndicatorRect(painter, indicator_rect)
            self._drawGlyph(painter, indicator_rect)
            self._drawText(painter, text_area_rect)
            self._drawHoverOverlayRect(painter, body_rect)

        with createPainter(self, renderHints) as painter:
            self._drawBuffer(painter, buffer, full_rect)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_hovered)
        self.ani_hover_overlay_color.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.ani_hover_overlay_color.setEndValue(self.style_data.hover_overlay_idle)
        self.ani_hover_overlay_color.start()


class SiCheckBox(SiOptionButton):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.setAutoExclusive(False)


class SiRadioButton(SiOptionButton):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.setAutoExclusive(True)
