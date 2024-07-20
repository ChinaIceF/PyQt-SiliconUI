import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

sys.path.append(str(Path().cwd()))

from siui.components.widgets import (
    SiCheckBox,
    SiLongPressButton,
    SiPushButton,
    SiRadioButton,
    SiSimpleButton,
    SiSwitch,
    SiToggleButton,
)
from siui.gui import colorsets


class ButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        # 设置窗口属性
        self.setWindowTitle("SiliconUI.SiPushButton 三类按钮实例")
        self.setStyleSheet(f"background-color: {colorsets.SiColorDark.BG_GRAD_HEX[2]}")
        self.setGeometry(300, 300, 320, 256)

        # 初始化窗口
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        self.layout = QVBoxLayout()
        # 设置包含该布局的部件的宽度
        self.setLayout(self.layout)
        self.setFixedWidth(128)
        # 设置子部件在布局中的对齐方式
        self.layout.setAlignment(Qt.AlignCenter)

        # 创建按钮
        push_button = SiPushButton()
        push_button.resize(128, 32)
        push_button.setText("普通按钮")
        push_button.clicked.connect(lambda: print("普通按钮被点击"))

        long_press_button = SiLongPressButton()
        long_press_button.resize(128, 32)
        long_press_button.setText("长按按钮")
        long_press_button.clicked.connect(lambda: print("长按按钮被点击"))

        toggle_button = SiToggleButton()
        toggle_button.resize(128, 32)
        toggle_button.setText("开关按钮")
        toggle_button.clicked.connect(lambda: print("开关按钮被点击"))

        simple_button = SiSimpleButton()
        simple_button.resize(128, 32)
        simple_button.setText("简单按钮")
        simple_button.clicked.connect(lambda: print("简单按钮被点击"))

        radio_button = SiRadioButton()
        radio_button.resize(128, 32)
        radio_button.setText("单选按钮")
        radio_button.toggled.connect(lambda: print("单选按钮被点击"))

        check_box = SiCheckBox()
        check_box.resize(128, 32)
        check_box.setText("复选框")
        check_box.toggled.connect(lambda: print("复选框被点击"))

        switch = SiSwitch()
        switch.resize(128, 32)
        switch.setText("开关")
        switch.clicked.connect(lambda: print("开关被点击"))

        # 将按钮添加到垂直布局中
        self.layout.addWidget(push_button)
        self.layout.addWidget(long_press_button)
        self.layout.addWidget(toggle_button)
        self.layout.addWidget(simple_button)
        self.layout.addWidget(radio_button)
        self.layout.addWidget(check_box)
        self.layout.addWidget(switch)


if __name__ == "__main__":
    app = QApplication()
    ex = ButtonExample()
    ex.show()
    app.exec()
