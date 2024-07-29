from siui.components.menu.abstracts import ABCSiMenu
from siui.components.menu.option import SiMenuOption


class SiMenu(ABCSiMenu):
    def addOption(self,
                  text: str,
                  value=None,
                  icon=None,
                  child_menu=None):
        new_option = SiMenuOption(self, child_menu, text, value=value, icon=icon)
        new_option.setSelectable(self.is_selection_menu)
        new_option.setFixedHeight(32)

        self.body().addWidget(new_option)
        self.options_.append(new_option)
