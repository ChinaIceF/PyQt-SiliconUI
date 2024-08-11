from siui.components import SiLabel, SiWidget
from siui.components.widgets.abstracts.navigation_bar import ABCSiNavigationBar
from siui.core.color import SiColor


class SiNavigationBarH(ABCSiNavigationBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.indicator_track.setColor(self.colorGroup().fromToken(SiColor.THEME))
        self.indicator.setColor(self.colorGroup().fromToken(SiColor.THEME))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator_frame.setGeometry(0, event.size().height() - self.indicator_frame.height(),
                                         event.size().width(), self.indicator_frame.height())
        self.indicator_track.resize(event.size().width(), 2)
