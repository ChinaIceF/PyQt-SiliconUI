from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtSvg import QSvgWidget

from . import SiFont
from . import SiStyle
from . import SiAnimationObject
from . import SiGlobal

import time

class SiButtonFlat(QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('')
        self.parent = parent

        self.hint = ''

        self.icon = QSvgWidget(self)
        self.icon_w = 16
        self.icon_h = 16

        self.button = QPushButton(self)
        self.button.clicked.connect(self.clicked.emit)  # 绑定信号
        self.button.setStyleSheet('border-radius:6px;background-color:rgba(255, 255, 255, 0)')

        self.target_alpha = 0
        self.current_alpha = 0

        self.animation = SiAnimationObject.SiAnimation(self.distance, self.stepLength, 1000 / 60, lambda : self.distance() == 0)
        self.animation.ticked.connect(self.change_color)

    def setHint(self, hint):
        self.hint = hint

    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target_alpha - self.current_alpha

    def change_color(self, delta_alpha):
        self.current_alpha += delta_alpha
        self.current_alpha = max(0, self.current_alpha)
        self.button.setStyleSheet('border-radius:6px;background-color:rgba(255, 255, 255, {})'.format(self.current_alpha))

    def setIconSize(self, w, h):
        self.icon_w = w
        self.icon_h = h

    def load(self, path):
        self.icon.load(path)
    '''
    def mousePressEvent(self, event):
        print('pressed')
        self.target_alpha = 30
        self.tryStartAnimation()
        #self.clicked.emit()

    def mouseReleaseEvent(self, event):
        print('released')
        self.target_alpha = 12
        self.tryStartAnimation()
    '''

    def enterEvent(self, event):
        self.target_alpha = 12
        self.tryStartAnimation()

        SiGlobal.floating_window.show_animation()
        SiGlobal.floating_window.setText(self.hint)

    def leaveEvent(self, event):
        self.target_alpha = 0
        self.tryStartAnimation()

        SiGlobal.floating_window.hide_animation()

    def tryStartAnimation(self):
        if self.animation.isActive() == False:
            self.animation.start()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.icon.setGeometry((w - self.icon_w) // 2, (h - self.icon_h) // 2, self.icon_w, self.icon_h)
        self.button.resize(w, h)




class SiButton(QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('')
        self.parent = parent
        self.name = None

        self.frame = QLabel(self)
        self.layer_back = QLabel(self.frame)
        self.layer_front = QLabel(self.frame)
        self.highlight = QLabel(self.frame)
        self.highlight.setVisible(False)
        self.layer_front.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.layer_front.setFont(SiFont.font_L1_bold)

        self.initialize_stylesheet()

    def setStrong(self, status):
        self.initialize_stylesheet(status)

    def initialize_stylesheet(self, strong = False):
        if strong:
            self.layer_back.setStyleSheet('background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #372456, stop:1 #562b49); border-radius: 4px')
            self.highlight.setStyleSheet('background-color:#10ffffff; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')
            self.layer_front.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #52389a, stop:1 #9c4e8b)  ; color:#d8c1c2; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')
        else:
            self.layer_back.setStyleSheet('background-color:#2f2b34; border-radius: 4px')
            self.highlight.setStyleSheet('background-color:#10ffffff; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')
            self.layer_front.setStyleSheet('background-color: #493f4e; color:#e2e2e2; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')

    def enterEvent(self, event):
        self.highlight.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.highlight.setVisible(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.frame.resize(w, h)
        self.layer_back.resize(w, h)
        self.layer_front.resize(w, h - 3)
        self.highlight.resize(w, h - 3)

    def setText(self, text):
        self.layer_front.setText(text)


class SiButtonHoldThread(QtCore.QThread):
    progress_changed = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def delta(self):
        p = self.parent.progress
        return (0.08 ** (p + 0.1)) / 10 - 0.003

    def run(self):
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5:

            while self.parent.isHolding():

                time_start_waiting = time.time()
                self.parent.progress += self.delta()
                self.progress_changed.emit()
                #print(self.parent.progress)
                time.sleep(1/60)

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
        self.parent = parent

        self.holding = False
        self.progress = 0

        self.thread = SiButtonHoldThread(self)
        self.thread.progress_changed.connect(self.paintProgress)

        self.layer_back.setStyleSheet('background-color:#6a3246; border-radius: 4px')
        self.highlight.setStyleSheet('background-color:#10ffffff; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')
        self.layer_front.setStyleSheet('background-color:#9F3652; color:#d8c1c2; border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px')

        self.paintProgress()

    def enterEvent(self, event):
        super().enterEvent(event)
        SiGlobal.floating_window.show_animation()
        SiGlobal.floating_window.setText('Hold to confirm')

    def leaveEvent(self, event):
        super().enterEvent(event)
        SiGlobal.floating_window.hide_animation()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.holding = True

        if self.thread.isRunning() == False:    # 如果线程没在运行，就启动
            self.thread.start()

    def mouseReleaseEvent(self, event):
        super().mousePressEvent(event)
        self.holding = False

    def isHolding(self):
        return self.holding

    def paintProgress(self):
        p = self.progress
        self.layer_front.setStyleSheet(
            '''
            background-color:qlineargradient(x1:{}, y1:0, x2:{}, y2:0, stop:0 #D82A5A, stop:1 #9F3652);
            color:#fafafa;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px
            '''.format(p-0.01, p)
            )
