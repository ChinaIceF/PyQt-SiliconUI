import time

from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup, SiPixLabel, SiDenseVContainer
from siui.components.page import SiPage
from siui.core import Si, SiColor

from ..core import Task
from ..widgets import SmallGroupTitle, TaskCardLinear
from .components import TodayMainWidget


class SmallTitledWidgetGroup(SiTitledWidgetGroup):
    def addTitle(self, title):

        if len(self.widgets_top) > 0:
            self.addPlaceholder(16)

        new_title = SmallGroupTitle(self)
        new_title.setTitle(title)
        self.addWidget(new_title)


class Homepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(0)
        self.setScrollMaximumWidth(10000)
        # self.setTitle("主页")

        self.head_pic_and_content = SiDenseVContainer(self)
        self.head_pic_and_content.setAlignment(Qt.AlignHCenter)
        self.head_pic_and_content.setSpacing(0)

        self.background_image = SiPixLabel(self)
        self.background_image.load("./images/default_background.png")
        self.background_image.setFixedHeight(320)
        self.background_image.setBorderRadius(6)

        self.titled_widget_group = SmallTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.titled_widget_group.addPlaceholder(32)

        with self.titled_widget_group as group:
            #group.addTitle("时间线")

            self.today_main_widget = TodayMainWidget(self)
            self.today_main_widget.adjustSize()

            group.addPlaceholder(16)
            group.addWidget(self.today_main_widget)

        self.titled_widget_group.addPlaceholder(32)

        with self.titled_widget_group as group:
            group.addTitle("待办详情")

            self.test_task_card = TaskCardLinear(Task("上床睡觉", "闭上眼睛直接睡觉就行", time.time(), self.getColor(SiColor.PROGRESS_BAR_COMPLETING)), parent=self)
            self.test_task_card.resize(0, 80)

            self.test_task_card2 = TaskCardLinear(Task("写数学作业", "不写完作业该怎么交作业呢", time.time(), self.getColor(SiColor.PROGRESS_BAR_PROCESSING)), parent=self)
            self.test_task_card2.resize(0, 80)

            group.addPlaceholder(16)
            group.addWidget(self.test_task_card)
            group.addWidget(self.test_task_card2)

        self.titled_widget_group.addPlaceholder(64)

        self.head_pic_and_content.addWidget(self.background_image)
        self.head_pic_and_content.addWidget(self.titled_widget_group)

        self.setAttachment(self.head_pic_and_content)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_image.resize(event.size().width(), 200)
        self.titled_widget_group.resize(event.size().width() - 128, self.titled_widget_group.height())
        self.head_pic_and_content.arrangeWidget()
