from siui.components.widgets import SiLabel
from siui.components.page import SiPage
from siui.core.globals import SiGlobal
from siui.core.color import Color
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import SiDenseHContainer
from .components.themed_option_card import ThemedOptionCardPlane


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.Qt import QColor


class ExampleHomepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 滚动区域
        self.titled_widget_group = SiTitledWidgetGroup(self)

        # 整个顶部
        self.head_area = SiLabel(self)
        self.head_area.setFixedHeight(450)

        # 创建背景底图和渐变
        self.background_image = SiLabel(self.head_area)
        self.background_image.setFixedHeight(300)
        self.background_image.setObjectName("bg_image")
        self.background_image.setStyleSheet(
            """
            #bg_image {
                background-image: url('./img/homepage_background.png');
                border-top-left-radius:6px
            }"""
        )

        self.background_fading_transition = SiLabel(self.head_area)
        self.background_fading_transition.setGeometry(0, 100, 0, 200)
        self.background_fading_transition.setStyleSheet(
            """
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 {}, stop:1 {})
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"],
                       Color.transparency(SiGlobal.siui.colors["INTERFACE_BG_B"], 0))
        )

        # 创建大标题和副标题
        self.title = SiLabel(self.head_area)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("Silicon UI")
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title.setFont(SiGlobal.siui.fonts["XL_NORMAL"])

        self.subtitle = SiLabel(self.head_area)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("基于 PyQt5 的 UI 框架，灵动、优雅而轻便")
        self.subtitle.setStyleSheet("color: {}".format(Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.9)))
        self.subtitle.setFont(SiGlobal.siui.fonts["S_BOLD"])

        # 创建一个水平容器
        self.container_for_cards = SiDenseHContainer(self.head_area)
        self.container_for_cards.move(0, 130)
        self.container_for_cards.setFixedHeight(310)
        self.container_for_cards.setAlignCenter(True)
        self.container_for_cards.setSpacing(32)

        # 添加卡片
        self.option_card_project = ThemedOptionCardPlane(self)
        self.option_card_project.setTitle("项目主页")
        self.option_card_project.setFixedSize(218, 270)
        self.option_card_project.setThemeColor("#855198")
        self.option_card_project.setDescription("访问 GitHub 项目主页，以获取最新版本，报告错误，建言献策，参与开发，查询文档和须知，寻求他人答疑解惑</strong>")
        self.option_card_project.setURL("https://github.com/ChinaIceF/PyQt-SiliconUI")

        self.option_card_example = ThemedOptionCardPlane(self)
        self.option_card_example.setTitle("应用示例")
        self.option_card_example.setFixedSize(218, 270)
        self.option_card_example.setThemeColor("#7573aa")
        self.option_card_example.setDescription("学习并快速上手，了解如何使用 SiliconUI 开发你的第一件作品")
        self.option_card_example.setURL("https://github.com/ChinaIceF/PyQt-SiliconUI")

        # 添加到水平容器
        self.container_for_cards.addPlaceholder(64 - 32)
        self.container_for_cards.addWidget(self.option_card_project)
        self.container_for_cards.addWidget(self.option_card_example)

        # 创建QGraphicsDropShadowEffect对象，为水平容器创造阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(48)
        self.container_for_cards.setGraphicsEffect(shadow)

        self.titled_widget_group.addWidget(self.head_area)


        self.setAttachment(self.titled_widget_group)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_image.setFixedWidth(event.size().width())
        self.background_fading_transition.setFixedWidth(event.size().width())