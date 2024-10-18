from PyQt5.QtCore import QPoint

from siui.components import SiSimpleButton, SiWidget, SiLabel
from siui.components.menu.menu import SiInteractionMenu
from siui.core import SiGlobal


class SiCalenderView(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = SiSimpleButton(self)
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_calendar_edit_regular"))
        self.button.resize(32, 32)
        self.button.clicked.connect(self._on_unfold_button_clicked)

        self.test_label = SiLabel(self)
        # self.test_label.setColor("#20FF0000")
        self.test_label.resize(200, 100)

        self.menu = SiInteractionMenu()
        self.menu.body_.addWidget(self.test_label)
        self.menu.setContentFixedWidth(200)

    def _on_unfold_button_clicked(self):
        pos = self.mapToGlobal(
            QPoint((self.width() - (self.menu.width() - 2 * self.menu.margin - 2 * self.menu.padding)) // 2, 0))
        self.menu.unfold(pos.x(), pos.y())
