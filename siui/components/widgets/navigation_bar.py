from PyQt5.QtCore import Qt

from siui.components import SiDenseHContainer, SiLabel, SiSimpleButton, SiWidget, SiDenseVContainer
from siui.components.widgets.abstracts.navigation_bar import ABCSiNavigationBar
from siui.core import SiColor


class SiNavigationBarH(ABCSiNavigationBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_dict = {}
        self.is_no_indicator = False

        self.item_container = SiDenseHContainer(self)
        self.item_container.setFixedHeight(32)
        self.item_container.setSpacing(2)

        self.indicator_frame = SiWidget(self)
        self.indicator_frame.setFixedHeight(6)

        self.indicator_track = SiLabel(self.indicator_frame)
        self.indicator_track.setFixedHeight(2)
        self.indicator_track.move(0, 2)
        self.indicator_track.setFixedStyleSheet("border-radius: 1px")

        self.indicator = SiLabel(self.indicator_frame)
        self.indicator.setFixedHeight(6)
        self.indicator.resize(32, 6)
        self.indicator.setFixedStyleSheet("border-radius: 3px")

        self.indexChanged.connect(self._on_index_changed)

    def container(self):
        return self.item_container

    def indicatorFrame(self):
        return self.indicator_frame

    def setNoIndicator(self, state):
        self.is_no_indicator = state
        self.indicatorFrame().setVisible(not state)

    def adjustSize(self):
        min_height = 32 + 4 * int(not self.is_no_indicator)
        self.resize(self.container().width(), max(self.height(), min_height))

    def addItem(self, name, side="left"):
        new_index = self.maximumIndex() + 1

        def on_clicked():
            self._on_button_clicked(new_index)

        button = SiSimpleButton(self)
        button.attachment().setText(name)
        button.colorGroup().assign(SiColor.TEXT_B, self.getColor(SiColor.BUTTON_TEXT_BUTTON_IDLE))
        button.adjustSize()
        button.clicked.connect(on_clicked)

        self.item_container.addWidget(button, side)
        self.item_dict[str(new_index)] = button
        self.setMaximumIndex(new_index)

    def _on_button_clicked(self, index):
        self.setCurrentIndex(index)

    def _on_index_changed(self, index):
        for btn in self.item_dict.values():
            btn.attachment().setTextColor(self.getColor(SiColor.BUTTON_TEXT_BUTTON_IDLE))

        button = self.item_dict[str(index)]
        button.attachment().setTextColor(self.getColor(SiColor.TEXT_B))

        width = int(button.width() * 0.618)
        x = button.x() + (button.width() - width) // 2

        self.indicator.moveTo(x, self.indicator.y())
        self.indicator.resizeTo(width, self.indicator.height())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.indicator_track.setColor(self.getColor(SiColor.THEME))
        self.indicator.setColor(self.getColor(SiColor.THEME))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator_frame.setGeometry(0, event.size().height() - self.indicator_frame.height(),
                                         event.size().width(), self.indicator_frame.height())
        self.indicator_track.resize(event.size().width(), 2)

    def showEvent(self, a0):
        super().showEvent(a0)
        button = self.item_dict[str(self.currentIndex())]
        button.attachment().setTextColor(self.getColor(SiColor.TEXT_B))


class SiNavigationBarV(ABCSiNavigationBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_dict = {}
        self.is_no_indicator = False

        self.item_container = SiDenseVContainer(self)
        self.item_container.setAlignment(Qt.AlignRight)
        self.item_container.setSpacing(2)

        self.indicator_frame = SiWidget(self)
        self.indicator_frame.setFixedWidth(6)

        self.indicator_track = SiLabel(self.indicator_frame)
        self.indicator_track.setFixedWidth(2)
        self.indicator_track.move(2, 0)
        self.indicator_track.setFixedStyleSheet("border-radius: 1px")

        self.indicator = SiLabel(self.indicator_frame)
        self.indicator.setFixedWidth(6)
        self.indicator.resize(6, 32)
        self.indicator.setFixedStyleSheet("border-radius: 3px")

        self.indexChanged.connect(self._on_index_changed)

    def container(self):
        return self.item_container

    def indicatorFrame(self):
        return self.indicator_frame

    def setNoIndicator(self, state):
        self.is_no_indicator = state
        self.indicatorFrame().setVisible(not state)

    def adjustSize(self):
        self.container().adjustSize()
        min_width = self.container().width() + 6 * int(not self.is_no_indicator)
        self.resize(max(self.container().width() + 6, min_width), self.container().height())

    def addItem(self, name, side="top"):
        new_index = self.maximumIndex() + 1

        def on_clicked():
            self._on_button_clicked(new_index)

        button = SiSimpleButton(self)
        button.attachment().setText(name)
        button.colorGroup().assign(SiColor.TEXT_B, self.getColor(SiColor.BUTTON_TEXT_BUTTON_IDLE))
        button.adjustSize()
        button.clicked.connect(on_clicked)

        self.item_container.addWidget(button, side)
        self.item_dict[str(new_index)] = button
        self.setMaximumIndex(new_index)

    def _on_button_clicked(self, index):
        self.setCurrentIndex(index)

    def _on_index_changed(self, index):
        for btn in self.item_dict.values():
            btn.attachment().setTextColor(self.getColor(SiColor.BUTTON_TEXT_BUTTON_IDLE))

        button = self.item_dict[str(index)]
        button.attachment().setTextColor(self.getColor(SiColor.TEXT_B))

        height = int(button.height() * (1-0.618)*2)
        y = button.y() + (button.height() - height) // 2

        self.indicator.moveTo(self.indicator.x(), y)
        self.indicator.resizeTo(self.indicator.width(), height)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.indicator_track.setColor(self.getColor(SiColor.THEME))
        self.indicator.setColor(self.getColor(SiColor.THEME))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator_frame.setGeometry(event.size().width() - self.indicator_frame.width(), 0,
                                         self.indicator_frame.width(), event.size().height())
        self.indicator_track.resize(2, event.size().height())

    def showEvent(self, a0):
        super().showEvent(a0)
        button = self.item_dict[str(self.currentIndex())]
        button.attachment().setTextColor(self.getColor(SiColor.TEXT_B))
