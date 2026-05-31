from __future__ import annotations

import weakref
from enum import Enum

from PyQt6 import sip
from PyQt6.QtCore import QMargins, QPoint, QRect, QRectF, QSize, Qt, QTimer, pyqtProperty
from PyQt6.QtGui import QColor, QCursor, QPainter, QPainterPath
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLayout, QWidget

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core import GlobalFont, Si, SiGlobal, SiQuickEffect, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.theme import GlobalStyleData, SiThemeManager, StyleData
from siui.gui import SiFont


class ToolTipWindow(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_shown = False
        self.completely_hid = False
        """ 是否已经完全隐藏（透明度是不是0） """
        self.now_inside_of = None
        """ 在哪个控件内部（最近一次被谁触发过显示事件） """
        self.margin = 8
        """ 周围给阴影预留的间隔空间 """
        self.shadow_size = 8
        """ 阴影大小 """

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        SiQuickEffect.applyDropShadowOn(self, (0, 0, 0, 128), blur_radius=int(self.shadow_size*1.5))

        self._initWidget()
        self._initStyle()
        self._initLayout()
        self._initAnimation()

        self.setText("", flash=False)  # 通过输入空文本初始化大小

    def _initWidget(self):
        self.bg_label = SiLabel(self)
        """背景颜色，可以用于呈现不同类型的信息"""

        self.text_container = SiLabel(self)
        """文字标签的父对象，防止文字超出界限"""

        self.text_label = SiLabel(self.text_container)
        """文字标签，显示工具提示内容"""

        self.highlight_mask = SiLabel(self)
        """高光遮罩，当信息刷新时会闪烁一下"""

    def _initStyle(self):
        self.bg_label.setFixedStyleSheet("border-radius: 6px")
        self.text_label.setFixedStyleSheet("padding: 8px")
        self.text_label.setSiliconWidgetFlag(Si.InstantResize)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.text_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.highlight_mask.setFixedStyleSheet("border-radius: 6px")
        self.highlight_mask.setColor("#00FFFFFF")

    def _initLayout(self):
        self.bg_label.move(self.margin, self.margin)
        self.text_container.move(self.margin, self.margin)
        self.highlight_mask.move(self.margin, self.margin)

    def _initAnimation(self):
        self.tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self.tracker_timer.setInterval(int(1000/60))
        self.tracker_timer.timeout.connect(self._refresh_position)
        self.tracker_timer.start()

        # 当透明度动画结束时处理隐藏与否
        self.animationGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)

    def reloadStyleSheet(self):
        self.bg_label.setColor(SiGlobal.siui.colors["TOOLTIP_BG"])
        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def show_(self):
        self.is_shown = True
        self.setOpacityTo(1.0)

    def hide_(self):
        self.is_shown = False
        self.setOpacityTo(0)

    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self.completely_hid = True
            self.resize(2 * self.margin, 36 + 2 * self.margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self.text_label.setText("")   # 清空文本内容
        else:
            self.completely_hid = False

    def setNowInsideOf(self, widget):
        """
        设置当前位于哪个控件内部。对于 siui 的控件，这将会在设置工具提示显示时被调用并传入调用者，在隐藏时被调用并传入 None
        :param widget: 在哪个控件的内部（被谁触发了显示）
        :return:
        """
        self.now_inside_of = widget

    def nowInsideOf(self):
        """
        返回最后一次被调用显示时的发出者
        :return: 控件或None
        """
        return self.now_inside_of

    def setText(self, text, flash=True):
        """
        设置工具提示的内容，支持富文本
        :param text: 内容，将被转化为字符串
        :param flash: 是否闪烁高光层
        :return:
        """
        text_changed = self.text_label.text() != text
        self.text_label.setText(str(text))
        self._refresh_size()
        if flash and text_changed:
            self.flash()

    def _refresh_size(self):
        """ 用于设置大小动画结束值并启动动画 """
        w = self.text_label.width()
        h = self.text_label.height()
        self.resizeTo(w + 2 * self.margin, h + 2 * self.margin)  # 设为文字标签的大小加上阴影间距

    def flash(self):
        """ 激活高光层动画，使高光层闪烁 """
        self.highlight_mask.setColor("#7FFFFFFF")
        self.highlight_mask.setColorTo("#00FFFFFF")

    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x(), pos.y()
        self.moveTo(x + 4, y - self.height())    # 动画跟踪，效果更佳，有了锚点直接输入鼠标坐标即可

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width() - 2 * self.margin, size.height() - 2 * self.margin

        # 重设内部控件大小
        self.bg_label.resize(w, h)
        self.text_container.resize(w, h)
        self.highlight_mask.resize(w, h)

        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        # self.text_label.move(0, h - self.text_label.height()) 2024.9.23 - 存在快速滑动鼠标时文字错位的情况
        self.text_label.move(0, h - self.height() + 16)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()


class ToolTipStyleData(StyleData):
    class Token(Enum):
        pass


ToolTipStyleData.registerData(
    themeName=SiThemeManager.Preset.Light,
    mapping={}
)

ToolTipStyleData.registerData(
    themeName=SiThemeManager.Preset.Dark,
    mapping={}
)


class ToolTipPanel(QWidget):
    class Property:
        FlashOverlayAlpha = "flashOverlayAlpha"

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # -- declaration ------
        self._sd: StyleData
        self._flashAlphaAni: SiExpAnimationRefactor
        self._content: QWidget | None
        self._contentMargins: QMargins
        self._flashOverlayAlpha: int

        # -- init ------
        self._sd = ToolTipStyleData(self, self._onStyleUpdated)
        self._content = None
        self._contentMargins = QMargins(8, 8, 8, 8)
        self._flashOverlayAlpha = 0

        self._initAnimation()
        self._initLayout()

    def _initAnimation(self) -> None:
        self._flashAlphaAni = SiExpAnimationRefactor(self, self.Property.FlashOverlayAlpha)
        self._flashAlphaAni.init(1 / 8, 0.01, 0, 0)

    def _initLayout(self) -> None:
        layout = QHBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        layout.setContentsMargins(self._contentMargins)
        self.setLayout(layout)

    def _onStyleUpdated(self) -> None:
        self.update()

    @pyqtProperty(int)
    def flashOverlayAlpha(self) -> int:
        return self._flashOverlayAlpha

    @flashOverlayAlpha.setter
    def flashOverlayAlpha(self, value: int) -> None:
        self._flashOverlayAlpha = value
        self.update()

    def flash(self) -> None:
        self._flashAlphaAni.setCurrentValue(99)
        self._flashAlphaAni.start()

    def setContent(self, widget: QWidget) -> None:
        layout = self.layout()
        if self._content:
            layout.removeWidget(self._content)
            self._content.deleteLater()

        layout.addWidget(widget)
        self._content = widget

    @property
    def contentMargins(self) -> QMargins:
        return self._contentMargins

    def _drawBackgroundRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)

        bgColor: QColor = self._sd.fromToken(GlobalStyleData.Token.SurfaceLevel3)
        painter.setBrush(bgColor)
        painter.drawPath(path)

    def _drawFlashOverlay(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)

        flashColor: QColor = self._sd.fromToken(GlobalStyleData.Token.Flash)
        flashColor.setAlpha(self._flashOverlayAlpha)
        painter.setBrush(flashColor)
        painter.drawPath(path)

    def paintEvent(self, event) -> None:
        bgRect = self.rect().toRectF()

        with createPainter(self) as painter:
            self._drawBackgroundRect(painter, bgRect)
            self._drawFlashOverlay(painter, bgRect)


