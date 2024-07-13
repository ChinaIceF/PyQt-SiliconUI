import sys

from PyQt5.QtWidgets import QApplication

from siui.templates.application import SiliconApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SiliconApplication()
    window.show()
    sys.exit(app.exec_())