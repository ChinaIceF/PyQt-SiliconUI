import sys

from PyQt5.QtWidgets import QApplication
from ui import TODOApplication

import siui

#siui.gui.set_scale_factor(2)
siui.core.globals.SiGlobal.siui.colors["SVG_COLOR_A"] = "#E8E2EE"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TODOApplication()
    window.show()
    sys.exit(app.exec_())
