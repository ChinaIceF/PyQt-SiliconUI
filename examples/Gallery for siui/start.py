import sys

from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp

import siui

# siui.gui.set_scale_factor(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    sys.exit(app.exec_())
