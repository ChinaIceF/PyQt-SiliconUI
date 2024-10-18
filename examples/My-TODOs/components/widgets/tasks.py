from PyQt5.QtGui import QFont

from siui.components import SiLabel, SiWidget
from siui.core import SiColor
from siui.gui import SiFont

from ..core import Task


class TaskCardLinear(SiWidget):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = None

        self.theme_color_indicator = SiLabel(self)
        self.theme_color_indicator.setFixedStyleSheet("border-radius: 8px")

        self.original_panel = SiLabel(self)
        self.original_panel.setFixedStyleSheet("border-radius: 8px")
        self.original_panel.setColor(self.getColor(SiColor.INTERFACE_BG_C))

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet("border-radius: 8px; border-top-left-radius: 6px; border-bottom-left-radius: 6px")

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=18, weight=QFont.Weight.Bold))

        self.description = SiLabel(self)
        self.description.setFont(SiFont.getFont(size=14, weight=QFont.Weight.Normal))

        self.loadTask(task)

    def loadTask(self, task: Task):
        self.task = task
        self.theme_color_indicator.setColor(task.color)
        self.panel.setColor(SiColor.mix(self.getColor(SiColor.INTERFACE_BG_C), task.color, weight=0.9))
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.description.setTextColor(SiColor.mix(self.getColor(SiColor.TEXT_B), task.color))

        self.title.setText(task.name)
        self.description.setText(task.description)

    def getTask(self):
        return self.task

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.theme_color_indicator.resize(48, event.size().height())
        self.original_panel.setGeometry(24, 0, event.size().width() - 24, event.size().height())
        self.panel.setGeometry(24, 0, event.size().width() - 24 - 60, event.size().height())
        self.title.move(80, 18)
        self.description.move(80, 18 + 24)
