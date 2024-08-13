import os

from components import ThemedOptionCardPlane
from icons import IconDictionary
from PyQt5.Qt import QColor, QPoint
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QTextEdit
from settings_parser import SettingsParser
from todos_parser import TODOParser

from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
    SiSvgLabel,
    SiSwitch,
    SiToggleButton,
)
from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.core.globals import NewGlobal, SiGlobal
from siui.components.tooltip.tooltip import ToolTipWindow

# 创建删除队列
SiGlobal.todo_list = NewGlobal()
SiGlobal.todo_list.delete_pile = []

# 创建锁定位置变量
SiGlobal.todo_list.position_locked = False

# 创建设置文件解析器并写入全局变量
SiGlobal.todo_list.settings_parser = SettingsParser("./options.ini")
SiGlobal.todo_list.todos_parser = TODOParser("./todos.ini")

def lock_position(state):
    SiGlobal.todo_list.position_locked = state


# 主题颜色
def load_colors(is_dark=True):
    if is_dark is True:  # 深色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#e1d9e8").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#e1d9e8"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#252229"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = SiGlobal.siui.colors["INTERFACE_BG_A"]
        SiGlobal.siui.colors["BORDER_COLOR"] = "#3b373f"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "ef413a47"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#52389a"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#9c4e8b"

        SiGlobal.siui.colors["TEXT_A"] = "#FFFFFF"
        SiGlobal.siui.colors["TEXT_B"] = "#e1d9e8"
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#D2D2D2"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#100912"

        SiGlobal.siui.colors["BUTTON_HOVER"] = "#10FFFFFF"
        SiGlobal.siui.colors["BUTTON_FLASH"] = "#20FFFFFF"

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    else:  # 亮色主题
        # 加载图标
        SiGlobal.siui.icons.update(IconDictionary(color="#0F85D3").icons)

        # 设置颜色
        SiGlobal.siui.colors["THEME"] = "#0F85D3"
        SiGlobal.siui.colors["PANEL_THEME"] = "#0F85D3"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#F3F3F3"
        SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"] = "#e8e8e8"
        SiGlobal.siui.colors["BORDER_COLOR"] = "#d0d0d0"
        SiGlobal.siui.colors["TOOLTIP_BG"] = "#F3F3F3"
        SiGlobal.siui.colors["SVG_A"] = SiGlobal.siui.colors["THEME"]

        SiGlobal.siui.colors["THEME_TRANSITION_A"] = "#2abed8"
        SiGlobal.siui.colors["THEME_TRANSITION_B"] = "#2ad98e"

        SiGlobal.siui.colors["TEXT_A"] = "#1f1f2f"
        SiGlobal.siui.colors["TEXT_B"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.85)
        SiGlobal.siui.colors["TEXT_C"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.75)
        SiGlobal.siui.colors["TEXT_D"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.6)
        SiGlobal.siui.colors["TEXT_E"] = Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.5)

        SiGlobal.siui.colors["SWITCH_DEACTIVATE"] = "#bec1c7"
        SiGlobal.siui.colors["SWITCH_ACTIVATE"] = "#F3F3F3"

        SiGlobal.siui.colors["BUTTON_HOVER"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.0625)
        SiGlobal.siui.colors["BUTTON_FLASH"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.43)

        SiGlobal.siui.colors["SIMPLE_BUTTON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.6)

        SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0)
        SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"] = Color.transparency(SiGlobal.siui.colors["THEME"], 0.1)

    SiGlobal.siui.reloadAllWindowsStyleSheet()


# 加载主题颜色
load_colors(is_dark=False)


