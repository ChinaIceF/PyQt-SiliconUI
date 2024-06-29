
from .SiMenu import *
from .SiButton import *
from .SiGlobal import colorset

class SiComboBox(ClickableLabel):
    valueChanged = pyqtSignal(object)
    textChanged = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.highlight_alpha = 4
        self.setHoverAnimation(True)

        self.arrow = QSvgWidget(self)
        self.arrow.lower()
        self.arrow.resize(16, 16)
        self.arrow.load(SiGlobal.icons.get('fi-rr-angle-small-down'))

        self.label = QLabel(self)
        self.label.lower()
        self.label.setStyleSheet('''
            background-color:{};
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 4px;
            color: {};
            '''.format(colorset.BG_GRAD_HEX[1], colorset.TEXT_GRAD_HEX[0]))
        self.label.setFont(SiFont.font_L1)
        self.label.setText('测试文字')

        self.menu = SiMenu(None)
        self.menu.textChanged.connect(lambda x: self.label.setText(x))
        self.menu.textChanged.connect(self.textChanged.emit)
        self.menu.valueChanged.connect(self.valueChanged.emit)

        self.clicked.connect(self.popup)

    def addOption(self, name, value):
        self.menu.addOption(name, value)

    def setOption(self, name):
        self.menu.setOption(name)

    def popup(self):
        global_pos = self.label.mapToGlobal(self.label.pos())
        self.menu.popup(global_pos.x() - self.menu.margin, global_pos.y() + 24)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.label.resize(w, h)
        self.arrow.move(w - 24, (h-16)//2)
        self.menu.resize(w + 2 * self.menu.margin, self.menu.height())
