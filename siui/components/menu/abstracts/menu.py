from PyQt5.Qt import QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.container import SiDenseVContainer
from siui.components.widgets.label import SiLabel
from siui.core import SiColor, SiGlobal


class ABCSiMenu(SiWidget):
    indexChanged = pyqtSignal(int)
    valueChanged = pyqtSignal(object)
    unfoldSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.options_ = []
        self.waken_option = None
        self.is_selection_menu = True
        self.current_index = None
        self.current_value = None
        self.animation_manager = None
        self.margin = 32
        self.padding = 4

        self.setMoveAnchor(self.margin + self.padding, self.margin + self.padding)
        self.setMinimumSize(self.margin*2, self.margin*2)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.frame_debugging = SiLabel(self)
        self.frame_debugging.setStyleSheet("background-color: transparent")

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

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(32)
        self.body_frame.setGraphicsEffect(shadow)

        SiGlobal.siui.windows[str(self)] = self

        self.indexChanged.connect(self.setAnchorByIndex)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.body_panel.setStyleSheet(
            f"""#menu_body_panel {{
                    background-color: {self.getColor(SiColor.MENU_BG)};
                    border: 1px solid {SiColor.mix(self.getColor(SiColor.MENU_BG), self.getColor(SiColor.TEXT_E), 0.9)};
                    border-radius: 6px
            }}"""
        )

    def setAnchorByIndex(self, index):
        """ set an option's position as the anchor of the menu by index """
        option = self.options_[index]
        shift = self.margin + self.padding
        self.setMoveAnchor(option.pos().x() + shift, option.pos().y() + shift)

    def setWakenOption(self, option_from_parent_menu):
        """ set the waken option of this menu """
        self.waken_option = option_from_parent_menu

    def wakenOption(self):
        """ get the waken option of this menu """
        return self.waken_option

    def setShowIcon(self, state: bool):
        """ set whether options show their icon """
        for option in self.options_:
            option.setShowIcon(state)

    def setSelectionMenu(self, state):
        """
        set this menu as a selection menu or not.

        A selection menu allows its options be selected, while a non-selection menu prevents its options be selected.
        """
        self.is_selection_menu = state
        for option in self.options_:
            option.setSelectable(state)

    def setIndex(self, index):
        """ Set current index of this menu """
        self.options()[index].setSelected(True)
        self.current_index = index
        self.current_value = self.options()[index].value()

    def index(self):
        return self.current_index

    def value(self):
        return self.current_value

    def addOption(self,
                  text: str,
                  icon: str = None,
                  child_menu=None):
        """
        add an option to this menu
        :param text: text of the option added
        :param icon: svg data or path for the icon of the option added
        :param child_menu: assign child menu if this option has one
        :return:
        """
        raise NotImplementedError()

    def body(self):
        """ get the body of this menu """
        return self.body_

    def options(self):
        """ get the options of this menu """
        return self.options_

    def setAnimationManager(self, token):
        self.animation_manager = token.value

    def animationManager(self):
        return self.animation_manager

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.closeSignal.emit()
        self.resize(self.width(), self.margin * 2)

    def recursiveClose(self):
        """ close menu recursively, this will close the menus' parent menus. """
        if self.wakenOption() is not None:
            self.wakenOption().parentMenu().recursiveClose()
        self.close()

    def setContentFixedWidth(self, w):
        self.setFixedWidth(w + self.padding*2 + self.margin*2)

    def unfold(self, x, y):
        """ unfold the menu """
        self.animationManager().on_parent_unfolded(self, x, y)

    def resizeEvent(self, event):
        self.animationManager().on_parent_resized(self, event)
        super().resizeEvent(event)