from siui.components import SiDenseHContainer, SiLabel, SiSimpleButton, SiWidget
from siui.components.widgets.abstracts.navigation_bar import ABCSiNavigationBar
from siui.core.color import SiColor


class SiNavigationBarH(ABCSiNavigationBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_dict = {}

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

    def adjustSize(self):
        self.resize(self.container().width(), max(self.height(), 36))

    def addItem(self, name, side="left"):
        new_index = self.maximumIndex() + 1

        def on_clicked():
            self._on_button_clicked(new_index)

        button = SiSimpleButton(self)
        button.attachment().setText(name)
        button.colorGroup().assign(SiColor.TEXT_B, self.colorGroup().fromToken(SiColor.BUTTON_TEXT_BUTTON_IDLE))
        button.adjustSize()
        button.clicked.connect(on_clicked)

        self.item_container.addWidget(button, side)
        self.item_dict[str(new_index)] = button
        self.setMaximumIndex(new_index)

    def _on_button_clicked(self, index):
        self.setCurrentIndex(index)

    def _on_index_changed(self, index):
        for btn in self.item_dict.values():
            btn.attachment().setTextColor(self.colorGroup().fromToken(SiColor.BUTTON_TEXT_BUTTON_IDLE))

        button = self.item_dict[str(index)]
        button.attachment().setTextColor(self.colorGroup().fromToken(SiColor.TEXT_B))

        width = int(button.width() * (1-0.618)*2)
        x = button.x() + (button.width() - width) // 2

        self.indicator.moveTo(x, self.indicator.y())
        self.indicator.resizeTo(width, self.indicator.height())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.indicator_track.setColor(self.colorGroup().fromToken(SiColor.THEME))
        self.indicator.setColor(self.colorGroup().fromToken(SiColor.THEME))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator_frame.setGeometry(0, event.size().height() - self.indicator_frame.height(),
                                         event.size().width(), self.indicator_frame.height())
        self.indicator_track.resize(event.size().width(), 2)

    def showEvent(self, a0):
        super().showEvent(a0)
        button = self.item_dict[str(self.currentIndex())]
        button.attachment().setTextColor(self.colorGroup().fromToken(SiColor.TEXT_B))
