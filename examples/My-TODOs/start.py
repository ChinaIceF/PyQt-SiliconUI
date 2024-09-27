import sys
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MySiliconApp()
    window.show()

    sys.exit(app.exec_())
