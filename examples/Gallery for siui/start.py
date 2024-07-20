import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from ui import MySiliconApp

sys.path.append(str(Path().cwd()))

import siui

siui.gui.set_scale_factor(1)

if __name__ == "__main__":
    app = QApplication()
    window = MySiliconApp()
    window.show()
    app.exec()
