from PyQt5.QtGui import QFont

from siui.components import SiLabel, SiSimpleButton, SiSvgLabel, SiWidget
from siui.core import SiColor, SiGlobal
from siui.gui import SiFont


class RectButtonWithIconAndDescription(SiWidget):
    def __init__(self, title, description, icon_name, parent=None):
        super().__init__(parent)

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet("border-radius: 4px")
        self.panel.setColor(self.getColor(SiColor.INTERFACE_BG_C))

        self.icon_circle = SiLabel(self)
        self.icon_circle.setFixedSize(32, 32)
        self.icon_circle.move(20, 24)
        self.icon_circle.setFixedStyleSheet("border-radius: 16px")
        self.icon_circle.setColor(self.getColor(SiColor.INTERFACE_BG_D))

        self.icon = SiSvgLabel(self.icon_circle)
        self.icon.resize(32, 32)
        self.icon.load(SiGlobal.siui.iconpack.get(icon_name, color_code=self.getColor(SiColor.SVG_NORMAL)))
        self.icon.setSvgSize(16, 16)

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=16, weight=QFont.Weight.Bold))
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.title.setText(title)
        self.title.adjustSize()
        self.title.move(72, 20)

        self.description = SiLabel(self)
        self.description.setFont(SiFont.getFont(size=14, weight=QFont.Weight.Light))
        self.description.setTextColor(self.getColor(SiColor.TEXT_D))
        self.description.setText(description)
        self.description.adjustSize()
        self.description.move(72, 20 + 20)

        self.button_ = SiSimpleButton(self)
        self.button_.setBorderRadius(4)

    def button(self):
        return self.button_

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.panel.resize(event.size())
        self.button_.resize(event.size())
