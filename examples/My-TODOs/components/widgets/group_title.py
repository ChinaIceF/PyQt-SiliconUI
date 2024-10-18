from PyQt5.Qt import QFont

from siui.components import SiLabel, SiWidget
from siui.core import SiColor
from siui.gui import SiFont


class SmallGroupTitle(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=16, weight=QFont.Weight.Bold))

        self.title_indicator = SiLabel(self)
        self.title_indicator.setFixedStyleSheet("border-radius: 1px")

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.title_indicator.setColor(self.getColor(SiColor.TITLE_INDICATOR))

    def setTitle(self, title):
        self.title.setText(title)
        self.title.adjustSize()
        self.adjustSize()

    def adjustSize(self):
        self.resize(self.title.width(), self.title.height() + 8)
        self.title_indicator.setGeometry(0, self.height() - 3, self.width(), 3)
