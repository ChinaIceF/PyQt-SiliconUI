from siui.components.menu.abstracts import ABCSiMenu, ABCSiMenuOption
from siui.components.widgets.button import SiSimpleButton


class SiMenuOption(ABCSiMenuOption):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = SiSimpleButton(self)
        self.button.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.parentMenu().setIndex(self.parentMenu().options().index(self))
        self.parentMenu().close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.button.resize(event.size())

class SiMenu(ABCSiMenu):
    def addOption(self,
                  text: str,
                  icon: str = None,
                  child_menu=None):
        new_option = SiMenuOption(self, child_menu, text, icon)
        new_option.setFixedHeight(32)
        self.body().addWidget(new_option)
        self.options_.append(new_option)
