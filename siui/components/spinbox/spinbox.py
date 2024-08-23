from PyQt5.QtCore import Qt

from ...core.color import SiColor
from .. import SiLabel, SiSimpleButton, SiWidget
from .abstract.spinbox import ABCSiSpinBox
from ...core.globals import SiGlobal


class SiSpinBoxButton(SiSimpleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.direction_ = Qt.LeftButton

        self.indicator_frame = SiWidget(self)

        self.indicator_label = SiLabel(self.indicator_frame)
        self.indicator_label.lower()

        # 禁用悬停颜色变化
        self.colorGroup().assign(SiColor.BUTTON_HOVER, "#00FFFFFF")

        self.indicator_label.setOpacity(0)

    def setThemeColor(self, color_code):
        self.colorGroup().assign(SiColor.THEME, color_code)

    def setDirection(self, direction):
        self.direction_ = direction

    def direction(self):
        return self.direction_

    def _get_border_radius_stylesheet(self):
        if self.direction_ == Qt.LeftButton:
            return "border-top-left-radius: 4px; border-bottom-left-radius: 4px;"
        elif self.direction_ == Qt.RightButton:
            return "border-top-right-radius: 4px; border-bottom-right-radius: 4px;"

    def _get_indicator_stylesheet(self):
        theme_color = self.colorGroup().fromToken(SiColor.THEME)
        stylesheet = (f"border-bottom: 3px solid {theme_color};"
                      f"background-color: {SiColor.trans(theme_color, 0.6)};"
                      f"{self._get_border_radius_stylesheet()}")
        return stylesheet

    def _get_color_label_stylesheet(self):
        panel_color = self.colorGroup().fromToken(SiColor.INTERFACE_BG_D)
        shadow_color = self.colorGroup().fromToken(SiColor.BUTTON_SHADOW)
        stylesheet = (f"border-bottom: 3px solid {shadow_color};"
                      f"background-color: {panel_color};"
                      f"{self._get_border_radius_stylesheet()}")
        return stylesheet


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.hoverLabel().setFixedStyleSheet(self._get_border_radius_stylesheet())
        self.colorLabel().setFixedStyleSheet(self._get_color_label_stylesheet())
        self.indicator_label.setStyleSheet(self._get_indicator_stylesheet())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator_frame.resize(event.size())
        self.indicator_label.resize(event.size())

    def enterEvent(self, event):
        super().enterEvent(event)
        self.indicator_label.setOpacityTo(1)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.indicator_label.setOpacityTo(0)

class SiSpinBox(ABCSiSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_width = 32

        self.button_up = SiSpinBoxButton(self)
        self.button_up.setDirection(Qt.RightButton)
        self.button_up.setIdleColor(self.colorGroup().fromToken(SiColor.INTERFACE_BG_D))
        self.button_up.setThemeColor(self.colorGroup().fromToken(SiColor.SIDE_MSG_THEME_SUCCESS))

        self.button_down = SiSpinBoxButton(self)
        self.button_down.setDirection(Qt.LeftButton)
        self.button_down.setIdleColor(self.colorGroup().fromToken(SiColor.INTERFACE_BG_D))
        self.button_down.setThemeColor(self.colorGroup().fromToken(SiColor.SIDE_MSG_THEME_ERROR))

        self.body_ = SiLabel(self)
        self.body_.setAlignment(Qt.AlignCenter)
        self.body_.setText("123")

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        SiGlobal.siui.reloadStyleSheetRecursively(self.button_up)
        SiGlobal.siui.reloadStyleSheetRecursively(self.button_down)
        self.body_.setStyleSheet(
            f"color: {self.colorGroup().fromToken(SiColor.TEXT_B)};"
            f"background-color: {self.colorGroup().fromToken(SiColor.INTERFACE_BG_E)};"
            f"border-bottom: 3px solid {self.colorGroup().fromToken(SiColor.BUTTON_SHADOW)}"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.button_down.setGeometry(0, 0, self.button_width, event.size().height())
        self.button_up.setGeometry(event.size().width() - self.button_width, 0, self.button_width, event.size().height())
        self.body_.setGeometry(self.button_width, 0, event.size().width() - 2 * self.button_width, event.size().height())
