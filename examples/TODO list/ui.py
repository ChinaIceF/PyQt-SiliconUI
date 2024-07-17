
from components import ThemedOptionCardPlane
from icons import IconDictionary
from PyQt5.Qt import QColor, QPoint
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QTextEdit

from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
    SiSvgLabel,
    SiToggleButton,
)
from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.core.globals import NewGlobal, SiGlobal
from siui.gui.tooltip import ToolTipWindow

# 创建删除队列
SiGlobal.todo_list = NewGlobal()
SiGlobal.todo_list.delete_pile = []

# 加载图标
SiGlobal.siui.icons.update(IconDictionary(color="#E8E2EE").icons)


class SingleTODOOption(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setShrinking(True)

        self.getAnimationGroup().fromToken("opacity").setFactor(1 / 32)
        self.getAnimationGroup().fromToken("opacity").setBias(0.01)

        self.check_box = SiCheckBox(self)
        self.check_box.resize(12, 12)
        self.check_box.setText(" ")
        self.check_box.toggled.connect(self._onChecked)

        self.text_label = SiLabel(self)
        self.text_label.resize(500-48-48-32, 32)
        self.text_label.setWordWrap(True)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setStyleSheet(
            "padding-top: 2px; padding-bottom: 2px; color: {}".format(SiGlobal.siui.colors["THEME"]))

        self.addWidget(self.check_box)
        self.addWidget(self.text_label)

        self.move = self.moveTo

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
        self.container_h.setAlignCenter(True)
        self.container_h.setFixedHeight(48)
        self.container_h.setSpacing(0)

        self.icon = SiSvgLabel(self)
        self.icon.resize(32, 32)
        self.icon.setSvgSize(16, 16)
        self.icon.load(
            '<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M0,8v-1C0,4.243,2.243,2,5,2h1V1c0-.552,.447-1,1-1s1,.448,1,1v1h8V1c0-.552,.447-1,1-1s1,.448,1,1v1h1c2.757,0,5,2.243,5,5v1H0Zm24,2v9c0,2.757-2.243,5-5,5H5c-2.757,0-5-2.243-5-5V10H24Zm-6.168,3.152c-.384-.397-1.016-.409-1.414-.026l-4.754,4.582c-.376,.376-1.007,.404-1.439-.026l-2.278-2.117c-.403-.375-1.035-.354-1.413,.052-.376,.404-.353,1.037,.052,1.413l2.252,2.092c.566,.567,1.32,.879,2.121,.879s1.556-.312,2.108-.866l4.74-4.568c.397-.383,.409-1.017,.025-1.414Z" fill="#e1d9e8" /></svg>'.encode())

        self.unfold_button = SiToggleButton(self)
        self.unfold_button.setFixedHeight(32)
        self.unfold_button.setStateColor(Color.transparency(SiGlobal.siui.colors["THEME"], 0),
                                         Color.transparency(SiGlobal.siui.colors["THEME"], 0.1))
        self.unfold_button.attachment().setText("0个待办事项")
        self.unfold_button.setChecked(True)

        self.options_button = SiSimpleButton(self)
        self.options_button.resize(32, 32)
        self.options_button.attachment().load(SiGlobal.siui.icons["fi-rr-menu-burger"])
        self.options_button.setHint("设置")

        self.add_todo_button = SiToggleButton(self)
        self.add_todo_button.resize(32, 32)
        self.add_todo_button.setStateColor(Color.transparency(SiGlobal.siui.colors["THEME"], 0),
                                           Color.transparency(SiGlobal.siui.colors["THEME"], 0.1))
        self.add_todo_button.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        self.add_todo_button.setHint("添加新代办")
        self.add_todo_button.setChecked(False)

        self.container_h.addPlaceholder(16)
        self.container_h.addWidget(self.icon)
        self.container_h.addPlaceholder(4)
        self.container_h.addWidget(self.unfold_button)

        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.options_button, "right")
        self.container_h.addPlaceholder(16, "right")
        self.container_h.addWidget(self.add_todo_button, "right")

        # 按钮加入全局变量
        SiGlobal.todo_list.todo_list_unfold_button = self.unfold_button
        SiGlobal.todo_list.add_todo_unfold_button = self.add_todo_button

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size().width(), 48)
        self.container_h.resize(event.size().width(), 48)

    def reloadStyleSheet(self):
        self.background_label.setStyleSheet("background-color: {}; border: 1px solid {}".format(
            SiGlobal.siui.colors["BACKGROUND_COLOR"], SiGlobal.siui.colors["BORDER_COLOR"]
        ))
        self.unfold_button.setStyleSheet("color: {}".format(SiGlobal.siui.colors["THEME"]))


