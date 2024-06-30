from PyQt5 import QtGui
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from SiliconUI.SiFont import *
from SiliconUI.SiInfo import *
from SiliconUI.SiInputBox import *
from SiliconUI.SiLayout import *
from SiliconUI.SiOption import *
from SiliconUI.SiScrollArea import *
from SiliconUI.SiScrollFrame import *
from SiliconUI.SiSliderBar import *
from SiliconUI.SiSticker import *
from SiliconUI.SiSwitch import *

from .web_url import GithubUrl, browse


# 用到模糊
class SiPixButton(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.image_label = QLabel(self)
        self.mask = QLabel(self)
        self.title = QLabel(self)
        self.discription = QLabel(self)
        self.button = QPushButton(self)

        self.title.setFont(font_L2_bold)
        self.title.move(24, 16)
        self.discription.setFont(font_L1)
        self.discription.setAlignment(Qt.AlignBottom)
        self.discription.move(24, 40)
        self.discription.setWordWrap(True)

        self.title.setStyleSheet("color:#ffffff")
        self.discription.setStyleSheet("color:#ffffff")
        self.mask.setStyleSheet("""
                    border-radius:6px;
                    background-image:none;
                    background-color:qlineargradient(
                        x1:0, y1:1, x2:0, y2:0,
                        stop:0 #7f000000, stop:1 #00000000
                    )""")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)  # 阴影模糊半径
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))  # 阴影颜色和不透明度
        shadow.setOffset(0, 0)  # 阴影偏移量
        self.title.setGraphicsEffect(shadow)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)  # 阴影模糊半径
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))  # 阴影颜色和不透明度
        shadow.setOffset(0, 0)  # 阴影偏移量
        self.discription.setGraphicsEffect(shadow)

    def setPixmap(self, path):
        self.button.setStyleSheet("""
        QPushButton {
            border-radius:6px;
            background-color:transparent;
        }
        QPushButton:hover {
            border-radius:6px;
            background-color:#04ffffff;
        }
        QPushButton:pressed {
            border-radius:6px;
            background-color:#02ffffff;
        }""")

        self.image_label.setStyleSheet(
            f"""
            background-image: url({path});
            border-radius:6px;
            border: 1px solid #2A252D """
        )

    def setText(self, title, discri):
        self.title.setText(title)
        self.discription.setText(discri)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.image_label.resize(w, h)
        self.mask.resize(w, h)
        self.button.resize(w, h)
        self.discription.resize(w - 48, h - 40 - 16)