class ToolTipContainer(QWidget):
    _instance = None

    class Property:
        Geometry = "geometry"
        Opacity = "opacity"

    @classmethod
    def getInstance(cls) -> ToolTipContainer:
        if cls._instance is None or sip.isdeleted(cls._instance):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()

        # -- declaration ------
        self._currentTarget: weakref.ReferenceType | None
        self._geometryAni: SiExpAnimationRefactor
        self._opacityAni: SiExpAnimationRefactor
        self._mouseTimer: QTimer
        self._panel: ToolTipPanel
        self._shadowMargins: QMargins
        self._desiredSize: QSize
        self._emptySize: QSize

        # -- init ------
        self._currentTarget = None
        self._shadowMargins = QMargins(16, 16, 16, 16)
        self._desiredSize = QSize(0, 19)
        self._emptySize = QSize(0, 19)

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0)

        self._initLayout()
        self._initAnimation()
        self._initTimer()

    def _initLayout(self) -> None:
        layout = QHBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        layout.setContentsMargins(self._shadowMargins)

        self._panel = ToolTipPanel(self)
        layout.addWidget(self._panel)
        self.setLayout(layout)

        SiQuickEffect.applyDropShadowOn(
            self._panel, (0, 0, 0, 128), blur_radius=self._shadowMargins.top()
        )

    def _initAnimation(self) -> None:
        self._geometryAni = SiExpAnimationRefactor(self, self.Property.Geometry)
        self._opacityAni = SiExpAnimationRefactor(self, self.Property.Opacity)

        g = self._getAdjustedGeometry(self._emptySize)
        self._geometryAni.init(1 / 4, 0.1, g, g)
        self._opacityAni.init(1 / 4, 0.01, 0, 0)

    def _initTimer(self) -> None:
        self._mouseTimer = QTimer()
        self._mouseTimer.setInterval(1000 // 60)
        self._mouseTimer.timeout.connect(self._onMouseTimerTimeout)

    def _getAdjustedGeometry(self, contentSize: QSize) -> QRect:
        panelMargins = self._panel.contentMargins
        totalMargins = self._shadowMargins + panelMargins

        mouseOffset = QPoint(8, 0) - QPoint(0, contentSize.height() + panelMargins.bottom())
        targetPos = QCursor.pos() + mouseOffset

        g = QRect(targetPos, contentSize)
        g = g.marginsAdded(totalMargins)
        return g

    def _onMouseTimerTimeout(self) -> None:
        g = self._getAdjustedGeometry(self._desiredSize)
        self._geometryAni.setEndValue(g)
        self._geometryAni.start()

    def _onAboutToAppear(self) -> None:
        g = self._getAdjustedGeometry(self._emptySize)
        self._geometryAni.setCurrentValue(g)
        self.setGeometry(g)

    def _onOpacityEqualsZero(self) -> None:
        g = self._getAdjustedGeometry(self._emptySize)
        self._mouseTimer.stop()
        self._geometryAni.stop()
        self._geometryAni.setCurrentValue(g)
        self.setGeometry(g)
        self.hide()

    @pyqtProperty(float)
    def opacity(self) -> float:
        return self.windowOpacity()

    @opacity.setter
    def opacity(self, value: float) -> None:
        if value == 0:
            self._onOpacityEqualsZero()
        self.setWindowOpacity(value)

    def isTargetAt(self, widget: QWidget) -> bool:
        if self._currentTarget is None:
            return False
        target = self._currentTarget()
        if target is None:
            return False
        if sip.isdeleted(target):
            return False
        return target is widget

    def appear(self, target: QWidget) -> None:
        self._currentTarget = weakref.ref(target)

        if self.windowOpacity() == 0:
            self._onAboutToAppear()

        self._opacityAni.setEndValue(1.0)
        self._opacityAni.start()

        self._mouseTimer.start()
        self.show()

    def disappear(self) -> None:
        self._currentTarget = None
        self._opacityAni.setEndValue(0.0)
        self._opacityAni.start()

    def flash(self) -> None:
        self._panel.flash()

    def setContent(self, widget: QWidget) -> None:
        self._panel.setContent(widget)
        self._desiredSize = widget.sizeHint()

    def setText(self, text: str) -> None:
        label = QLabel(text, self._panel)
        label.setFont(SiFont.getFont(size=14))
        self.setContent(label)

    def tryUpdateText(self, target: QWidget, text: str) -> None:
        if self.isTargetAt(target):
            self.setText(text)
