from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtSvg import QSvgWidget

from . import SiFont
from . import SiAnimationObject
from . import SiGlobal

from .SiGlobal import colorset
from .SiLabel import SiLabel

import time

class FlatButtonAnimation(SiAnimationObject.SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target - self.current

    def isCompleted(self):
        return self.distance() == 0

class ButtonHasHoldSignal(QPushButton):
    holdStateChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.holding = False
        self.ignore_click_event = False

    def setIgnoreClickEvent(self, v):
        self.ignore_click_event = v

    def isHolding(self):
        return self.holding

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.holding = True
        self.holdStateChanged.emit(True)

    def mouseReleaseEvent(self, event):
        if self.ignore_click_event == False:
            super().mouseReleaseEvent(event)
        self.holding = False
        self.holdStateChanged.emit(False)

class ClickableLabel(SiLabel):
    clicked = QtCore.pyqtSignal()
    holdStateChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        #self.setStyleSheet('')

        self.highlight_alpha = 12
        self.clicked_alpha = 40
        self.radius = 6
        self.has_hover_animation = True

        self.button = ButtonHasHoldSignal(self)
        self.button.clicked.connect(self._clickedAnimation)
        self.button.clicked.connect(self.clicked.emit)
        self.button.holdStateChanged.connect(self.holdStateChanged.emit)
        self.setAlpha(0)

        self.animation = FlatButtonAnimation(self)
        self.animation.ticked.connect(self.change_color)

    def _clickedAnimation(self):
        self.animation.stop()
        self.animation.setCurrent(self.clicked_alpha)
        self.animation.setTarget(self.highlight_alpha)
        self.setAlpha(self.clicked_alpha)
        self.animation.try_to_start()

    def setBorderRadius(self, radius):
        self.radius = radius

    def isHolding(self):
        return self.button.holding

    def setHoverAnimation(self, b):
        self.has_hover_animation = b

    def change_color(self, alpha):
        self.setAlpha(alpha)

    def setAlpha(self, alpha):
        self.button.setStyleSheet('''
            border-radius: {}px;
            background-color:rgba(255, 255, 255, {})
            '''.format(self.radius, alpha))

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.has_hover_animation:
            self.animation.setTarget(self.highlight_alpha)
            self.animation.try_to_start()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.has_hover_animation:
            self.animation.setTarget(0)
            self.animation.try_to_start()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        self.button.resize(w, h)

class SiButtonLabel(ClickableLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

class SiButtonFlat(ClickableLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.hint = ''

        self.icon = QSvgWidget(self)
        self.icon.lower()
        self.icon_w = 16
        self.icon_h = 16

    def setHint(self, hint):
        self.hint = hint

    def setIconSize(self, w, h):
        self.icon_w = w
        self.icon_h = h

    def load(self, path):
        self.icon.load(path)

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.show_animation()
            SiGlobal.floating_window.setText(self.hint)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.hide_animation()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        h = event.size().height()
        self.icon.setGeometry((w - self.icon_w) // 2, (h - self.icon_h) // 2,
                              self.icon_w           , self.icon_h)

class SiButtonFlatWithLabel(SiButtonFlat):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.label = QLabel(self)
        self.label.lower()
        self.label.setFont(SiFont.font_L1)
        self.label.setFixedHeight(32)
        self.label.setStyleSheet('''
            color:{};
            padding-left: 12px;
            '''.format(colorset.TEXT_GRAD_HEX[0]))
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

    def setFixedHeight(self, h):
        super().setFixedHeight(h)
        self.label.setFixedHeight(h)

    def setText(self, text):
        self.label.setText(text)
        self.label.adjustSize()
        self.resize(self.label.width() + 16 + 8, self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.icon.move(8, (h-16)//2)
        self.label.setGeometry(16, 0, w - 16 - 8, h)

class ClickableLabelForButton(ClickableLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.button.setStyleSheet('''
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
            background-color:rgba(255, 255, 255, 0)
            ''')

    def setAlpha(self, alpha):
        self.button.setStyleSheet('''
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
            background-color:rgba(255, 255, 255, {})
            '''.format(alpha))

class SiButton(QLabel):
    clicked = QtCore.pyqtSignal()
    holdStateChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.setStyleSheet('')
        
        self.name = None

        self.frame = QLabel(self)
        self.layer_back = QLabel(self.frame)
        self.layer_front = ClickableLabelForButton(self.frame)
        self.layer_front.setAlignment(QtCore.Qt.AlignHCenter |
                                      QtCore.Qt.AlignVCenter)
        self.layer_front.setFont(SiFont.font_L1_bold)

        self.layer_front.clicked.connect(self.clicked.emit)
        self.layer_front.holdStateChanged.connect(self.holdStateChanged.emit)

        self.initialize_stylesheet()

    def isHolding(self):
        return self.layer_front.isHolding()

    def setStrong(self, status):
        self.initialize_stylesheet(status)

    def initialize_stylesheet(self, strong = False):
        if strong:
            self.layer_back.setStyleSheet('''
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                 stop:0 {}, stop:1 {});
                border-radius: 4px'''.format(*colorset.BTN_HL_HEX[2:4]))

            self.layer_front.setStyleSheet('''
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 {}, stop:1 {});
                color: {};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: 2px;
                border-bottom-right-radius: 2px
            '''.format(*colorset.BTN_HL_HEX[0:2], colorset.BTN_HL_TEXT_HEX))

        else:
            self.layer_back.setStyleSheet('''
                background-color: {};
                border-radius: 4px '''.format(colorset.BTN_NORM_HEX[1]))

            self.layer_front.setStyleSheet('''
                background-color: {};
                color: {};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: 2px;
                border-bottom-right-radius: 2px '''.format(
                    colorset.BTN_NORM_HEX[0],
                    colorset.BTN_NORM_TEXT_HEX,
                ))

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.frame.resize(w, h)
        self.layer_back.resize(w, h)
        self.layer_front.resize(w, h - 3)

    def setText(self, text):
        self.layer_front.setText(text)

class SiButtonHoldThread(QtCore.QThread):
    progress_changed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

    def delta(self):
        p = self.parent.progress
        return (0.08 ** (p + 0.1)) / 10 - 0.003

    def run(self):
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5:

            while self.parent.isHolding() and self.parent.progress <= 1:
                time_start_waiting = time.time()
                self.parent.progress += self.delta()
                self.progress_changed.emit()
                #print(self.parent.progress)
                time.sleep(1/60)

            if self.parent.progress > 1:
                self.parent.layer_front.button.clicked.emit()
                time.sleep(10/60)
                break

            time.sleep(1/60)

        # 回退动画
        while self.parent.progress >= 0:
            self.parent.progress -= 0.1
            self.progress_changed.emit()
            time.sleep(1/60)

        self.parent.progress = 0
        self.progress_changed.emit()

class SiButtonHoldtoConfirm(SiButton):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        

        self.progress = 0

        self.thread = SiButtonHoldThread(self)
        self.thread.progress_changed.connect(self.paintProgress)

        self.layer_back.setStyleSheet('''
            background-color:{};
            border-radius: 4px'''.format(colorset.BTN_HOLD_HEX[2]))
        self.layer_front.setStyleSheet('''
            background-color:{};
            color:{};
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px
            '''.format(colorset.BTN_HOLD_HEX[1], colorset.BTN_HOLD_TEXT_HEX))

        self.layer_front.button.setIgnoreClickEvent(True)
        self.holdStateChanged.connect(self._holdAnimationHandler)

        self.paintProgress()

    def enterEvent(self, event):
        super().enterEvent(event)
        try:
            SiGlobal.floating_window.show_animation()
            SiGlobal.floating_window.setText('长按以确定')
        except:
            pass

    def leaveEvent(self, event):
        super().enterEvent(event)
        try:
            SiGlobal.floating_window.hide_animation()
        except:
            pass

    def _holdAnimationHandler(self, _):
        if self.isHolding() == True:
            if self.thread.isRunning() == False:    # 如果线程没在运行，就启动
                self.thread.start()

    def paintProgress(self):
        p = self.progress
        self.layer_front.setStyleSheet('''
            background-color:qlineargradient(x1:{}, y1:0, x2:{}, y2:0,
                                             stop:0 {}, stop:1 {});
            color:{};
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px
            '''.format(p-0.01, p,
                       *colorset.BTN_HOLD_HEX[0:2], colorset.BTN_HOLD_TEXT_HEX))

class SiRadioButtonGroup(object):
    def __init__(self):
        self.radio_buttons = []

    def addItem(self, obj):
        obj.chose.connect(self._choseHandler)
        self.radio_buttons.append(obj)

    def _choseHandler(self, chose_name):
        for obj in self.radio_buttons:
            if obj.name() != chose_name:
                obj.deactivate()

class SiRadioButton(SiLabel):
    stateChanged = QtCore.pyqtSignal(bool)
    chose = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.setStyleSheet('')

        self.radius = 10
        self.activated = False  # 是否被选中

        self.status_label = QLabel(self)
        self.status_label.resize(20, 20)
        self.status_label.setStyleSheet('''
            border: 2px solid {};
            border-radius: {}px;
        '''.format(colorset.BG_GRAD_HEX[0], self.radius))

        self.border = ClickableLabel(self)
        self.border.resize(20, 20)
        self.border.setBorderRadius(10)
        self.border.clicked.connect(self.activate)

        self.option_name_label = SiLabel(self)
        self.option_name_label.move(28, 0)
        self.option_name_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.option_name_label.setStyleSheet('''
            color: {};
        '''.format(colorset.TEXT_GRAD_HEX[0]))

    def name(self):
        return self.option_name_label.text()

    def setText(self, text):
        self.option_name_label.setText(text)
        self.adjustSize()

    def adjustSize(self):
        self.option_name_label.adjustSize()
        self.resize(self.option_name_label.width()+28, self.height())

    def isActivated(self):
        return self.activated

    def activate(self):
        self.activated = True
        self.stateChanged.emit(True)
        self.chose.emit(self.name())
        self.status_label.setStyleSheet('''
            border: 4px solid {};
            border-radius: {}px;
        '''.format(colorset.BTN_HL_HEX[1], self.radius))

    def deactivate(self):
        self.activated = False
        self.stateChanged.emit(False)
        self.status_label.setStyleSheet('''
            border: 2px solid {};
            border-radius: {}px;
        '''.format(colorset.BG_GRAD_HEX[0], self.radius))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        h = event.size().height()

        self.status_label.move(0, (h-20)//2)
        self.border.move(0, (h-20)//2)
        self.option_name_label.setGeometry(28, 0, w-28, h)