class SingleSettingOption(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(2)

        self.title = SiLabel(self)
        self.title.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.title.setAutoAdjustSize(True)

        self.description = SiLabel(self)
        self.description.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.description.setAutoAdjustSize(True)

        self.addWidget(self.title)
        self.addWidget(self.description)
        self.addPlaceholder(4)

    def setTitle(self, title: str, description: str):
        self.title.setText(title)
        self.description.setText(description)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.description.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_D"]))


class SingleTODOOption(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_box = SiCheckBox(self)
        self.check_box.resize(12, 12)
        self.check_box.setText(" ")
        self.check_box.toggled.connect(self._onChecked)

        self.text_label = SiLabel(self)
        self.text_label.resize(500 - 48 - 48 - 32, 32)
        self.text_label.setWordWrap(True)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setFixedStyleSheet("padding-top: 2px; padding-bottom: 2px")

        self.addWidget(self.check_box)
        self.addWidget(self.text_label)

        self.move = self.moveTo

        # 初始化时自动载入样式表
        self.reloadStyleSheet()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))

    def _onChecked(self, state):
        if state is True:
            SiGlobal.todo_list.delete_pile.append(self)
        else:
            index = SiGlobal.todo_list.delete_pile.index(self)
            SiGlobal.todo_list.delete_pile.pop(index)

    def setText(self, text: str):
        self.text_label.setText(text)

    def adjustSize(self):
        self.setFixedHeight(self.text_label.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.text_label.setFixedWidth(event.size().width() - 48)
        self.text_label.adjustSize()
        self.adjustSize()


class AppHeaderPanel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        self.container_h = SiDenseHContainer(self)
        self.container_h.setAlignment(Qt.AlignCenter)
        self.container_h.setFixedHeight(48)
        self.container_h.setSpacing(0)

        self.icon = SiSvgLabel(self)
        self.icon.resize(32, 32)
        self.icon.setSvgSize(16, 16)

        self.unfold_button = SiToggleButton(self)
        self.unfold_button.setFixedHeight(32)
        self.unfold_button.attachment().setText("0个待办事项")
        self.unfold_button.setChecked(True)

        self.settings_button = SiToggleButton(self)
        self.settings_button.resize(32, 32)
        self.settings_button.setHint("设置")
        self.settings_button.setChecked(False)

        self.add_todo_button = SiToggleButton(self)
        self.add_todo_button.resize(32, 32)
        self.add_todo_button.setHint("添加新待办")
        self.add_todo_button.setChecked(False)

        self.container_h.addPlaceholder(16)
        self.container_h.addWidget(self.icon)
        self.container_h.addPlaceholder(4)
        self.container_h.addWidget(self.unfold_button)

        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.settings_button, "right")
        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.add_todo_button, "right")

        # 按钮加入全局变量
        SiGlobal.todo_list.todo_list_unfold_button = self.unfold_button
        SiGlobal.todo_list.add_todo_unfold_button = self.add_todo_button
        SiGlobal.todo_list.settings_unfold_button = self.settings_button

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size().width(), 48)
        self.container_h.resize(event.size().width(), 48)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        # 按钮颜色
        self.unfold_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                         SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.settings_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])
        self.add_todo_button.setStateColor(SiGlobal.siui.colors["TOGGLE_BUTTON_OFF_BG"],
                                           SiGlobal.siui.colors["TOGGLE_BUTTON_ON_BG"])

        # svg 图标
        self.settings_button.attachment().load(SiGlobal.siui.icons["fi-rr-menu-burger"])
        self.add_todo_button.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        self.icon.load('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" '
                       'data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M0,8v-1C0,4.243,'
                       '2.243,2,5,2h1V1c0-.552,.447-1,1-1s1,.448,1,1v1h8V1c0-.552,.447-1,1-1s1,.448,1,1v1h1c2.757,0,'
                       '5,2.243,5,5v1H0Zm24,2v9c0,2.757-2.243,5-5,5H5c-2.757,0-5-2.243-5-5V10H24Zm-6.168,'
                       '3.152c-.384-.397-1.016-.409-1.414-.026l-4.754,4.582c-.376,.376-1.007,'
                       '.404-1.439-.026l-2.278-2.117c-.403-.375-1.035-.354-1.413,.052-.376,.404-.353,1.037,.052,'
                       '1.413l2.252,2.092c.566,.567,1.32,.879,2.121,.879s1.556-.312,2.108-.866l4.74-4.568c.397-.383,'
                       '.409-1.017,.025-1.414Z" fill="{}" /></svg>'.format(SiGlobal.siui.colors["SVG_A"]).encode())

        self.background_label.setStyleSheet("""background-color: {}; border: 1px solid {}""".format(
            SiGlobal.siui.colors["BACKGROUND_COLOR"], SiGlobal.siui.colors["BORDER_COLOR"]))
        self.unfold_button.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))


