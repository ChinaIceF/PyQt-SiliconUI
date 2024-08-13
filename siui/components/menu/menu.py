from siui.components.menu.abstracts import ABCSiMenu, AnimationManager
from siui.components.menu.option import SiMenuOption


class SiMenu(ABCSiMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAnimationManager(AnimationManager.PULL_DOWN)

    def addOption(self,
                  text: str,
                  value=None,
                  icon=None,
                  child_menu=None):
        new_option = SiMenuOption(self, child_menu, text, value=value, icon=icon)
        new_option.setSelectable(self.is_selection_menu)
        new_option.setFixedHeight(32)

        self.options_.append(new_option)
        self.body().addWidget(new_option)
        self.body().arrangeWidget()