class TODOListPanel(ThemedOptionCardPlane):
    todoAmountChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("background-color: transparent")

        self.setThemeColor(SiGlobal.siui.colors["THEME"])
        self.setTitle("全部待办")
        self.setUseSignals(True)

        self.no_todo_label = SiLabel(self)
        self.no_todo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.no_todo_label.setAutoAdjustSize(True)
        self.no_todo_label.setText("当前没有待办哦")
        self.no_todo_label.setAlignment(Qt.AlignCenter)
        self.no_todo_label.setStyleSheet("color: {}".format(Color.transparency(SiGlobal.siui.colors["THEME"], 0.5)))
        self.no_todo_label.hide()

        self.body().setUseMoveTo(False)
        self.body().setShrinking(True)
        self.body().setAdjustWidgetsSize(True)

        self.footer().setFixedHeight(64)
        self.footer().setSpacing(8)
        self.footer().setAlignCenter(True)

        self.complete_all_button = SiSimpleButton(self)
        self.complete_all_button.resize(32, 32)
        self.complete_all_button.attachment().load(SiGlobal.siui.icons["fi-rr-list-check"])
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
        super().reloadStyleSheet()

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

        self.setStyleSheet("background-color: transparent")

        self.setThemeColor(SiGlobal.siui.colors["THEME"])
        self.setTitle("添加新待办")
        self.setUseSignals(True)

        self.confirm_button = SiSimpleButton(self)
        self.confirm_button.attachment().load(SiGlobal.siui.icons["fi-rr-check"])
        self.confirm_button.resize(32, 32)
        self.confirm_button.setHint("确认并添加")

        self.cancel_button = SiSimpleButton(self)
        self.cancel_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross"])
        self.cancel_button.resize(32, 32)
        self.cancel_button.setHint("取消")

        self.header().addWidget(self.cancel_button, "right")
        self.header().addWidget(self.confirm_button, "right")

        self.instruction = SiLabel(self)
        self.instruction.setStyleSheet("color: {}".format(SiGlobal.siui.colors["THEME"]))
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
        super().reloadStyleSheet()
        self.text_edit.setStyleSheet(
            """
            border: 1px solid {};
            background-color: {};
            border-radius: 4px;
            padding-left: 8px; padding-right: 8px; 
            color: {}
            """.format(SiGlobal.siui.colors["BORDER_COLOR"],
                       SiGlobal.siui.colors["INTERFACE_BG_A"],
                       SiGlobal.siui.colors["THEME"])
        )

    def showEvent(self, a0):
        super().showEvent(a0)
        self.setForceUseAnimations(True)


class TODOApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 窗口周围留白，供阴影使用
        self.padding = 48
        self.anchor = QPoint(self.x(), self.y())

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 初始化全局变量
        SiGlobal.todo_list.todo_list_unfold_state = True
        SiGlobal.todo_list.add_todo_unfold_state = False

        # 定义主题色
        SiGlobal.siui.colors["THEME"] = "#E8E2EE"
        SiGlobal.siui.colors["BACKGROUND_COLOR"] = "#252229"
        SiGlobal.siui.colors["BORDER_COLOR"] = "#3b373f"

        # 初始化工具提示窗口
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        SiGlobal.siui.windows["MAIN_WINDOW"] = self

        # 创建移动动画
        self.move_animation = SiExpAnimation(self)
        self.move_animation.setFactor(1/4)
        self.move_animation.setBias(1)
        self.move_animation.setCurrent([self.x(), self.y()])
        self.move_animation.ticked.connect(self._onMoveAnimationTicked)

        # 创建垂直容器
        self.container_v = SiDenseVContainer(self)
        self.container_v.setFixedWidth(500)
        self.container_v.setSpacing(0)
        self.container_v.setShrinking(True)
        self.container_v.setAlignCenter(True)

        # 构建界面
        # 头
        self.header_panel = AppHeaderPanel(self)
        self.header_panel.setFixedWidth(500-2*self.padding)
        self.header_panel.setFixedHeight(48 + 12)

        # 添加新待办面板
        self.add_todo_panel = AddNewTODOPanel(self)
        self.add_todo_panel.setFixedWidth(500-2*self.padding)
        self.add_todo_panel.adjustSize()

        self.add_todo_panel_placeholder = SiLabel(self)
        self.add_todo_panel_placeholder.setFixedHeight(12)

        # 全部待办面板
        self.todo_list_panel = TODOListPanel(self)
        self.todo_list_panel.setFixedWidth(500 - 2 * self.padding)
        self._onAddTODOButtonToggled(False)

        self.todo_list_panel_placeholder = SiLabel(self)
        self.todo_list_panel_placeholder.setFixedHeight(12)

        # <- 添加到垂直容器
        self.container_v.addWidget(self.header_panel)
        self.container_v.addWidget(self.add_todo_panel)
        self.container_v.addWidget(self.add_todo_panel_placeholder)
        self.container_v.addWidget(self.todo_list_panel)
        self.container_v.addWidget(self.todo_list_panel_placeholder)

        # 绑定界面信号
        self.header_panel.unfold_button.toggled.connect(self._onShowTODOButtonToggled)
        self.header_panel.add_todo_button.toggled.connect(self._onAddTODOButtonToggled)

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
        self.moveTo(64, 64)

    def adjustSize(self):
        h = (self.header_panel.height() + 12 +
             self.add_todo_panel.height() + 12 +
             self.todo_list_panel.height() +
             2 * self.padding)
        self.resize(self.width(), h)
        self.container_v.adjustSize()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        size = a0.size()
        self.container_v.move(0, self.padding)

    def showEvent(self, a0):
        super().showEvent(a0)
        SiGlobal.siui.reloadAllWindowsStyleSheet()

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

    def _onMoveAnimationTicked(self, pos):
        self.move(int(pos[0]), int(pos[1]))

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
