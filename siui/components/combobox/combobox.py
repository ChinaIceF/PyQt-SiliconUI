
from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from siui.components.menu.abstracts.ani_manager import AnimationManager
from siui.components.menu.menu import SiMenu
from siui.components.widgets import SiDenseHContainer
from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.button import SiSimpleButton
from siui.components.widgets.label import SiLabel, SiSvgLabel
from siui.core import GlobalFont, Si, SiColor
from siui.gui.font import SiFont


class ABCSiComboBox(SiWidget):
    indexChanged = pyqtSignal(int)
    valueChanged = pyqtSignal(object)
    menuUnfolded = pyqtSignal()
    menuClosed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attachment_ = None
        self.menu_ = None

        # panel label provides background
        self.panel_label = SiLabel(self)
        self.panel_label.setFixedStyleSheet("border-radius: 4px")

        self.container_ = SiDenseHContainer(self)
        self.container_.setAlignment(Qt.AlignCenter)
        self.container_.setSpacing(0)

        self.unfold_menu_indicator = SiSvgLabel(self)
        self.unfold_menu_indicator.setSvgSize(16, 16)
        self.unfold_menu_indicator.resize(32, 32)

        self.container_.addWidget(self.unfold_menu_indicator, side="right")

    def setMenu(self, menu: SiMenu):
        """ Set the menu of this combo box"""
        self.menu_ = menu

    def menu(self) -> SiMenu:
        """ Get the menu of this combo box """
        return self.menu_

    def setAttachment(self, widget):
        """ Get the attachment of this combo box """
        widget.setParent(self.container_)
        self.attachment_ = widget
        self.container_.addWidget(self.attachment_, side="left")

    def attachment(self):
        """ Get the attachment of this combo box """
        return self.attachment_

    def container(self):
        """ Get the container of this combobox """
        return self.container_

    def _on_unfold_button_clicked(self):
        pos = self.mapToGlobal(QPoint(0, 0))
        self.menu_.unfold(pos.x(), pos.y())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.panel_label.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_B)};"
            f"border: 1px solid {self.getColor(SiColor.INTERFACE_BG_D)};"
        )

        svg_data = ('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Outline" '
                    'viewBox="0 0 24 24" width="512" height="512"><path d="M18.71,8.21a1,1,0,0,0-1.42,0l-4.58,4.58a1,'
                    '1,0,0,1-1.42,0L6.71,8.21a1,1,0,0,0-1.42,0,1,1,0,0,0,0,1.41l4.59,4.59a3,3,0,0,0,4.24,'
                    '0l4.59-4.59A1,1,0,0,0,18.71,8.21Z"'
                    f' fill="{self.getColor(SiColor.SVG_NORMAL)}" /></svg>')
        self.unfold_menu_indicator.load(svg_data.encode())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.panel_label.resize(event.size())
        self.container_.resize(event.size())
        self.menu_.setContentFixedWidth(event.size().width())


class SiComboBox(ABCSiComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMenu(SiMenu())
        self.menu().setSelectionMenu(True)
        self.menu().setAnimationManager(AnimationManager.EXPAND)

        self.value_label = SiLabel(self)
        self.value_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.value_label.setAlignment(Qt.AlignVCenter)
        self.value_label.setFixedHeight(32)
        self.value_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.value_label.setFixedStyleSheet("padding-left: 8px; padding-right: 8px")
        self.setAttachment(self.value_label)

        self.unfold_menu_button = SiSimpleButton(self)
        self.unfold_menu_button.setBorderRadius(4)
        self.unfold_menu_button.clicked.connect(self._on_unfold_button_clicked)
        self.unfold_menu_button.setFlashOnClicked(False)
        self.unfold_menu_button.colorGroup().setReference(self.colorGroup())
        self.unfold_menu_button.flashLabel().setOpacity(0.6)
        self.unfold_menu_button.flashLabel().animationGroup().fromToken("color").setFactor(1 / 16)  # slow down ani

        self.menu().indexChanged.connect(lambda x: self.value_label.setText(self.menu().options()[x].text()))
        self.menu().indexChanged.connect(self.indexChanged)
        self.menu().valueChanged.connect(lambda _: self.unfold_menu_button.flash())
        self.menu().valueChanged.connect(self.valueChanged)

    def addOption(self,
                  text: str,
                  value=None,
                  icon=None,
                  child_menu=None):
        self.menu().addOption(text, icon=icon, value=value, child_menu=child_menu)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.value_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.unfold_menu_button.resize(event.size())
