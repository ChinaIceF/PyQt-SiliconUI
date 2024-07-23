import numpy
from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup
from siui.components.page import SiPage
from siui.components.widgets import SiDenseHContainer, SiDraggableLabel, SiIconLabel, SiLabel, SiPixLabel, SiPushButton
from siui.core.globals import SiGlobal
from siui.core.silicon import Si

from .option_card import OptionCardPlaneForWidgetDemos


class ExampleWidgets(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("控件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 标签
        with self.titled_widgets_group as group:
            group.addTitle("标签")

            # 文字标签
            self.label_for_text = OptionCardPlaneForWidgetDemos(self)
            self.label_for_text.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                 "/widgets/label.py")
            self.label_for_text.setTitle("文字标签")
            self.label_for_text.setFixedWidth(580)

            self.demo_label = SiLabel(self)
            self.demo_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label.setText("测试标签")

            self.demo_label_hinted = SiLabel(self)
            self.demo_label_hinted.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label_hinted.setText("测试标签（具有工具提示）")
            self.demo_label_hinted.setHint("使用 setHint 方法设置工具提示")

            self.demo_label_with_svg = SiIconLabel(self)
            self.demo_label_with_svg.load(SiGlobal.siui.icons["fi-rr-comment"])
            self.demo_label_with_svg.setText(" 具有 SVG 图标的标签")

            self.label_for_text.body().addWidget(self.demo_label)
            self.label_for_text.body().addWidget(self.demo_label_hinted)
            self.label_for_text.body().addWidget(self.demo_label_with_svg)
            self.label_for_text.body().addPlaceholder(12)
            self.label_for_text.adjustSize()

            # 图片标签
            self.pix_label = OptionCardPlaneForWidgetDemos(self)
            self.pix_label.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                            "/widgets/label.py")
            self.pix_label.setTitle("图片标签")
            self.pix_label.setFixedWidth(580)

            container_pix_label = SiDenseHContainer(self)
            container_pix_label.setFixedHeight(80)

            self.demo_pix_label_a = SiPixLabel(self)
            self.demo_pix_label_a.setFixedSize(80, 80)
            self.demo_pix_label_a.setBorderRadius(40)
            self.demo_pix_label_a.load("./img/avatar1.png")
            self.demo_pix_label_a.setHint("<strong>尺寸：</strong> 80px * 80px<br>"
                                          "<strong>圆角半径：</strong> 40px")

            self.demo_pix_label_b = SiPixLabel(self)
            self.demo_pix_label_b.setFixedSize(80, 80)
            self.demo_pix_label_b.setBorderRadius(32)
            self.demo_pix_label_b.load("./img/avatar1.png")
            self.demo_pix_label_b.setHint("<strong>尺寸：</strong> 80px * 80px<br>"
                                          "<strong>圆角半径：</strong> 32px")

            container_pix_label.addWidget(self.demo_pix_label_a)
            container_pix_label.addWidget(self.demo_pix_label_b)

            self.pix_label.body().addWidget(container_pix_label)
            self.pix_label.body().addPlaceholder(12)
            self.pix_label.adjustSize()

            # 标签动画
            self.label_ani = OptionCardPlaneForWidgetDemos(self)
            self.label_ani.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                            "/widgets/label.py")
            self.label_ani.setTitle("标签动画")
            self.label_ani.setAdditionalDescription("特性")
            self.label_ani.setFixedWidth(580)

            self.demo_move_area = SiLabel(self)
            self.demo_move_area.setFixedSize(526, 80)

            self.demo_label_ani = SiLabel(self.demo_move_area)
            self.demo_label_ani.setFixedStyleSheet("border-radius: 4px")
            self.demo_label_ani.resize(128, 32)
            self.demo_label_ani.setMoveLimits(0, 0, 526, 80)
            self.demo_label_ani.setHint("标签的 moveTo, resizeTo 等内置动画方法提供灵动的动画")

            container_label_ani_for_buttons = SiDenseHContainer(self)
            container_label_ani_for_buttons.setFixedHeight(32)

            self.ctrl_button_random_pos_for_label_ani = SiPushButton(self)
            self.ctrl_button_random_pos_for_label_ani.attachment().setText("随机位置")
            self.ctrl_button_random_pos_for_label_ani.resize(128, 32)
            self.ctrl_button_random_pos_for_label_ani.clicked.connect(
                lambda: self.demo_label_ani.moveTo(numpy.random.randint(0, 526), numpy.random.randint(0, 80)))

            self.ctrl_button_random_size_for_label_ani = SiPushButton(self)
            self.ctrl_button_random_size_for_label_ani.attachment().setText("随机尺寸")
            self.ctrl_button_random_size_for_label_ani.resize(128, 32)
            self.ctrl_button_random_size_for_label_ani.clicked.connect(
                lambda: self.demo_label_ani.resizeTo(numpy.random.randint(32, 256), numpy.random.randint(16, 64)))

            self.ctrl_button_reset_for_label_ani = SiPushButton(self)
            self.ctrl_button_reset_for_label_ani.attachment().setText("还原初始状态")
            self.ctrl_button_reset_for_label_ani.resize(128, 32)
            self.ctrl_button_reset_for_label_ani.clicked.connect(lambda: self.demo_label_ani.moveTo(0, 0))
            self.ctrl_button_reset_for_label_ani.clicked.connect(lambda: self.demo_label_ani.resizeTo(128, 32))

            container_label_ani_for_buttons.addWidget(self.ctrl_button_random_pos_for_label_ani)
            container_label_ani_for_buttons.addWidget(self.ctrl_button_random_size_for_label_ani)
            container_label_ani_for_buttons.addWidget(self.ctrl_button_reset_for_label_ani)

            self.label_ani.body().addWidget(self.demo_move_area)
            self.label_ani.body().addWidget(container_label_ani_for_buttons)
            self.label_ani.body().addPlaceholder(12)
            self.label_ani.adjustSize()

            # 可拖动标签
            self.draggable_label = OptionCardPlaneForWidgetDemos(self)
            self.draggable_label.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui"
                                                  "/components/widgets/label.py")
            self.draggable_label.setTitle("可拖动标签")
            self.draggable_label.setFixedWidth(580)

            self.demo_drag_area = SiLabel(self)
            self.demo_drag_area.setFixedSize(526, 80)

            self.demo_draggable_label = SiDraggableLabel(self.demo_drag_area)
            self.demo_draggable_label.setFixedStyleSheet("border-radius: 4px")
            self.demo_draggable_label.setMoveLimits(0, 0, 526, 80)
            self.demo_draggable_label.resize(128, 32)
            self.demo_draggable_label.setHint("使用 setMoveLimits 方法限制移动范围"
                                              "\n移动动画（可禁用）提供更平滑的移动效果")

            self.draggable_label.body().addWidget(self.demo_drag_area)
            self.draggable_label.body().addPlaceholder(12)
            self.draggable_label.adjustSize()

            # <- 添加到控件组
            group.addWidget(self.label_for_text)
            group.addWidget(self.pix_label)
            group.addWidget(self.label_ani)
            group.addWidget(self.draggable_label)

        # 按钮
        with self.titled_widgets_group as group:
            group.addTitle("按钮")

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 标签
        # 文字标签
        self.demo_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.demo_label_hinted.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.demo_label_with_svg.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        # 标签动画
        self.demo_label_ani.setColorTo(SiGlobal.siui.colors["INTERFACE_BG_E"])
        # 可拖动标签
        self.demo_draggable_label.setColorTo(SiGlobal.siui.colors["INTERFACE_BG_E"])
