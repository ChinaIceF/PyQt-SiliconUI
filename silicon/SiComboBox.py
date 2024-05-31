from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel, QDialog
from PyQt5.QtSvg import QSvgWidget

from . import SiFont

class DeactivateEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate or event.type() == QEvent.Wheel:
            self.func()
            return True  # 如果事件已被处理，返回True
        return QObject.eventFilter(self, obj, event)  # 对于其他事件，继续传递
    
    def connect(self, func):
        self.func = func

class SiComboBoxDialog(QDialog):
    def __init__(self, parent, pos):
        super().__init__()
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setGeometry(pos.x(), pos.y(), 400, 100)
        self.setModal(False)  # 设置为模态对话框

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 400, 100)
        self.label.setStyleSheet('background-color:red')
        self.label.setText('123')
        
        self.eventFilter = DeactivateEventFilter()
        self.eventFilter.connect(self.destory)
        self.label.installEventFilter(self.eventFilter)
        
    def showEvent(self, event):
        self.label.show()
        self.activateWindow()

    def destory(self):
        print('销毁')
        self.parent.destoryDialog()  # 调用父对象的销毁方法

    def closeEvent(self, event):
        self.destory()
        
    '''
    def focusOutEvent(self, event):
        # 当下拉窗口失去焦点时，销毁下拉窗口
        print('a')
        super().focusOutEvent(event)
        self.destory()
    '''
class SiComboBox(QLabel):
    click_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('')
        self.parent = parent
        self.name = None
        self.dialog = None
        
        self.combobox_frame = QLabel(self)
        self.combobox_background = QLabel(self.combobox_frame)
        self.combobox_bar = QLabel(self.combobox_frame)
        self.combobox_text = QLabel(self.combobox_bar)
        self.combobox_icon = QSvgWidget(self.combobox_bar)
        self.combobox_icon.load(SiGlobal.icons.get('fi-rr-angle-small-down'))
        
        self.combobox_text.setAlignment(QtCore.Qt.AlignVCenter)
        self.combobox_text.setFont(SiFont.font_L1)
        self.combobox_text.setText('测试内容')
        
    def getFramePos(self):
        return self.combobox_frame.mapToGlobal(self.combobox_frame.pos())
        
    def createDialog(self):
        pos = self.getFramePos()
        self.dialog = SiComboBoxDialog(self, pos)
        self.dialog.show()

    def destoryDialog(self):
        self.dialog.deleteLater()
        self.dialog = None

    def mousePressEvent(self, event):
        if not self.dialog:
            self.createDialog()


    def initialize_stylesheet(self):
        self.combobox_background.setStyleSheet('background-color:#493f4e; border-radius: 4px; border: 1px solid #594f5e')
        self.combobox_bar.setStyleSheet('')
        self.combobox_text.setStyleSheet('color:#fefefe')
        self.combobox_icon.setStyleSheet('')
        
        #self.combobox_text.setStyleSheet('background-color:#ff0000')
        #self.combobox_icon.setStyleSheet('background-color:#ff0000')
        
    def setGeometry(self, x, y, w, h):
        super().setGeometry(x, y, w, h)
        self.combobox_frame.setGeometry(0, 0, w, h)
        self.combobox_background.setGeometry(0, 0, w, h)
        self.combobox_bar.setGeometry(12, 4, w - 12 - 8, h - 8)
        self.combobox_text.setGeometry(0, 0, w - 12 - 8 - 20, h - 8)
        self.combobox_icon.setGeometry(w - 12 - 8 - 16, (h - 8 - 16) // 2, 16, 16)