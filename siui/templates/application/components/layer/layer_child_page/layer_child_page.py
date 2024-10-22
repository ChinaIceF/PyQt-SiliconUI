from PyQt5.QtCore import Qt, QTimer

from ..layer import SiLayer


class LayerChildPage(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.child_page = None
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def childPage(self):
        return self.child_page

    def setChildPage(self, page):
        if self.childPage() is not None:
            page.deleteLater()
            return

        self.child_page = page
        self.child_page.animationGroup().fromToken("move").setFactor(1/4)
        self.child_page.animationGroup().fromToken("move").setBias(0.5)
        self.child_page.setParent(self)
        self.child_page.adjustSize()
        self.child_page.move((self.width() - self.childPage().width()) // 2, self.height())
        self.child_page.show()
        self.showLayer()

    def showLayer(self):
        super().showLayer()
        self.showChildPage()

    def closeLayer(self):
        super().closeLayer()
        self.closeChildPage()

    def showChildPage(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.child_page.moveTo((self.width() - self.childPage().width()) // 2, self.height() - self.childPage().height())

    def closeChildPage(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.child_page.moveTo((self.width() - self.childPage().width()) // 2, self.height())
        self.child_page.delete_timer = QTimer()
        self.child_page.delete_timer.singleShot(500, self.child_page.deleteLater)
        self.child_page = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.child_page is not None:
            self.child_page.adjustSize()
            self.child_page.move((self.width() - self.childPage().width()) // 2, self.height() - self.childPage().height())