class WidgetSticker(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.button_github = SiButtonFlat(self)
        self.button_github.resize(32, 32)
        self.button_github.load(SiGlobal.icons.get("fi-rr-link"))
        self.button_github.setHint("前往 GitHub")
        self.button_github.clicked.connect(lambda: browse(GithubUrl.SiliconUI_Home))

        self.button_example = SiButtonFlat(self)
        self.button_example.resize(32, 32)
        self.button_example.load(SiGlobal.icons.get("fi-rr-presentation"))
        self.button_example.setHint("查看使用样例")
        self.button_example.clicked.connect(lambda: browse(GithubUrl.SiliconUI_Home))

        self.head.addItem(self.button_github, side="right")
        self.head.addItem(self.button_example, side="right")

        self.body = SiLayoutV(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.body.setGeometry(24, 16 + 32 + 16, w - 48, h - 64 - 16)


class WidgetSticker_Buttons(WidgetSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.widgets = SiLayoutH(self)
        self.widgets.resize(500, 32)

        self.button_A = SiButton(self)
        self.button_A.setStrong(False)
        self.button_A.setText("普通按钮")
        self.button_A.resize(128, 32)

        self.button_B = SiButton(self)
        self.button_B.setStrong(True)
        self.button_B.setText("高亮按钮")
        self.button_B.resize(128, 32)

        self.button_C = SiButtonHoldtoConfirm(self)
        self.button_C.setText("长按按钮")
        self.button_C.resize(128, 32)

        self.widgets.addItem(self.button_A, "left")
        self.widgets.addItem(self.button_B, "left")
        self.widgets.addItem(self.button_C, "left")

        self.body.addItem(self.widgets, "top")


class WidgetSticker_Switches(WidgetSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.widgets = SiLayoutH(self)
        self.widgets.resize(500, 32)

        self.switch = SiSwitch(self)
        self.switch.resize(128, 32)

        self.widgets.addItem(self.switch, "left")

        self.body.addItem(self.widgets, "top")


class WidgetSticker_Sliders(WidgetSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.slider_A = SiSliderBar(self)
        self.slider_A.resize(500, 32)

        self.body.addItem(self.slider_A, "top")


class WidgetSticker_InputBoxes(WidgetSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.widgets = SiLayoutH(self)
        self.widgets.resize(500, 32)

        self.inputbox = SiInputBox(self)
        self.inputbox.resize(300, 32)

        self.widgets.addItem(self.inputbox, "left")

        self.body.addItem(self.widgets, "top")


class GlazeSticker(WidgetSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.glaze_example = SiOptionButton(self)
        self.glaze_example.resize(500, 0)
        self.glaze_example.setText("Glaze 样例", "使用 Silicon Glaze 帮助您高效构建界面", "确定")
        self.glaze_example.setIcon(SiGlobal.icons.get("fi-rr-apps-add"))

        self.body.addItem(self.glaze_example, "top")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()

        self.glaze_example.resize(w - 48, self.glaze_example.geometry().height())


class SiHomePage(SiScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setStyleSheet("")

        self.rightside_interval = 0

        self.title = QLabel(self)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("Silicon UI")
        self.title.setStyleSheet("color:#fafafa")
        self.title.setFont(font_L4)

        self.subtitle = QLabel(self)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("基于 PyQt5 / PySide6 的 UI 框架，灵动、优雅而轻便")
        self.subtitle.setStyleSheet("color:#fafafa")
        self.subtitle.setFont(font_L1_bold)

        self.theme_image = QLabel(self)
        self.theme_image.setStyleSheet("""  background-image: url('./img/image.png');
                                            border-top-left-radius:8px""")
        self.theme_image.setGeometry(0, 0, 100, 300)

        self.theme_image_hover = QLabel(self)
        self.theme_image_hover.setGeometry(0, 100, 0, 200)
        self.theme_image_hover.setStyleSheet("""
            background-image:none;
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                                              stop:0 #ff252229, stop:1 #00252229)
            """)

        self.interval = 64
        self.delta = 48

        self.title.raise_()
        self.subtitle.raise_()

        self.addH(148)

        self.sticker_project = SiStickerWithBottomButton(self)
        self.sticker_project.setGeometry(64, 148, 196, 256)
        self.sticker_project.setTitle("访问项目主页")
        self.sticker_project.setContent(
            "  访问 GitHub 项目主页，以获取最新版本，参与 Silicon UI 的开发，报告错误，建言献策"
        )
        self.sticker_project.bgimage.setStyleSheet("background-image: url('./img/wiki.png');border-radius:6px")
        self.sticker_project.bottom_button.load(SiGlobal.icons.get("fi-rr-link"))
        self.sticker_project.bottom_button.setHint("前往 GitHub")
        self.sticker_project.bottom_button.clicked.connect(lambda: browse(GithubUrl.SiliconUI_Home))

        self.sticker_wiki = SiStickerWithBottomButton(self)
        self.sticker_wiki.setGeometry(64 + 196 + 32, 148, 196, 256)
        self.sticker_wiki.setTitle("应用示例")
        self.sticker_wiki.setContent("  学习并快速上手 Silicon UI，了解如何开发你的第一件作品")
        self.sticker_wiki.bgimage.setStyleSheet("background-image: url('./img/github.png');border-radius:6px")
        self.sticker_wiki.bottom_button.load(SiGlobal.icons.get("fi-rr-link"))
        self.sticker_wiki.bottom_button.setHint("前往 GitHub")
        self.sticker_wiki.bottom_button.clicked.connect(lambda: browse(GithubUrl.SiliconUI_Home))

        self.addH(300)

        # ============== Stack 开始 ===============

        self.widgets_stack = SiCategory(self)
        self.widgets_stack.setTitle("Silicon 控件")
        self.widgets_stack.resize(1000, 0)

        # 初始化两个 SiLayoutH 用于平行放置四个 Sticker
        self.layout_widgets_A = SiLayoutH(self)
        self.layout_widgets_A.resize(0, 128)
        self.layout_widgets_B = SiLayoutH(self)
        self.layout_widgets_B.resize(0, 128)

        self.sticker_buttons = WidgetSticker_Buttons(self)
        self.sticker_buttons.resize(600, 128)
        self.sticker_buttons.setTitle("按钮")

        self.sticker_switches = WidgetSticker_Switches(self)
        self.sticker_switches.resize(300, 128)
        self.sticker_switches.setTitle("开关")

        self.sticker_inputboxes = WidgetSticker_InputBoxes(self)
        self.sticker_inputboxes.resize(350, 128)
        self.sticker_inputboxes.setTitle("输入框")

        self.sticker_sliders = WidgetSticker_Sliders(self)
        self.sticker_sliders.resize(550, 128)
        self.sticker_sliders.setTitle("滑动条")

        # 四个 sticker 添加到 layout
        self.layout_widgets_A.addItem(self.sticker_buttons, "left")
        self.layout_widgets_A.addItem(self.sticker_switches, "left")
        self.layout_widgets_B.addItem(self.sticker_inputboxes, "left")
        self.layout_widgets_B.addItem(self.sticker_sliders, "left")

        # 添加到 Stack
        self.widgets_stack.addItem(self.layout_widgets_A)
        self.widgets_stack.addItem(self.layout_widgets_B)

        # 添加到 Frame
        self.addItem(self.widgets_stack)

        # ============== Stack 开始 ===============

        self.glazes_stack = SiCategory(self)
        self.glazes_stack.setTitle("Silicon Glaze 界面构建模板")
        self.glazes_stack.resize(916, 0)

        self.sticker_glaze = GlazeSticker(self.glazes_stack)
        self.sticker_glaze.resize(0, 176)
        self.sticker_glaze.setTitle("Glaze 组建预设")

        # 添加到 Stack
        self.glazes_stack.addItem(self.sticker_glaze)

        # 添加到 Frame
        self.addItem(self.glazes_stack)

        # ============== Stack 开始 ===============

        self.info_stack = SiCategory(self)
        self.info_stack.setTitle("提示信息")
        self.info_stack.resize(916, 0)

        self.info_layout = SiLayoutH(self.info_stack)
        self.info_layout.resize(0, 176)

        self.info_bar_A = SiInfo(self.info_layout)
        self.info_bar_A.setFixedWidth(184)
        self.info_bar_A.setType(0)
        self.info_bar_A.setContent(
            "提示",
            "·  你可以创建提示信息<br>·  提示信息支持<strong>富文本</strong><br>·  这段信息过长的时候会自动换行并自动设置高度，你只需要锁定一个宽度",
        )

        self.info_bar_B = SiInfo(self.info_layout)
        self.info_bar_B.setFixedWidth(184)
        self.info_bar_B.setType(1)
        self.info_bar_B.setContent("已完成", "提示信息已经创建完成")

        self.info_bar_C = SiInfo(self.info_layout)
        self.info_bar_C.setFixedWidth(184)
        self.info_bar_C.setType(2)
        self.info_bar_C.setContent("警告", "为什么创建这么多的提示信息，还要堆在一起")

        self.info_bar_D = SiInfo(self.info_layout)
        self.info_bar_D.setFixedWidth(184)
        self.info_bar_D.setType(3)
        self.info_bar_D.setContent("错误", "我们在Bug中发现了少量代码（雾")

        # 添加到 Layout
        self.info_layout.addItem(self.info_bar_A, "left")
        self.info_layout.addItem(self.info_bar_B, "left")
        self.info_layout.addItem(self.info_bar_C, "left")
        self.info_layout.addItem(self.info_bar_D, "left")

        # 添加到 Stack
        self.info_stack.addItem(self.info_layout)

        # 添加到 Frame
        self.addItem(self.info_stack)

        self.adjustSize()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.theme_image.resize(w, self.theme_image.geometry().height())
        self.theme_image_hover.resize(w, 200)
