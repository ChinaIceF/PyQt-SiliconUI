
from .SiAnimationObject import *
from .SiGlobal import *
from . import SiGlobal

class SiSlider(QLabel):
    value_change = pyqtSignal(float)
    dragged = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.dispersed = False  # 是否离散型
        self.levels = []  # 离散取值空间

        self.setMouseTracking(True)  # 开启鼠标追踪

    def setDispersed(self, levels):
        self.levels = list(levels)  # 归一化，可以接受 list 或者 range 对象
        self.dispersed = True

    def enterEvent(self, event):
        SiGlobal.floating_window.show_animation()
        SiGlobal.floating_window.setText(round(self.getValue(), 11))

    def leaveEvent(self, event):
        SiGlobal.floating_window.hide_animation()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton):
            return

        newpos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        max_x = self.max_x()
        x = max(0, min(newpos.x(), max_x))

        if self.dispersed == False:  # 连续
            self.value_change.emit(round(x / max_x, 11))
            self.dragged.emit(x / max_x)
            event.accept()
            return

        else:  # 离散
            n = len(self.levels)
            d = max_x / (n - 1)   # 每个档位之间的间隔
            current_level = int((x + d / 2) // d)    # 所处档位

            self.value_change.emit(self.levels[current_level])
            self.dragged.emit(current_level * d / self.max_x())
            event.accept()
            return

    def getValue(self):
        x = self.x()
        max_x = self.max_x()
        if self.dispersed == False:  # 连续
            return x / max_x
        else:  # 离散
            n = len(self.levels)
            d = max_x / (n - 1)   # 每个档位之间的间隔
            current_level = int((x + d / 2) // d)    # 所处档位
            return self.levels[current_level]

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            event.accept()

    def value(self):
        max_x = self.max_x()
        x = self.geometry().x()

        return x / max_x

    def max_x(self):
        return self.parent.geometry().width() - self.geometry().width()

class SiSliderBar(QLabel):
    valueChanged = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.value_bar = QLabel(self)
        self.background_bar = QLabel(self)
        self.slider = SiSlider(self)
        self.slider.value_change.connect(self.valueChanged.emit)
        self.slider.dragged.connect(self.animationHandler)

        self.target_value = 0
        self.current_value = 0

        self.animation = SiAnimation(self.distance, self.stepLength, 1000 / SiGlobal.fps, lambda : abs(self.distance()) == 0)
        self.animation.ticked.connect(self.changePosition)

        self.background_bar.setStyleSheet('''
            background-color:{};
            border-radius: 2px'''.format(colorset.BG_GRAD_HEX[1]))

        self.value_bar.setStyleSheet('''
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 {}, stop:1 {});
            border-radius: 2px'''.format(*colorset.THEME_HEX))

        self.slider.setStyleSheet('''
            border-radius: 4px;
            background-color: {}'''.format(colorset.THEME_HEX[0]))

        self.valueChanged.connect(self.hint_handler)

        self.bar_width = 32
        self.bar_height = 8

    def hint_handler(self, value):
        SiGlobal.floating_window.setText(str(value), flash = False)  # 滑动时不触发闪烁动画，避免一片白

    def setDispersed(self, levels):
        self.slider.setDispersed(levels)

    def animationHandler(self, target_value):
        self.target_value = int(target_value * self.slider.max_x()) / self.slider.max_x()
        if target_value == 1:
            self.target_value = 1.0

        if self.animation.isActive() == False:
            self.animation.start()

    def distance(self):
        return self.target_value - self.current_value

    def stepLength(self, dis):
        if abs(dis) <= 0.01:
            return dis
        else:
            return (abs(dis) * 0.25) * (1 if dis > 0 else -1)

    def value(self):
        return self.slider.value()

    def changePosition(self, delta = None):
        if delta is None:
            delta = self.distance()

        self.current_value = delta
        v = self.current_value
        g = self.value_bar.geometry()
        d = int(g.width() * (1 - v))
        self.background_bar.setGeometry(g.width() - d + self.bar_width //2, g.y(), d, g.height())

        g = self.geometry()
        self.slider.move(int((g.width() - self.bar_width) * v), (g.height() - self.bar_height) // 2)
        p = g.width()/self.bar_width
        self.slider.setStyleSheet('''
            background-color: qlineargradient(x1:{}, y1:0, x2:{}, y2:0,
                                              stop:0 {}, stop:1 {});
            border-radius: 4px;'''.format(-v * p, (1-v) * p, *colorset.THEME_HEX))


    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        x = self.bar_width // 2
        y = (h - 4) // 2

        self.background_bar.setGeometry(x, y, w - self.bar_width, 4)
        self.value_bar.setGeometry(x, y, w - self.bar_width, 4)
        self.slider.setGeometry(0, (h - self.bar_height) // 2, self.bar_width, self.bar_height)

        self.changePosition()
