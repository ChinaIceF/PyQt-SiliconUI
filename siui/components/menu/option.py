from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtWidgets import QAction

from siui.components.widgets.button import SiSimpleButton
from siui.components.widgets.container import SiDenseHContainer
from siui.components.widgets.label import SiLabel, SiSvgLabel
from siui.core import SiColor
from siui.core import Si


class OptionButton(SiSimpleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option_ = None
        self.hover_timer = QTimer()
        self.hover_timer.setInterval(500)
        self.hover_timer.setSingleShot(True)

    def setOption(self, option):
        self.option_ = option
        self.hover_timer.timeout.connect(self.option_.on_hover_timeout)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_timer.start()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.hover_timer.stop()


class SiMenuOption(SiDenseHContainer):
    def __init__(self,
                 parent_menu,
                 child_menu,
                 text: str,
                 value=None,
                 icon=None):
        super().__init__(parent_menu)  # parent will be overwritten when added to container

        self.value_ = text if value is None else value
        self.text_ = text
        self.parent_menu = parent_menu
        self.child_menu = child_menu
        if self.child_menu is not None:
            self.child_menu.setWakenOption(self)

        self.is_selectable = True
        self.is_selected = False

        self.setSpacing(0)
        self.setFixedHeight(32)
        self.setAlignment(Qt.AlignCenter)

        self.chosen_indicator = SiLabel(self)
        self.chosen_indicator.setFixedSize(4, 20)
        self.chosen_indicator.setFixedStyleSheet("border-radius: 2px")
        self.chosen_indicator.setVisible(False)

        self.icon = SiSvgLabel(self)
        self.icon.resize(32, 32)
        self.icon.setSvgSize(16, 16)
        if icon is not None:
            self.icon.load(icon)

        self.text_label = SiLabel(self)
        self.text_label.setFixedHeight(32)
        self.text_label.setText(text)
        self.text_label.setAlignment(Qt.AlignVCenter)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

        self.has_child_menu_indicator = SiSvgLabel(self)
        self.has_child_menu_indicator.resize(24, 32)
        self.has_child_menu_indicator.setSvgSize(16, 16)

        self.addWidget(self.chosen_indicator)
        self.addPlaceholder(4)
        self.addWidget(self.icon)
        self.addPlaceholder(3)
        self.addWidget(self.text_label)
        self.addWidget(self.has_child_menu_indicator, side="right")

        self.button = OptionButton(self)
        self.button.setOption(self)
        self.button.clicked.connect(self.on_clicked)

    def parentMenu(self):
        """
        Get the parent menu of this option
        :return: parent menu
        """
        return self.parent_menu

    def setSelectable(self, state):
        """
        set whether this option is selectable or not
        """
        if state is False:
            self.setSelected(False)
        self.is_selectable = state

    def setSelected(self,
                    state: bool,
                    has_signal: bool = True):
        """
        Set the select state of this option
        """
        if self.is_selectable is False:
            return

        self.is_selected = state
        self.chosen_indicator.setVisible(state)
        if (has_signal is True) and (state is True):
            self.parentMenu().indexChanged.emit(self.parentMenu().options().index(self))
            self.parentMenu().valueChanged.emit(self.value())

        if state is True:
            for option in self.parentMenu().options():
                if option != self:
                    option.setSelected(False)

    def isSelected(self):
        """
        Get the select state of this option
        :return: select state
        """
        return self.is_selected

    def setValue(self, value):
        self.value_ = value

    def value(self):
        return self.value_

    def text(self):
        return self.text_

    def setShowIcon(self, state):
        if state:
            self.icon.resize(32, 32)
        else:
            self.icon.resize(0, 32)
        self.arrangeWidget()

    def on_clicked(self):
        self.parentMenu().setIndex(self.parentMenu().options().index(self))
        if self.child_menu is None:
            self.parentMenu().recursiveClose()
        else:
            self.button.hover_timer.stop()
            self.on_hover_timeout()

    def on_hover_timeout(self):
        # close parent's all children menu
        for option in self.parentMenu().options():
            if option.child_menu is not None:
                option.child_menu.close()

        # show this option's child menu
        if self.child_menu is not None:
            map_pos = self.mapToGlobal(QPoint(0, 0))
            self.child_menu.unfold(map_pos.x() + self.width(), map_pos.y())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.chosen_indicator.setColor(self.getColor(SiColor.THEME))
        self.text_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")

        if self.child_menu is not None:
            svg_arrow = ('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Outline" '
                         'viewBox="0 0 24 24" width="512" height="512"><path d="M15.4,9.88,10.81,5.29a1,1,0,0,0-1.41,0,'
                         '1,1,0,0,0,0,1.42L14,11.29a1,1,0,0,1,0,1.42L9.4,17.29a1,1,0,0,0,1.41,1.42l4.59-4.59A3,3,0,0,0,'
                         f'15.4,9.88Z" fill="{self.getColor(SiColor.SVG_NORMAL)}" /></svg>')
            self.has_child_menu_indicator.load(svg_arrow.encode())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.button.resize(event.size())

    def focusOutEvent(self, ev):
        super().focusOutEvent(ev)
        self.close()