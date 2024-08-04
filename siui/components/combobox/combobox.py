
from PyQt5.QtCore import Qt

from siui.components.combobox.abstracts import ABCSiComboBox
from siui.components.menu.abstracts.ani_manager import AnimationManager
from siui.components.menu.menu import SiMenu
from siui.components.widgets.button import SiSimpleButton
from siui.components.widgets.label import SiLabel
from siui.core.color import SiColor
from siui.core.silicon import Si
from siui.gui.font import GlobalFont, SiFont


class SiComboBox(ABCSiComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMenu(SiMenu())
        self.menu().setSelectionMenu(True)
        self.menu().setAnimationManager(AnimationManager.EXPAND)

        self.value_label = SiLabel(self)
        self.value_label.setFont(SiFont.fromToken(GlobalFont.S_NORMAL))
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
        self.value_label.setStyleSheet(f"color: {self.colorGroup().fromToken(SiColor.TEXT_B)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.unfold_menu_button.resize(event.size())
