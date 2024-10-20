from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from siui.components import SiWidget, SiLabel, SiDenseVContainer
from siui.components.menu.abstracts import ABCSiMenu, AnimationManager
from siui.components.menu.option import SiMenuOption
from siui.core import SiQuickEffect, SiColor, SiGlobal


class SiMenu(ABCSiMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAnimationManager(AnimationManager.PULL_DOWN)

    def addOption(self,
                  text: str,
                  value=None,
                  icon=None,
                  child_menu=None):
        new_option = SiMenuOption(self, child_menu, text, value=value, icon=icon)
        new_option.setSelectable(self.is_selection_menu)
        new_option.setFixedHeight(32)

        self.options_.append(new_option)
        self.body().addWidget(new_option)
        self.body().arrangeWidget()


class SiInteractionMenu(SiWidget):
    indexChanged = pyqtSignal(int)
    valueChanged = pyqtSignal(object)
    unfoldSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 在窗口列表里注册菜单，用于重载样式表
        SiGlobal.siui.windows[str(self)] = self

        self.animation_manager = None
        self.margin = 32
        self.padding = 4

        self.setAnimationManager(AnimationManager.PULL_DOWN)

        self.setMoveAnchor(self.margin + self.padding, self.margin + self.padding)
        self.setMinimumSize(self.margin*2, self.margin*2)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.body_frame = SiWidget(self)

        self.body_panel = SiLabel(self.body_frame)
        self.body_panel.setObjectName("menu_body_panel")

        self.flash_layer = SiLabel(self)
        self.flash_layer.setFixedStyleSheet("border-radius: 6px")
        self.flash_layer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.flash_layer.animationGroup().fromToken("color").setFactor(1/16)

        self.body_ = SiDenseVContainer(self.body_panel)
        self.body_.setAdjustWidgetsSize(True)
        self.body_.setSpacing(2)
        self.body_.resize(0, 0)

        SiQuickEffect.applyDropShadowOn(self.body_frame, (0, 0, 0, 80), (0, 0), 32)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.body_panel.setStyleSheet(
            f"""#menu_body_panel {{
                    background-color: {self.getColor(SiColor.MENU_BG)};
                    border: 1px solid {SiColor.mix(self.getColor(SiColor.MENU_BG), self.getColor(SiColor.TEXT_E), 0.9)};
                    border-radius: 6px
            }}"""
        )

    def setAnimationManager(self, token):
        self.animation_manager = token.value

    def animationManager(self):
        return self.animation_manager

    def unfold(self, x, y):
        """ unfold the menu """
        self.animationManager().on_parent_unfolded(self, x, y)
        SiGlobal.siui.windows["TOOL_TIP"].raise_()

    def setContentFixedWidth(self, w):
        self.setFixedWidth(w + self.padding*2 + self.margin*2)

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.closeSignal.emit()
        self.resize(self.width(), self.margin * 2)

    def resizeEvent(self, event):
        self.animationManager().on_parent_resized(self, event)
        super().resizeEvent(event)

    def sizeHint(self):
        w = self.body_.sizeHint().width() + 2 * self.padding + 2 * self.margin
        h = self.body_.sizeHint().height() + 2 * self.padding + 2 * self.margin
        return QSize(w, h)

