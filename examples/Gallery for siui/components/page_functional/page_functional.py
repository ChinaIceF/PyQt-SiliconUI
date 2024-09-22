from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup, SiPushButton, SiLabel, SiLongPressButton, SiDenseHContainer, \
    SiMasonryContainer
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.core import SiColor
from siui.core import SiQuickEffect
from siui.core import SiGlobal
from siui.templates.application.components.dialog.modal import SiModalDialog

from ..option_card import OptionCardPlaneForWidgetDemos
from .components.music_displayer.music_displayer import SiMusicDisplayer

class ExampleFunctional(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1040)
        self.setScrollAlignment(Qt.AlignHCenter)
        self.setTitle("功能组件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 音乐展示框
        with self.titled_widgets_group as group:
            group.addTitle("音乐展示框")

            self.displayer_container = SiMasonryContainer(self)
            self.displayer_container.setColumns(2)
            self.displayer_container.setColumnWidth(512)
            self.displayer_container.setFixedWidth(512 + 512 + 16)
            self.displayer_container.setSpacing(horizontal=16, vertical=16)

            self.demo_displayer_1 = SiMusicDisplayer(self)
            self.demo_displayer_1.resize(512, 128)
            self.demo_displayer_1.loadInfo("./img/pages/functional/music_covers/cover1.jpg", "Moon Without The Stars", "Unknown Artist", "Unknown Album")  # noqa: E501

            self.demo_displayer_2 = SiMusicDisplayer(self)
            self.demo_displayer_2.resize(512, 128)
            self.demo_displayer_2.loadInfo("./img/pages/functional/music_covers/cover2.png", "Never Gonna Give You Up", "Rick Astley", "Whenever You Need Somebody")  # noqa: E501

            self.demo_displayer_3 = SiMusicDisplayer(self)
            self.demo_displayer_3.resize(512, 128)
            self.demo_displayer_3.loadInfo("./img/pages/functional/music_covers/cover3.png", "Friend", "玉置浩二", "ワインレッドの心")  # noqa: E501

            self.demo_displayer_4 = SiMusicDisplayer(self)
            self.demo_displayer_4.resize(512, 128)
            self.demo_displayer_4.loadInfo("./img/pages/functional/music_covers/cover4.png", "雨中的重逢", "Parion圆周率", "Reunion In The Rain")  # noqa: E501

            self.demo_displayer_5 = SiMusicDisplayer(self)
            self.demo_displayer_5.resize(512, 128)
            self.demo_displayer_5.loadInfo("./img/pages/functional/music_covers/cover5.png", "Melting White", "塞壬唱片-MSR / Cubes Collective", "Melting White")  # noqa: E501

            self.demo_displayer_6 = SiMusicDisplayer(self)
            self.demo_displayer_6.resize(512, 128)
            self.demo_displayer_6.loadInfo("./img/pages/functional/music_covers/cover6.png", "Axolotl", "C418", "Axolotl")  # noqa: E501

            self.displayer_container.addWidget(self.demo_displayer_1)
            self.displayer_container.addWidget(self.demo_displayer_2)
            self.displayer_container.addWidget(self.demo_displayer_3)
            self.displayer_container.addWidget(self.demo_displayer_4)
            self.displayer_container.addWidget(self.demo_displayer_5)
            self.displayer_container.addWidget(self.demo_displayer_6)

            group.addWidget(self.displayer_container)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

