import pyperclip
from PyQt5.QtCore import Qt

from siui.components import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiFlowContainer,
    SiLabel,
    SiLineEdit,
    SiPushButton,
    SiScrollArea,
    SiSimpleButton,
)
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.core import SiColor
from siui.core import SiGlobal
from siui.core import Si


def get_on_button_clicked_func(button):
    def on_button_clicked():
        pyperclip.copy(button.objectName())
        SiGlobal.siui.windows["TOOL_TIP"].setText(
            f"{button.objectName()}<br>"
            f'<span style="color: {button.getColor(SiColor.TEXT_D)}">复制成功</span>',
        )
    return on_button_clicked


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return 0

    previous_row = range(len(s2) + 1)
    for i, ltr1 in enumerate(s1):
        current_row = [i + 1]
        for j, ltr2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + int(ltr1 != ltr2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1] / max(len(s1), len(s2))


class ExampleIcons(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_page_index = 0
        self.icon_dict = None

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("图标库")

        self.content_container = SiDenseVContainer(self)
        self.content_container.setAlignment(Qt.AlignCenter)
        self.content_container.setAdjustWidgetsSize(True)

        self.package_operation_container = SiDenseHContainer(self)
        self.package_operation_container.setFixedHeight(48)
        self.package_operation_container.setAlignment(Qt.AlignCenter)

        self.package_selection_description = SiLabel(self)
        self.package_selection_description.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_D)}")
        self.package_selection_description.setAlignment(Qt.AlignVCenter)
        self.package_selection_description.setText("当前图标包")
        self.package_selection_description.adjustSize()

        self.package_selection_combobox = SiComboBox(self)
        self.package_selection_combobox.resize(256, 32)
        self.package_selection_combobox.addOption("所有图标包", (None,))
        for package_name in SiGlobal.siui.iconpack.getClassNames():
            self.package_selection_combobox.addOption(package_name)
        self.package_selection_combobox.valueChanged.connect(self.on_package_changed)
        self.package_selection_combobox.menu().setShowIcon(False)
        self.package_selection_combobox.colorGroup().assign(
            SiColor.INTERFACE_BG_B, self.getColor(SiColor.INTERFACE_BG_A))
        self.package_selection_combobox.colorGroup().assign(
            SiColor.INTERFACE_BG_D, self.getColor(SiColor.INTERFACE_BG_C))

        self.search_description = SiLabel(self)
        self.search_description.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_D)}")
        self.search_description.setAlignment(Qt.AlignVCenter)
        self.search_description.setText("搜索图标")
        self.search_description.adjustSize()

        self.search_input_box = SiLineEdit(self)
        self.search_input_box.resize(256, 32)
        self.search_input_box.reloadStyleSheet()
        self.search_input_box.line_edit.textChanged.connect(self.on_search_text_changed)
        self.search_input_box.colorGroup().assign(
            SiColor.INTERFACE_BG_B, self.getColor(SiColor.INTERFACE_BG_A))
        self.search_input_box.colorGroup().assign(
            SiColor.INTERFACE_BG_D, self.getColor(SiColor.INTERFACE_BG_C))

        self.package_operation_container.addWidget(self.package_selection_description)
        self.package_operation_container.addWidget(self.package_selection_combobox)
        self.package_operation_container.addPlaceholder(16)
        self.package_operation_container.addWidget(self.search_description)
        self.package_operation_container.addWidget(self.search_input_box)
        self.package_operation_container.adjustSize()

        self.icon_scroll_area = SiScrollArea(self)

        self.icon_container = SiFlowContainer(self)
        self.icon_container.setLineHeight(96)

        self.icon_scroll_area.setAttachment(self.icon_container)

        self.operation_panel_container_v = SiDenseVContainer(self)
        self.operation_panel_container_v.setAlignment(Qt.AlignCenter)

        self.operation_panel_container_h = SiDenseHContainer(self)
        self.operation_panel_container_h.setFixedHeight(48)
        self.operation_panel_container_h.setAlignment(Qt.AlignCenter)

        self.page_up_button = SiPushButton(self)
        self.page_up_button.attachment().setText("上一页")
        self.page_up_button.setFixedSize(128, 32)
        self.page_up_button.clicked.connect(lambda: self.load_icon_page_to(self.icon_page_index - 1))

        self.page_index_label = SiLabel(self)
        self.page_index_label.setAlignment(Qt.AlignCenter)
        self.page_index_label.setFixedSize(128, 32)
        self.page_index_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.page_index_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_D)}")

        self.page_down_button = SiPushButton(self)
        self.page_down_button.attachment().setText("下一页")
        self.page_down_button.setFixedSize(128, 32)
        self.page_down_button.clicked.connect(lambda: self.load_icon_page_to(self.icon_page_index + 1))

        self.operation_panel_container_h.addWidget(self.page_up_button)
        self.operation_panel_container_h.addWidget(self.page_index_label)
        self.operation_panel_container_h.addWidget(self.page_down_button)
        self.operation_panel_container_h.adjustSize()

        self.operation_panel_container_v.addWidget(self.operation_panel_container_h)

        self.content_container.addWidget(self.package_operation_container)
        self.content_container.addPlaceholder(4)
        self.content_container.addWidget(self.icon_scroll_area)
        self.content_container.addWidget(self.operation_panel_container_v, "bottom")

        # load package indexed 0
        self.package_selection_combobox.menu().setIndex(0)

    def on_package_changed(self, package_name):
        if package_name == (None,):
            package_name = None
        self.icon_dict = SiGlobal.siui.iconpack.getDict(package_name)
        self.load_icon_page_to(0)

    def on_search_text_changed(self, text):
        self.load_icon_page_to(0, fade_ani=False)

    def load_icon_page_to(self, page_index, fade_ani=True):
        icon_dict = self.icon_dict
        icon_pack = SiGlobal.siui.iconpack
        page_capacity = 50

        from_index, to_index = page_capacity * page_index, page_capacity * (page_index + 1)
        icon_list = list(zip(icon_dict.keys(), icon_dict.values()))
        target = self.search_input_box.line_edit.text()

        # return if index is out of range
        if (page_index < 0) or (page_index > len(icon_list) // page_capacity):
            return

        # sort icon list if search box is not empty
        if target.strip() != "":
            icon_list = [item for item in icon_list if target.strip() in item[0]]
            icon_list = sorted(icon_list, key=lambda s: levenshtein_distance(s[0], target))

        self.icon_page_index = page_index
        self.page_index_label.setText(f"{self.icon_page_index+1}/{len(icon_list) // page_capacity + 1}")
        self.operation_panel_container_h.adjustSize()

        for index, widget in enumerate(list(self.icon_container.widgets())):
            if fade_ani is True:
                self.icon_container.removeWidget(widget, fade_out=True, fade_out_delay=index*3)
            else:
                self.icon_container.removeWidget(widget)

        for key, value in icon_list[from_index:to_index]:
            widget = SiLabel(self)
            widget.setFixedSize(96, 96)
            widget.setObjectName(key)
            widget.animationGroup().fromToken("opacity").setBias(0.02)

            svg_button = SiSimpleButton(widget)
            svg_button.colorGroup().assign(SiColor.BUTTON_OFF,
                                           svg_button.getColor(SiColor.INTERFACE_BG_C))
            svg_button.attachment().setSvgSize(32, 32)
            svg_button.attachment().load(icon_pack.getFromData(value, self.getColor(SiColor.SVG_NORMAL)))
            svg_button.setFixedSize(96, 96)
            svg_button.setHint(
                f"{key}<br>"
                f'<span style="color: {self.getColor(SiColor.TEXT_D)}">点击复制图标名称</span>'
            )
            svg_button.clicked.connect(get_on_button_clicked_func(widget))
            svg_button.reloadStyleSheet()

            self.icon_container.addWidget(widget, arrange=False)
            widget.show()

        self.icon_container.arrangeWidgets(ani=False,
                                           all_fade_in=fade_ani,
                                           fade_in_delay=50,
                                           fade_in_delay_cumulate_rate=2)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.icon_container.resize(event.size().width() - 2 * self.padding, self.icon_container.height())
        self.icon_container.arrangeWidgets()
        self.icon_container.adjustSize()

        self.content_container.setGeometry(self.padding,
                                           self.title_height,
                                           self.icon_container.width(),
                                           event.size().height() - self.title_height - 64)
        self.content_container.arrangeWidget()
        self.icon_scroll_area.resize(self.icon_scroll_area.width(), self.content_container.height() - 64 - 80)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.icon_container.arrangeWidgets(ani=False, all_fade_in=True, fade_in_delay=300, fade_in_delay_cumulate_rate=2)