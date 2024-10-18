from siui.components import SiLabel, SiMasonryContainer, SiSvgLabel, SiWidget
from siui.core import SiColor, SiGlobal


class SiTimeLineItem(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = SiSvgLabel(self)
        self.icon.setSvgSize(24, 24)
        self.icon.setFixedSize(32, 32)
        self.icon.load(SiGlobal.siui.iconpack.get(
            "ic_fluent_warning_shield_filled", color_code=self.getColor(SiColor.PROGRESS_BAR_COMPLETING)))
        self.icon.move(16, 16)

        self.anchor = SiLabel(self)
        self.anchor.setFixedSize(24, 24)
        self.anchor.setFixedStyleSheet("border-radius: 12px")
        self.anchor.setStyleSheet(
            f"border: 4px solid {self.colorGroup().fromToken(SiColor.INTERFACE_BG_C)};"
            f"background-color: {self.colorGroup().fromToken(SiColor.INTERFACE_BG_E)};"
        )
        self.anchor.move(64 + 4, 20)

        self.anchor_dot = SiLabel(self.anchor)
        self.anchor_dot.setFixedSize(8, 8)
        self.anchor_dot.setFixedStyleSheet("border-radius: 4px")
        self.anchor_dot.move(8, 8)
        self.anchor_dot.setStyleSheet(
            f"background-color: {self.colorGroup().fromToken(SiColor.INTERFACE_BG_C)};"
        )

        self.title = SiLabel(self)
        # self.title.setTextColor(self.colorGroup().fromToken(SiColor))
        self.title.setText("你好世界")
        self.title.move(0, 0)
        self.title.adjustSize()

        self.description = SiLabel(self)
        self.description.setText("这是一段解释")
        self.description.move(100, self.title.height())
        self.description.adjustSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        print(event.size().width())
        self.title.resize(event.size().width() - 100, self.title.height())
        self.description.resize(event.size().width() - 100, self.description.height())
        self.description.move(100, self.title.height())


class SiTimeLine(SiMasonryContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumns(1)
        self.setColumnWidth(500)

        self.track = SiLabel(self)
        self.track.setFixedStyleSheet("border-radius: 2px")
        self.track.setColor(self.colorGroup().fromToken(SiColor.INTERFACE_BG_E))
        self.track.setFixedWidth(4)
        self.track.resize(4, 100)
        self.track.move(14 + 64, 0)

        self.item1 = SiTimeLineItem(self)
        self.item2 = SiTimeLineItem(self)

        self.addWidget(self.item1)
        self.addWidget(self.item2)
        # self.arrangeWidgets()

        self.setMinimumWidth(500)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        for item in self.widgets():
            item.resize(event.size().width(), item.height())
