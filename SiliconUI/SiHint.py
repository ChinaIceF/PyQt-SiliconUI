
from .SiAnimationObject import *
from .SiFont import *
from .SiGlobal import colorset

class FloatingSizeAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__()

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= 1:
            return dis
        else:
            return (abs(dis) * 0.25 + 1) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0


class FloatingTransparencyAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__()
        

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= 1:
            return dis
        else:
            return (abs(dis) * 0.25 + 1) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0


class FloatingWindow(QWidget):
    def __init__(self, parent=None):
        super(FloatingWindow, self).__init__(parent,
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.status = False

        self.timer = QTimer()
        self.timer.setInterval(int(1000/60))
        self.timer.timeout.connect(self.refresh_position)
        self.timer.start()

        self.resize_animation = FloatingSizeAnimation(self)
        self.resize_animation.ticked.connect(self.resize_delta_handler)

        self.transparency_animation = FloatingTransparencyAnimation(self)
        self.transparency_animation.ticked.connect(self.transparency_delta_handler)

        self.highlight_animation = FloatingTransparencyAnimation(self)
        self.highlight_animation.ticked.connect(self.highlight_delta_handler)

        self.interval = 8  # 左右两侧的间隔
        self.shadow_radius = 8  # 阴影半径

        self.initUI()
        self.setText('')

    def initUI(self):

        self.background = QLabel(self)
        self.background.setStyleSheet('''
            background-color:{};
            border-radius: 6px; '''.format(colorset.HINT_HEX[1]))

        # 创建QGraphicsDropShadowEffect对象
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 128))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(int(self.shadow_radius * 1.5))
        self.setGraphicsEffect(shadow)

        self.label = QLabel(self)
        self.label.setStyleSheet('''
            background-color:transparent;
            color:{} '''.format(colorset.HINT_HEX[0]))
        self.label.move(8,0)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.setFont(font_L1)

        self.highlight = QLabel(self)
        self.highlight.setStyleSheet('''
            background-color:rgba(255, 255, 255, 1);
            border-radius: 6px ''')

    def setText(self, text, flash = True):
        text = str(text)
        self.label.setText(text)

        w = self.label.fontMetrics().width(text)

        self.resize_animation.setTarget(w)
        self.resize_animation.try_to_start()

        if flash == True:
            a = 128
            self.highlight.setStyleSheet('''
                background-color:rgba(255, 255, 255, {});
                border-radius: 6px'''.format(a))
            self.highlight_animation.setTarget(0)
            self.highlight_animation.setCurrent(a)
            self.highlight_animation.try_to_start()

    def highlight_delta_handler(self, alpha):
        self.highlight.setStyleSheet('''
            background-color:rgba(255, 255, 255, {});
            border-radius: 6px '''.format(alpha / 255))

    def resize_delta_handler(self, width):
        dw = 2 * (self.interval + self.shadow_radius)
        dh = 2 * self.shadow_radius
        self.resize(int(width + dw), 32 + dh)

    def transparency_delta_handler(self, opacity):
        self.setWindowOpacity(opacity / 255)

    def resizeEvent(self, event):
        dw = 2 * (self.interval + self.shadow_radius)
        dh = 2 * self.shadow_radius
        size = event.size()

        w, h = size.width(), size.height()

        self.highlight.setGeometry(self.shadow_radius, self.shadow_radius, w-2*self.shadow_radius, h-2*self.shadow_radius)
        self.background.setGeometry(self.shadow_radius, self.shadow_radius, w-2*self.shadow_radius, h-2*self.shadow_radius)
        self.label.setGeometry(self.interval + self.shadow_radius, self.shadow_radius, w - dw, h - dh)

    def refresh_position(self):
        pos = QCursor.pos()
        x, y =  pos.x(), pos.y()
        self.move(x, y - self.geometry().height())

    def hide_animation(self):
        self.setText('', flash = False)
        self.status = False
        self.transparency_animation.setTarget(0)
        self.transparency_animation.try_to_start()

    def show_animation(self):
        self.status = True
        self.transparency_animation.setTarget(255)
        self.transparency_animation.try_to_start()
