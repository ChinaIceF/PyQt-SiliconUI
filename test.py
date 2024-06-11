import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet('background-color:#2C2930')
        self.initUI()

    def initUI(self):
        # 创建复选框
        self.checkbox = QCheckBox('Check me', self)
        self.checkbox.setGeometry(50, 50, 100, 32)
        self.checkbox.toggle()  # 初始设置为选中状态
        self.checkbox.setStyleSheet('''

            QCheckBox::indicator:unchecked
            {
                /* 设置边框的风格*/
                border-style: solid;
                border-width: 1px;
                border-color: rgb(255, 255, 255);
                border-radius: 4px;
                width: 16px;
                height: 16px;
                background-color: transparent;
            }

            QCheckBox::indicator:checked
            {
                /* 设置边框的风格*/
                border-style: solid;
                border-width: 1px;
                border-color: rgb(255, 255, 255);
                border-radius: 4px;
                width: 16px;
                height: 16px;
                background-color: rgb(255, 255, 255);
            }
            ''')

        # 连接状态改变信号到槽函数
        self.checkbox.stateChanged.connect(self.on_state_changed)

        # 设置窗口属性
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox example')
        self.show()

    def on_state_changed(self, state):
        if state == Qt.Checked:
            print('QCheckBox is checked')
        else:
            print('QCheckBox is unchecked')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
