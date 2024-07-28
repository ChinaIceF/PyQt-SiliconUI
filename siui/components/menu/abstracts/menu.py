
from PyQt5.Qt import QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.container import SiDenseHContainer, SiDenseVContainer
from siui.components.widgets.label import SiLabel, SiSvgLabel
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si


class ABCSiMenuOption(SiDenseHContainer):
    def __init__(self,
                 parent_menu,
                 child_menu,
                 text: str,
                 icon: str = None):
        super().__init__(parent_menu)  # parent will be overwritten when added to container

        self.child_menu = child_menu
        self.parent_menu = parent_menu
        self.is_selected = False

        self.setSpacing(0)
        self.setFixedHeight(32)
        self.setAlignCenter(True)

        self.indicator = SiLabel(self)
        self.indicator.setFixedSize(4, 20)
        self.indicator.setFixedStyleSheet("border-radius: 2px")
        self.indicator.setVisible(False)

        self.icon = SiSvgLabel(self)
        self.icon.resize(48, 32)
        self.icon.setSvgSize(16, 16)
        if icon is not None:
            self.icon.load(icon)

        self.text_label = SiLabel(self)
        self.text_label.setFixedHeight(32)
        self.text_label.setText(text)
        self.text_label.setAlignment(Qt.AlignVCenter)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

        self.addWidget(self.indicator)
        self.addPlaceholder(4)
        self.addWidget(self.icon)
        self.addPlaceholder(4)
        self.addWidget(self.text_label)

    def parentMenu(self):
        """
        Get the parent menu of this option
        :return: parent menu
        """
        return self.parent_menu

    def setSelected(self,
                    state: bool,
                    has_signal: bool = True):
        """
        Set the select state of this option
        """
        self.is_selected = state
        self.indicator.setVisible(state)
        if (has_signal is True) and (state is True):
            self.parentMenu().indexChanged.emit(self.parentMenu().options().index(self))

        if state is True:
            for option in self.parentMenu().options():
                if option != self:
                    option.setSelected(False)

    def isSelected(self):
        """
        Get the select state of this option
        :return: select state
        """
        return self.is_selected

    def setShowIcon(self, state):
        if state:
            self.icon.resize(32, 32)
        else:
            self.icon.resize(0, 32)
        self.adjustWidgetsGeometry()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.indicator.setColor(self.colorGroup().fromToken(SiColor.THEME))
        self.text_label.setStyleSheet(f"color: {self.colorGroup().fromToken(SiColor.TEXT_B)}")


class ABCSiMenu(SiWidget):
    indexChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.options_ = []
        self.parent_menu = None
        self.margin = 32
        self.padding = 4

        self.setMoveAnchor(self.margin, self.margin)
        self.setMinimumSize(self.margin*2, self.margin*2)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.body_panel = SiLabel(self)
        self.body_panel.setObjectName("menu_body_panel")

        self.flash_layer = SiLabel(self)
        self.flash_layer.setFixedStyleSheet("border-radius: 6px")
        self.flash_layer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.flash_layer.getAnimationGroup().fromToken("color").setFactor(1/16)

        self.body_ = SiDenseVContainer(self.body_panel)
        self.body_.setAdjustWidgetsSize(True)
        self.body_.setSpacing(2)
        self.body_.resize(0, 0)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(32)
        self.body_panel.setGraphicsEffect(shadow)

        SiGlobal.siui.windows[str(self)] = self

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.body_panel.setStyleSheet(
            f"""#menu_body_panel {{
                    background-color: {self.colorGroup().fromToken(SiColor.MENU_BG)};
                    border: 1px solid {SiColor.mix(self.colorGroup().fromToken(SiColor.MENU_BG), self.colorGroup().fromToken(SiColor.TEXT_E), 0.9)};
                    border-radius: 6px
            }}"""
        )

    def setShowIcon(self, state: bool):
        """
        set whether options show their icon
        """
        for option in self.options_:
            option.setShowIcon(state)

    def setIndex(self, index):
        """
        Set current index of this menu
        """
        self.options()[index].setSelected(True)

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
        """
        get the body of this menu
        """
        return self.body_

    def options(self):
        """
        get the options of this menu
        """
        return self.options_

    def unfold(self, x, y):
        """
        unfold the menu
        """
        _, body_preferred_height = self.body_.getPreferredSize()
        self.move(x, y)
        self.show()

        target_height = body_preferred_height + self.margin * 2 + self.padding * 2
        self.resize(self.width(), int(target_height * 0.6))
        self.resizeTo(self.width(), target_height)

        self.flash_layer.setColor(SiColor.trans(self.colorGroup().fromToken(SiColor.BUTTON_FLASH), 1))
        self.flash_layer.setColorTo(SiColor.trans(self.colorGroup().fromToken(SiColor.BUTTON_FLASH), 0))

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.resize(self.width(), self.margin * 2)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.body_panel.setGeometry(self.margin,
                                    self.margin,
                                    size.width() - self.margin * 2,
                                    size.height() - self.margin * 2)
        self.flash_layer.setGeometry(self.margin,
                                     self.margin,
                                     size.width() - self.margin * 2,
                                     size.height() - self.margin * 2)
        self.body_.setGeometry(self.padding,
                               self.padding,
                               size.width() - self.margin * 2 - self.padding * 2,
                               size.height() - self.margin * 2 - self.padding * 2)
