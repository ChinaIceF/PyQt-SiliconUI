import ctypes
import sys
from ctypes.wintypes import MSG, RECT, POINT

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout

WM_NCCALCSIZE = 0x0083
WM_ACTIVATE = 0x0006
WM_NCHITTEST = 0x0084
SM_CXSIZEFRAME = 32
HTNOWHERE = 0x00
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
HTTOP = 12
HTLEFT = 10
HTRIGHT = 11
HTBOTTOM = 15
HTCLIENT = 1

GWL_STYLE = -16
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_CAPTION = 0x00C00000
CS_DBLCLKS = 0x0008
WS_THICKFRAME = 0x00040000


class WINDOWPOS(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.wintypes.HWND),
        ("hwndInsertAfter", ctypes.wintypes.HWND),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("cx", ctypes.c_int),
        ("cy", ctypes.c_int),
        ("flags", ctypes.wintypes.UINT)
    ]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [
        ("rgrc", ctypes.wintypes.RECT * 3),
        ("lppos", ctypes.POINTER(WINDOWPOS))
    ]


class MARGINS(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", ctypes.c_int),
        ("cxRightWidth", ctypes.c_int),
        ("cyTopHeight", ctypes.c_int),
        ("cyBottomHeight", ctypes.c_int)
    ]


def GET_X_LPARAM(lParam):
    return ctypes.c_short(lParam & 0xFFFF).value


def GET_Y_LPARAM(lParam):
    return ctypes.c_short((lParam >> 16) & 0xFFFF).value


class SiFrameless(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint |
                            Qt.WindowMinimizeButtonHint | Qt.FramelessWindowHint)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.titleHeight = 30

        self.titleWidget = QWidget(self)
        self.titleWidget.setFixedHeight(self.titleHeight)
        self.titleWidget.setStyleSheet("border-bottom: 1px solid black;")
        self.titleLayout = QHBoxLayout(self.titleWidget)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleLayout.setSpacing(0)
        self.layout.addWidget(self.titleWidget, 0, Qt.AlignTop)
        self.minimize = QPushButton(self)
        self.minimize.setFixedSize(self.titleHeight, self.titleHeight)
        self.maximize = QPushButton(self)
        self.maximize.setFixedSize(self.titleHeight, self.titleHeight)
        self.close_ = QPushButton(self)
        self.close_.setFixedSize(self.titleHeight, self.titleHeight)

        self.titleLayout.addWidget(self.minimize, 0, Qt.AlignRight)
        self.titleLayout.addWidget(self.maximize, 0)
        self.titleLayout.addWidget(self.close_, 0)

        self.close_.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showMinimized)
        self.maximize.clicked.connect(self.handle_maximize)

    def handle_maximize(self):
        if self.isMaximized():
            self.maximize.setIcon(QIcon("maximize.png"))
            self.showNormal()
        else:
            self.maximize.setIcon(QIcon("normal.png"))
            self.showMaximized()

    def setCentralWidget(self, widget):
        if self.layout.count() >= 2:
            raise RuntimeError("最多只能添加1个中央部件")
        self.layout.addWidget(widget, 1)

    def setTitleWidget(self, widget):
        if self.titleLayout.count() >= 4:
            raise RuntimeError("最多只能添加1个标题部件")
        self.titleLayout.insertWidget(0, widget, 1)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and event.pos().y() < self.titleHeight:
            self.window().windowHandle().startSystemMove()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < self.titleHeight:
            self.maximize.click()

    def showEvent(self, event):
        super().showEvent(event)
        hwnd = self.winId().__int__()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | CS_DBLCLKS)

    def nativeEvent(self, event, message):
        msg = MSG.from_address(message.__int__())
        if msg.message == WM_NCCALCSIZE:
            if ctypes.windll.user32.IsZoomed(msg.hWnd):
                border = ctypes.windll.user32.GetSystemMetrics(SM_CXSIZEFRAME) + 2
                params = ctypes.cast(msg.lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents
                # 注意这里需要测试。为窗口添加边框
                rect = params.rgrc[0]
                rect.top += border
                rect.left += border
                rect.right -= border
                rect.bottom -= border
                return True, HTNOWHERE
        elif msg.message == WM_ACTIVATE:
            margins = MARGINS(1, 1, 0, 1)
            hr = ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(msg.hWnd, ctypes.byref(margins))
            return True, hr
        elif msg.message == WM_NCHITTEST:
            mouse = POINT()
            mouse.x = GET_X_LPARAM(msg.lParam)
            mouse.y = GET_Y_LPARAM(msg.lParam)

            rc = RECT()
            ctypes.windll.user32.GetWindowRect(msg.hWnd, ctypes.byref(rc))
            boundary = 5

            left = mouse.x < rc.left + boundary
            right = mouse.x >= rc.right - boundary
            top = mouse.y < rc.top + boundary
            bottom = mouse.y >= rc.bottom - boundary

            if top and left:
                return True, HTTOPLEFT
            if top and right:
                return True, HTTOPRIGHT
            if bottom and left:
                return True, HTBOTTOMLEFT
            if bottom and right:
                return True, HTBOTTOMRIGHT
            if top:
                return True, HTTOP
            if left:
                return True, HTLEFT
            if right:
                return True, HTRIGHT
            if bottom:
                return True, HTBOTTOM
            return False, HTCLIENT
        return super().nativeEvent(event, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SiFrameless()
    window.resize(800, 600)

    central = QWidget(window)
    title = QWidget(window)

    central.setStyleSheet("background:#00ffff;")
    title.setStyleSheet("background:#ffff00;")

    QPushButton("阿松大", central)

    window.setTitleWidget(title)
    window.setCentralWidget(central)
    window.show()
    sys.exit(app.exec())
