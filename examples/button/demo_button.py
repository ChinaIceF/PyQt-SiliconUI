import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from SiliconUI.SiButton import SiButton, SiButtonHoldtoConfirm
from SiliconUI.SiLayout import SiLayoutV
from SiliconUI.SiGlobal import colorset

# 当按钮点击事件触发时
def when_button_clicked():
    print('Clicked.')

# 当按钮按下状态改变时
def when_button_holdstatechanged(state):
    print('Hold state changed.', state)


class ButtonExample(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化窗口
        self.initUI()

    def initUI(self):

        # 创建垂直布局
        self.layout = SiLayoutV(self)
        self.layout.setFixedWidth(128)
        self.layout.setAlignment(Qt.AlignCenter)        # 设置元素居中

        # 创建三个按钮
        btn1 = SiButton(self.layout)
        btn1.resize(128, 32)
        btn1.setText('普通按钮')
        btn1.clicked.connect(when_button_clicked)
        btn1.holdStateChanged.connect(when_button_holdstatechanged)

        btn2 = SiButton(self.layout)
        btn2.resize(128, 32)
        btn2.setText('高亮按钮')
        btn2.clicked.connect(when_button_clicked)
        btn2.holdStateChanged.connect(when_button_holdstatechanged)

        btn3 = SiButtonHoldtoConfirm(self.layout)
        btn3.resize(128, 32)
        btn3.setText('长按按钮')
        btn3.clicked.connect(when_button_clicked)
        btn3.holdStateChanged.connect(when_button_holdstatechanged)

        # 将按钮添加到垂直布局中
        self.layout.addItem(btn1)
        self.layout.addItem(btn2)
        self.layout.addItem(btn3)

        # 设置布局位置
        self.layout.move(96, 64)

        # 设置窗口属性
        self.setWindowTitle('SiliconUI.SiButton 三类按钮实例')
        self.setStyleSheet('background-color: {}'.format(colorset.BG_GRAD_HEX[2]))
        self.setGeometry(300, 300, 320, 256)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ButtonExample()
    ex.show()
    sys.exit(app.exec_())
