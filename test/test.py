import sys
from PyQt5.QtCore    import Qt
from PyQt5.QtGui     import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication

class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.radius = 32
        self.path = None

    def setRadius(self, r):
        self.radius = r

    def load(self, path):
        self.path = path

    def draw(self):
        if self.path is None:
            return

        w, h = self.width(), self.height()
        self.setMaximumSize(w, h)
        self.setMinimumSize(w, h)

        self.target = QPixmap(self.size())
        self.target.fill(Qt.transparent)

        p = QPixmap(self.path).scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        label = Label(self)
        label.resize(128, 128)
        label.setRadius(64)
        label.load("./headpic.png")
        label.draw()

        layout.addWidget(label)
        self.setStyleSheet("background: #262224;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
