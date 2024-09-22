from PyQt5.QtCore import Qt

from siui.components.option_card import SiOptionCardLinear, SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.progress_bar import SiProgressBar
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiLabel, SiPushButton, SiSimpleButton
from siui.core import SiGlobal
from siui.core import Si


class ExampleOptionCards(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # From here, we can start to build our first page in Silicon Application
        # You can set the name of this page, and add widgets to varify the function to beautify it.

        # Set the title of the page
        # self.setTitle("应用模版")

        # Set X Offset for better outfit.
        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("选项卡")

        # Create a SiTitledWidgetGroup object
        self.titled_widget_group = SiTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        # 线性选项卡
        self.option_card_linear_beginning = SiOptionCardLinear(self)
        self.option_card_linear_beginning.setTitle("使用线性选项卡搭建框架", "从线性选项卡这一基础元素开始构建你的应用界面")
        self.option_card_linear_beginning.load(SiGlobal.siui.iconpack.get("ic_fluent_rectangle_landscape_regular"))

        attached_button_a = SiPushButton(self)
        attached_button_a.resize(128, 32)
        attached_button_a.attachment().setText("绑定按钮")

        attached_button_b = SiPushButton(self)
        attached_button_b.resize(32, 32)
        attached_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_attach_regular"))

        self.option_card_linear_attaching = SiOptionCardLinear(self)
        self.option_card_linear_attaching.setTitle("绑定控件", "线性选项卡提供水平容器，可以添加任意控件，不限数量")
        self.option_card_linear_attaching.load(SiGlobal.siui.iconpack.get("ic_fluent_attach_regular"))
        self.option_card_linear_attaching.addWidget(attached_button_a)
        self.option_card_linear_attaching.addWidget(attached_button_b)

        # <- ADD
        self.titled_widget_group.addTitle("线性选项卡")
        self.titled_widget_group.addWidget(self.option_card_linear_beginning)
        self.titled_widget_group.addWidget(self.option_card_linear_attaching)

        # 平面选项卡
        header_button = SiSimpleButton(self)
        header_button.setFixedHeight(32)
        header_button.attachment().setText("Header 区域")
        header_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_window_header_horizontal_regular"))
        header_button.adjustSize()

        body_label = SiLabel(self)
        body_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        body_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        body_label.setText("平面选项卡提供了三个容器：header，body，footer，每个容器都可以独立访问\n其中 header 和 footer 是水平容器，body 是垂直容器\n这个容器是平面选项卡的 body，在这里尽情添加控件吧！")

        footer_button_a = SiSimpleButton(self)
        footer_button_a.resize(32, 32)
        footer_button_a.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pen_regular"))
        footer_button_a.setHint("绘制")

        footer_button_b = SiSimpleButton(self)
        footer_button_b.resize(32, 32)
        footer_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_eyedropper_regular"))
        footer_button_b.setHint("取色器")

        footer_button_c = SiSimpleButton(self)
        footer_button_c.resize(32, 32)
        footer_button_c.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_save_regular"))
        footer_button_c.setHint("保存")

        self.option_card_plane_beginning = SiOptionCardPlane(self)
        self.option_card_plane_beginning.setTitle("平面选项卡")
        self.option_card_plane_beginning.header().addWidget(header_button, side="right")
        self.option_card_plane_beginning.body().addWidget(body_label, side="top")
        self.option_card_plane_beginning.footer().setFixedHeight(64)
        self.option_card_plane_beginning.footer().setSpacing(8)
        self.option_card_plane_beginning.footer().setAlignment(Qt.AlignCenter)
        self.option_card_plane_beginning.footer().addWidget(footer_button_a, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_b, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_c, side="left")
        self.option_card_plane_beginning.adjustSize()

        # <- ADD
        self.titled_widget_group.addTitle("平面选项卡")
        self.titled_widget_group.addWidget(self.option_card_plane_beginning)

        # 容器

        container_h = SiDenseHContainer(self)
        container_h.setSpacing(8)
        container_h.setFixedHeight(80+8+250)

        container_v = SiDenseVContainer(self)
        container_v.setSpacing(8)
        container_v.setAdjustWidgetsSize(True)
        self.titled_widget_group.resized.connect(lambda pos: container_v.setFixedWidth(pos[0] - 320 - 8))

        container_description = SiOptionCardLinear(self)
        container_description.setTitle("嵌套容器", "让你的界面布局更加美观和直观")
        container_description.load(SiGlobal.siui.iconpack.get("ic_fluent_slide_layout_regular"))

        container_plane_left_bottom = SiOptionCardPlane(self)
        container_plane_left_bottom.setTitle("资源监视器")
        container_plane_left_bottom.setFixedHeight(250)

        label_cpu = SiLabel(self)
        label_cpu.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        label_cpu.setText("CPU")

        progress_bar_cpu = SiProgressBar(self)
        progress_bar_cpu.setFixedHeight(8)
        progress_bar_cpu.setValue(0.12)

        label_ram = SiLabel(self)
        label_ram.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        label_ram.setText("内存")

        progress_bar_ram = SiProgressBar(self)
        progress_bar_ram.setFixedHeight(8)
        progress_bar_ram.setValue(0.61)

        label_gpu = SiLabel(self)
        label_gpu.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
        label_gpu.setText("GPU")

        progress_bar_gpu = SiProgressBar(self)
        progress_bar_gpu.setFixedHeight(8)
        progress_bar_gpu.setValue(0.23)

        container_plane_left_bottom.body().setAdjustWidgetsSize(True)
        container_plane_left_bottom.body().addWidget(label_cpu)
        container_plane_left_bottom.body().addWidget(progress_bar_cpu)
        container_plane_left_bottom.body().addWidget(label_ram)
        container_plane_left_bottom.body().addWidget(progress_bar_ram)
        container_plane_left_bottom.body().addWidget(label_gpu)
        container_plane_left_bottom.body().addWidget(progress_bar_gpu)

        container_v.addWidget(container_description)
        container_v.addWidget(container_plane_left_bottom)

        container_plane_right = SiOptionCardPlane(self)
        container_plane_right.setTitle("操作面板")
        container_plane_right.setFixedHeight(80+8+250)
        container_plane_right.setFixedWidth(320)

        label_nothing = SiLabel()
        label_nothing.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_D"]))
        label_nothing.setText("这里好像什么也没有")
        label_nothing.setAlignment(Qt.AlignCenter)
        label_nothing.setFixedHeight(220)

        container_plane_right.body().setAdjustWidgetsSize(True)
        container_plane_right.body().addWidget(label_nothing)

        container_h.addWidget(container_v)
        container_h.addWidget(container_plane_right)

        # <- ADD
        self.titled_widget_group.addTitle("容器")
        self.titled_widget_group.addWidget(container_h)

        # add placeholder for better outfit
        self.titled_widget_group.addPlaceholder(64)

        # Set SiTitledWidgetGroup object as the attachment of the page's scroll area
        self.setAttachment(self.titled_widget_group)