class TODOListPanel(ThemedOptionCardPlane):
    todoAmountChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("全部待办")
        self.setUseSignals(True)

        self.no_todo_label = SiLabel(self)
        self.no_todo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.no_todo_label.setAutoAdjustSize(True)
        self.no_todo_label.setText("当前没有待办哦")
        self.no_todo_label.setAlignment(Qt.AlignCenter)
        self.no_todo_label.hide()

        self.body().setUseMoveTo(False)
        self.body().setAdjustWidgetsSize(True)

        self.footer().setFixedHeight(64)
        self.footer().setSpacing(8)
        self.footer().setAlignment(Qt.AlignCenter)

        self.complete_all_button = SiSimpleButton(self)
        self.complete_all_button.resize(32, 32)
        self.complete_all_button.setHint("全部完成")
        self.complete_all_button.clicked.connect(self._onCompleteAllButtonClicked)

        self.footer().addWidget(self.complete_all_button, "right")

        # 全局方法
        SiGlobal.todo_list.addTODO = self.addTODO

    def updateTODOAmount(self):
        todo_amount = len(self.body().widgets_top)
        self.todoAmountChanged.emit(todo_amount)

        if todo_amount == 0:
            self.no_todo_label.show()
        else:
            self.no_todo_label.hide()

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.no_todo_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))
        self.complete_all_button.attachment().load(SiGlobal.siui.icons["fi-rr-list-check"])

    def _onCompleteAllButtonClicked(self):
        for obj in self.body().widgets_top:
            if isinstance(obj, SingleTODOOption):
                obj.check_box.setChecked(True)

    def addTODO(self, text):
        new_todo = SingleTODOOption(self)
        self.body().addWidget(new_todo)

        new_todo.setText(text)
        new_todo.show()
        new_todo.adjustSize()

        SiGlobal.todo_list.todo_list_unfold_button.setChecked(True)
        self.adjustSize()
        self.updateTODOAmount()

    def adjustSize(self):
        self.body().adjustSize()
        super().adjustSize()

    def leaveEvent(self, event):
        super().leaveEvent(event)

        for index, obj in enumerate(SiGlobal.todo_list.delete_pile):
            self.body().removeWidget(obj)
            obj.close()

        SiGlobal.todo_list.delete_pile = []

        if SiGlobal.todo_list.todo_list_unfold_button.isChecked() is True:
            self.adjustSize()
            self.updateTODOAmount()

    def showEvent(self, a0):
        super().showEvent(a0)
        self.updateTODOAmount()
        self.setForceUseAnimations(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.no_todo_label.resize(event.size().width(), 150)


class AddNewTODOPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("添加新待办")
        self.setUseSignals(True)

        self.confirm_button = SiSimpleButton(self)
        self.confirm_button.resize(32, 32)
        self.confirm_button.setHint("确认并添加")

        self.cancel_button = SiSimpleButton(self)
        self.cancel_button.resize(32, 32)
        self.cancel_button.setHint("取消")

        self.header().addWidget(self.cancel_button, "right")
        self.header().addWidget(self.confirm_button, "right")

        self.instruction = SiLabel(self)
        self.instruction.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.instruction.setText("请输入待办内容")

        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedHeight(70)
        self.text_edit.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.text_edit.lineWrapMode()

        self.body().setAdjustWidgetsSize(True)
        self.body().setSpacing(4)
        self.body().addWidget(self.instruction)
        self.body().addWidget(self.text_edit)

    def adjustSize(self):
        self.resize(self.width(), 200)

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.confirm_button.attachment().load(SiGlobal.siui.icons["fi-rr-check"])
        self.cancel_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross"])
        self.instruction.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        self.text_edit.setStyleSheet(
            """
            border: 1px solid {};
            background-color: {};
            border-radius: 4px;
            padding-left: 8px; padding-right: 8px;
            color: {}
            """.format(SiGlobal.siui.colors["BORDER_COLOR"],
                       SiGlobal.siui.colors["BACKGROUND_DARK_COLOR"],
                       SiGlobal.siui.colors["TEXT_B"])
        )

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class SettingsPanel(ThemedOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("设置")
        self.setUseSignals(True)

        # 启用深色模式
        self.use_dark_mode = SingleSettingOption(self)
        self.use_dark_mode.setTitle("深色模式", "在深色主题的计算机上提供更佳的视觉效果")

        self.button_use_dark_mode = SiSwitch(self)
        self.button_use_dark_mode.setFixedHeight(32)
        self.button_use_dark_mode.toggled.connect(load_colors)
        self.button_use_dark_mode.toggled.connect(
            lambda b: SiGlobal.todo_list.settings_parser.modify("USE_DARK_MODE", b))
        self.button_use_dark_mode.setChecked(SiGlobal.todo_list.settings_parser.options["USE_DARK_MODE"])

        self.use_dark_mode.addWidget(self.button_use_dark_mode)
        self.use_dark_mode.addPlaceholder(16)

        # 锁定位置
        self.fix_position = SingleSettingOption(self)
        self.fix_position.setTitle("锁定位置", "阻止拖动窗口以保持位置不变")

        self.button_fix_position = SiSwitch(self)
        self.button_fix_position.setFixedHeight(32)
        self.button_fix_position.toggled.connect(lock_position)
        self.button_fix_position.toggled.connect(
            lambda b: SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION", b))
        self.button_fix_position.setChecked(SiGlobal.todo_list.settings_parser.options["FIXED_POSITION"])

        self.fix_position.addWidget(self.button_fix_position)
        self.fix_position.addPlaceholder(16)

        # 第三方资源
        self.third_party_res = SingleSettingOption(self)
        self.third_party_res.setTitle("第三方资源", "本项目使用了 FlatIcon 提供的图标")

        self.button_to_flaticon = SiSimpleButton(self)
        self.button_to_flaticon.setFixedHeight(32)
        self.button_to_flaticon.attachment().setText("前往 FlatIcon")
        self.button_to_flaticon.clicked.connect(lambda: os.system("start https://flaticon.com/"))
        self.button_to_flaticon.adjustSize()

        self.third_party_res.addWidget(self.button_to_flaticon)
        self.third_party_res.addPlaceholder(16)

        # 许可
        self.license = SingleSettingOption(self)
        self.license.setTitle("开源许可证", "本项目采用 GNU General Public License v3.0")

        self.button_license = SiSimpleButton(self)
        self.button_license.setFixedHeight(32)
        self.button_license.attachment().setText("在 Github 上查看")
        self.button_license.clicked.connect(
            lambda: os.system("start https://github.com/ChinaIceF/My-TODOs/blob/main/LICENSE"))
        self.button_license.adjustSize()

        self.license.addWidget(self.button_license)
        self.license.addPlaceholder(16)

        # 关于
        self.about = SingleSettingOption(self)
        self.about.setTitle("关于此软件", "制作者 霏泠Ice 保留所有权利")

        about_button_set = SiDenseHContainer(self)
        about_button_set.setFixedHeight(32)

        self.button_github = SiSimpleButton(self)
        self.button_github.setFixedHeight(32)
        self.button_github.attachment().setText("Github 主页")
        self.button_github.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF"))
        self.button_github.adjustSize()

        self.button_bilibili = SiSimpleButton(self)
        self.button_bilibili.setFixedHeight(32)
        self.button_bilibili.attachment().setText("哔哩哔哩 主页")
        self.button_bilibili.clicked.connect(lambda: os.system("start https://space.bilibili.com/390832893"))
        self.button_bilibili.adjustSize()

        about_button_set.addWidget(self.button_github)
        about_button_set.addWidget(self.button_bilibili)

        self.about.addWidget(about_button_set)
        self.about.addPlaceholder(16)

        # 赞助
        self.donation = SingleSettingOption(self)
        self.donation.setTitle("赞助作者", "为爱发电，您的支持是我最大的动力")

        self.button_donation = SiSimpleButton(self)
        self.button_donation.setFixedHeight(32)
        self.button_donation.attachment().setText("在 Github 上扫码赞助")
        self.button_donation.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF/My-TODOs?tab=readme-ov-file#%E8%B5%9E%E5%8A%A9"))
        self.button_donation.adjustSize()

        self.donation.addWidget(self.button_donation)
        self.donation.addPlaceholder(16)

        # SiliconUI
        self.silicon_ui = SiDenseVContainer(self)
        self.silicon_ui.setAlignment(Qt.AlignCenter)

        self.button_silicon_ui = SiSimpleButton(self)
        self.button_silicon_ui.attachment().setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.button_silicon_ui.attachment().setText("基于 PyQt-SiliconUI 编写")
        self.button_silicon_ui.adjustSize()
        self.button_silicon_ui.clicked.connect(lambda: os.system("start https://github.com/ChinaIceF/PyQt-SiliconUI"))

        self.silicon_ui.addWidget(self.button_silicon_ui)

        # 添加到body
        self.body().setAdjustWidgetsSize(True)
        self.body().addWidget(self.use_dark_mode)
        self.body().addWidget(self.fix_position)
        self.body().addWidget(self.third_party_res)
        self.body().addWidget(self.license)
        self.body().addWidget(self.about)
        self.body().addWidget(self.donation)
        self.body().addWidget(self.silicon_ui)
        self.body().addPlaceholder(16)

    def reloadStyleSheet(self):
        self.setThemeColor(SiGlobal.siui.colors["PANEL_THEME"])
        super().reloadStyleSheet()

        self.button_to_flaticon.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_license.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_github.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_bilibili.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_donation.setColor(SiGlobal.siui.colors["SIMPLE_BUTTON_BG"])
        self.button_silicon_ui.attachment().setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_E"]))

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class TODOApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 窗口周围留白，供阴影使用
        self.padding = 48
        self.anchor = QPoint(self.x(), self.y())
        self.fixed_position = QPoint(SiGlobal.todo_list.settings_parser.options["FIXED_POSITION_X"],
                                     SiGlobal.todo_list.settings_parser.options["FIXED_POSITION_Y"])

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 初始化全局变量
        SiGlobal.todo_list.todo_list_unfold_state = True
        SiGlobal.todo_list.add_todo_unfold_state = False

        # 初始化工具提示窗口
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        SiGlobal.siui.windows["MAIN_WINDOW"] = self

        # 创建移动动画
        self.move_animation = SiExpAnimation(self)
        self.move_animation.setFactor(1 / 4)
        self.move_animation.setBias(1)
        self.move_animation.setCurrent([self.x(), self.y()])
        self.move_animation.ticked.connect(self._onMoveAnimationTicked)

        # 创建垂直容器
        self.container_v = SiDenseVContainer(self)
        self.container_v.setFixedWidth(500)
        self.container_v.setSpacing(0)
        self.container_v.setAlignment(Qt.AlignCenter)

        # 构建界面
        # 头
        self.header_panel = AppHeaderPanel(self)
        self.header_panel.setFixedWidth(500 - 2 * self.padding)
        self.header_panel.setFixedHeight(48 + 12)

        # 设置面板
        self.settings_panel = SettingsPanel(self)
        self.settings_panel.setFixedWidth(500 - 2 * self.padding)
        self.settings_panel.adjustSize()

        self.settings_panel_placeholder = SiLabel(self)
        self.settings_panel_placeholder.setFixedHeight(12)
        self._onSettingsButtonToggled(False)

        # 添加新待办面板
        self.add_todo_panel = AddNewTODOPanel(self)
        self.add_todo_panel.setFixedWidth(500 - 2 * self.padding)
        self.add_todo_panel.adjustSize()

        self.add_todo_panel_placeholder = SiLabel(self)
        self.add_todo_panel_placeholder.setFixedHeight(12)
        self._onAddTODOButtonToggled(False)

        # 全部待办面板
        self.todo_list_panel = TODOListPanel(self)
        self.todo_list_panel.setFixedWidth(500 - 2 * self.padding)

        self.todo_list_panel_placeholder = SiLabel(self)
        self.todo_list_panel_placeholder.setFixedHeight(12)
        self._onShowTODOButtonToggled(True)

        # <- 添加到垂直容器
        self.container_v.addWidget(self.header_panel)
        self.container_v.addWidget(self.settings_panel)
        self.container_v.addWidget(self.settings_panel_placeholder)
        self.container_v.addWidget(self.add_todo_panel)
        self.container_v.addWidget(self.add_todo_panel_placeholder)
        self.container_v.addWidget(self.todo_list_panel)
        self.container_v.addWidget(self.todo_list_panel_placeholder)

        # 绑定界面信号
        self.header_panel.unfold_button.toggled.connect(self._onShowTODOButtonToggled)
        self.header_panel.add_todo_button.toggled.connect(self._onAddTODOButtonToggled)
        self.header_panel.settings_button.toggled.connect(self._onSettingsButtonToggled)

        self.settings_panel.resized.connect(self._onTODOWindowResized)
        self.add_todo_panel.resized.connect(self._onTODOWindowResized)
        self.todo_list_panel.resized.connect(self._onTODOWindowResized)

        self.add_todo_panel.confirm_button.clicked.connect(self._onAddTODOConfirmButtonClicked)
        self.add_todo_panel.cancel_button.clicked.connect(self._onAddTODOCancelButtonClicked)

        self.todo_list_panel.todoAmountChanged.connect(self._onTODOAmountChanged)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(48)
        self.setGraphicsEffect(shadow)

        self.resize(500, 800)
        self.move(self.fixed_position.x(), self.fixed_position.y())
        SiGlobal.siui.reloadAllWindowsStyleSheet()

        # 读取 todos.ini 添加到待办
        for todo in SiGlobal.todo_list.todos_parser.todos:
            self.todo_list_panel.addTODO(todo)


    def adjustSize(self):
        h = (self.header_panel.height() + 12 +
             self.settings_panel.height() + 12 +
             self.add_todo_panel.height() + 12 +
             self.todo_list_panel.height() +
             2 * self.padding)
        self.resize(self.width(), h)
        self.container_v.adjustSize()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.container_v.move(0, self.padding)

    def showEvent(self, a0):
        super().showEvent(a0)

    def _onTODOWindowResized(self, size):
        w, h = size
        self.adjustSize()

    def _onShowTODOButtonToggled(self, state):
        if state is True:
            self.todo_list_panel_placeholder.setFixedHeight(12)
            self.todo_list_panel.adjustSize()
        else:
            self.todo_list_panel_placeholder.setFixedHeight(0)
            self.todo_list_panel.resize(self.todo_list_panel.width(), 0)

    def _onAddTODOButtonToggled(self, state):
        if state is True:
            self.add_todo_panel_placeholder.setFixedHeight(12)
            self.add_todo_panel.adjustSize()
        else:
            self.add_todo_panel_placeholder.setFixedHeight(0)
            self.add_todo_panel.resize(self.add_todo_panel.width(), 0)

    def _onSettingsButtonToggled(self, state):
        if state is True:
            self.settings_panel_placeholder.setFixedHeight(12)
            self.settings_panel.adjustSize()
        else:
            self.settings_panel_placeholder.setFixedHeight(0)
            self.settings_panel.resize(self.settings_panel.width(), 0)

    def _onTODOAmountChanged(self, amount):
        if amount == 0:
            self.header_panel.unfold_button.attachment().setText("没有待办")
        else:
            self.header_panel.unfold_button.attachment().setText(f"{amount}个待办事项")
        self.header_panel.unfold_button.adjustSize()

    def _onAddTODOConfirmButtonClicked(self):
        text = self.add_todo_panel.text_edit.toPlainText()
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

        while text[-1:] == "\n":
            text = text[:-1]

        if text == "":
            return

        self.todo_list_panel.addTODO(text)

    def _onAddTODOCancelButtonClicked(self):
        self.add_todo_panel.text_edit.setText("")
        self.header_panel.add_todo_button.setChecked(False)

    def moveTo(self, x, y):
        self.move_animation.setTarget([x, y])
        self.move_animation.try_to_start()

    def moveEvent(self, a0):
        super().moveEvent(a0)
        x, y = a0.pos().x(), a0.pos().y()
        self.move_animation.setCurrent([x, y])

    def _onMoveAnimationTicked(self, pos):
        self.move(int(pos[0]), int(pos[1]))
        if SiGlobal.todo_list.position_locked is False:
            self.fixed_position = self.pos()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return

        new_pos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        x, y = new_pos.x(), new_pos.y()

        self.moveTo(x, y)

    def mouseReleaseEvent(self, a0):
        if SiGlobal.todo_list.position_locked is True:
            self.moveTo(self.fixed_position.x(), self.fixed_position.y())

    def closeEvent(self, a0):
        super().closeEvent(a0)

        # 获取当前待办，并写入 todos.ini
        todos = [widget.text_label.text() for widget in self.todo_list_panel.body().widgets_top]
        SiGlobal.todo_list.todos_parser.todos = todos
        SiGlobal.todo_list.todos_parser.write()

        # 写入设置到 options.ini
        SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_X", self.fixed_position.x())
        SiGlobal.todo_list.settings_parser.modify("FIXED_POSITION_Y", self.fixed_position.y())
        SiGlobal.todo_list.settings_parser.write()
