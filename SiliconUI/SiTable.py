
from PyQt5.QtWidgets import QLabel

from .SiGlobal import colorset
from .SiFont import *

class SingleData(SiliconUI.SiLabel):
    def __init__(self, data, strong = False, color = colorset.TEXT_GRAD_HEX[1]):
        super().__init__(parent = None)
        self.setFixedHeight(32)
        self.setStyleSheet('color: {}; padding: 4px'.format(color))

        self.setText(data)

        if strong:
            self.setFont(font_L1_bold)


class ScrollContent(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.backgrounds = []

        self.bg_placeholder = SiliconUI.SiLayoutV(self)
        self.bg_placeholder.setAlignCenter(True)
        self.bg_placeholder.setInterval(0)
        self.bg_placeholder.addVacant(32)

        self.data_placeholder = SiliconUI.SiLayoutH(self)
        self.data_placeholder.setInterval(0)
        self.data_placeholder.addVacant(24)

        self.colors = [colorset.BG_GRAD_HEX[1], colorset.BG_GRAD_HEX[2]]

    def adjustSize(self):
        self.data_placeholder.adjustSize()
        self.resize(self.data_placeholder.size())

    def addBackground(self, id):
        color = self.colors[id % 2]
        new_label = QLabel(self)
        new_label.setStyleSheet('''
            background-color: {};
            border-radius: 8px
        '''.format(color))
        new_label.resize(self.width() - 16, 32)
        self.bg_placeholder.addItem(new_label)
        self.backgrounds.append(new_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.bg_placeholder.resize(w, self.bg_placeholder.height())
        self.data_placeholder.resize(w, self.data_placeholder.height())

        for bg in self.backgrounds:
            bg.resize(w - 16, 32)

        self.bg_placeholder.adjustSize()

class SiTable(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.classes = []
        self.classes_width = []
        self.data = []
        self.classes_layouts = []

        self.outline = QLabel(self)
        self.outline.setStyleSheet('''
            border-radius: 4px;
            border: 1px solid {};
            background-color: {}
        '''.format(colorset.BG_GRAD_HEX[2], colorset.BG_GRAD_HEX[1]))

        self.scroll_content = ScrollContent(self)
        self.scroll_content.resize(0, 1)

        self.scroll_area = SiliconUI.SiScrollArea(self)
        self.scroll_area.attach_content(self.scroll_content)

    def setClasses(self, classes, width):
        self.classes = classes
        self.classes_width = width
        # 初始化表头
        self._createEachClassesLayout()

    def _createEachClassesLayout(self):
        for name, width in zip(self.classes, self.classes_width):
            new_layout = SiliconUI.SiLayoutV(self)
            new_layout.setFixedWidth(width)
            new_layout.setInterval(0)
            new_layout.addItem(
                SingleData(name, strong = True, color = colorset.TEXT_GRAD_HEX[0])
            )
            self.scroll_content.data_placeholder.addItem(new_layout)
            self.classes_layouts.append(new_layout)

    def addData(self, data):
        self.data.append(data)
        for layout, value in zip(self.classes_layouts, data):
            newdata = SingleData(value)
            layout.addItem(newdata)
        self.scroll_content.addBackground(len(self.data))
        self.scroll_content.adjustSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.outline.resize(w, h)
        self.scroll_area.setGeometry(0, 1, w, h-2)
        self.scroll_content.resize(w, self.scroll_content.height())
