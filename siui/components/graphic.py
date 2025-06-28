from typing import List

from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtProperty
from PyQt5.QtGui import QPainter, QTransform, QWheelEvent
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QWidget

from siui.core.animation import SiExpAnimationRefactor
from siui.typing import T_WidgetParent


class SiAnimatedTransformGraphicProxyWidget(QGraphicsProxyWidget):
    class Property:
        XRotate = "xRotate"
        YRotate = "yRotate"
        ZRotate = "zRotate"

        Scale = "scale"
        Center = "center"
        Opacity = "opacity"
        Translate = "translate"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._x_rotate = 0.0
        self._y_rotate = 0.0
        self._z_rotate = 0.0
        self._scale = 1.0
        self._opacity = 1.0  # unused
        self._center = QPointF()
        self._translate = QPointF()

        self.x_rotate_ani = SiExpAnimationRefactor(self, self.Property.XRotate)
        self.y_rotate_ani = SiExpAnimationRefactor(self, self.Property.YRotate)
        self.z_rotate_ani = SiExpAnimationRefactor(self, self.Property.ZRotate)
        self.scale_ani = SiExpAnimationRefactor(self, self.Property.Scale)
        self.center_ani = SiExpAnimationRefactor(self, self.Property.Center)
        self.opacity_ani = SiExpAnimationRefactor(self, self.Property.Opacity)
        self.translate_ani = SiExpAnimationRefactor(self, self.Property.Translate)

        self.x_rotate_ani.init(1/6, 0.01, self._x_rotate, self._x_rotate)
        self.y_rotate_ani.init(1/6, 0.01, self._y_rotate, self._y_rotate)
        self.z_rotate_ani.init(1/6, 0.01, self._z_rotate, self._z_rotate)
        self.scale_ani.init(1/8, 0.0001, self._scale, self._scale)
        self.center_ani.init(1/6, 0.01, self._center, self._center)
        self.opacity_ani.init(1/16, 0.01, self._opacity, self._opacity)
        self.translate_ani.init(1/6, 0.01, self._translate, self._translate)

        self.setAcceptHoverEvents(True)

    @pyqtProperty(QPointF)
    def center(self):
        return self._center

    @center.setter
    def center(self, value: QPointF):
        self._center = value
        self.updateTransform()

    @pyqtProperty(QPointF)
    def translate(self):
        return self._translate

    @translate.setter
    def translate(self, value: QPointF):
        self._translate = value
        self.updateTransform()

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.updateTransform()

    @pyqtProperty(float)
    def xRotate(self):
        return self._x_rotate

    @xRotate.setter
    def xRotate(self, value: float):
        self._x_rotate = value
        self.updateTransform()

    @pyqtProperty(float)
    def yRotate(self):
        return self._y_rotate

    @yRotate.setter
    def yRotate(self, value: float):
        self._y_rotate = value
        self.updateTransform()

    @pyqtProperty(float)
    def zRotate(self):
        return self._z_rotate

    @zRotate.setter
    def zRotate(self, value: float):
        self._z_rotate = value
        self.updateTransform()

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.XRotate: self.x_rotate_ani,
            self.Property.YRotate: self.y_rotate_ani,
            self.Property.ZRotate: self.z_rotate_ani,
            self.Property.Scale: self.scale_ani,
            self.Property.Center: self.center_ani,
            self.Property.Opacity: self.opacity_ani,
            self.Property.Translate: self.translate_ani,
        }.get(prop_name)

    def updateTransform(self):
        transform = QTransform()
        transform.translate(self._center.x(), self._center.y())

        transform.rotate(self._x_rotate, Qt.XAxis)
        transform.rotate(self._y_rotate, Qt.YAxis)
        transform.rotate(self._z_rotate, Qt.ZAxis)
        transform.scale(self._scale, self._scale)

        transform.translate(-self._center.x(), -self._center.y())
        transform.translate(self._translate.x(), self._translate.y())

        self.setTransform(transform)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.grabMouse()

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.ungrabMouse()


class SiGraphicWrapperWidget(QWidget):
    class TransitionAnimations:
        @staticmethod
        def fadeIn(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            opacity_ani = proxy_widget.animation(proxy_widget.Property.Opacity)
            opacity_ani.setCurrentValue(0.0)
            opacity_ani.setEndValue(1.0)
            # opacity_ani.toProperty()
            opacity_ani.start()

        @staticmethod
        def floatUp(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            translate_ani = proxy_widget.animation(proxy_widget.Property.Translate)
            translate_ani.setCurrentValue(QPointF(0, 50))
            translate_ani.setEndValue(QPointF(0, 0))
            # translate_ani.toProperty()
            translate_ani.start()

        @staticmethod
        def floatDown(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            translate_ani = proxy_widget.animation(proxy_widget.Property.Translate)
            translate_ani.setCurrentValue(QPointF(0, -50))
            translate_ani.setEndValue(QPointF(0, 0))
            # translate_ani.toProperty()
            translate_ani.start()

        @staticmethod
        def floatLeftIn(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            translate_ani = proxy_widget.animation(proxy_widget.Property.Translate)
            translate_ani.setCurrentValue(QPointF(-50, 0))
            translate_ani.setEndValue(QPointF(0, 0))
            # translate_ani.toProperty()
            translate_ani.start()

        @staticmethod
        def floatRightIn(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            translate_ani = proxy_widget.animation(proxy_widget.Property.Translate)
            translate_ani.setCurrentValue(QPointF(50, 0))
            translate_ani.setEndValue(QPointF(0, 0))
            # translate_ani.toProperty()
            translate_ani.start()

        @staticmethod
        def scaleUp(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            scale_ani = proxy_widget.animation(proxy_widget.Property.Scale)
            scale_ani.setCurrentValue(0.95)
            scale_ani.setEndValue(1.0)
            # scale_ani.toProperty()
            scale_ani.start()

        @staticmethod
        def resetToFloatUp(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            translate_ani = proxy_widget.animation(proxy_widget.Property.Translate)
            translate_ani.setCurrentValue(QPointF(0, 50))
            translate_ani.toProperty()

        @staticmethod
        def rotateInX(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            rotate_ani = proxy_widget.animation(proxy_widget.Property.XRotate)
            rotate_ani.setCurrentValue(25)
            rotate_ani.setEndValue(0)
            rotate_ani.start()

        @staticmethod
        def rotateInY(proxy_widget: SiAnimatedTransformGraphicProxyWidget):
            rotate_ani = proxy_widget.animation(proxy_widget.Property.YRotate)
            rotate_ani.setCurrentValue(25)
            rotate_ani.setEndValue(0)
            rotate_ani.start()

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._animation_funcs = []
        self._proxy_widget = SiAnimatedTransformGraphicProxyWidget()
        self._scene = QGraphicsScene()
        self._view = QGraphicsView(self._scene, self)
        self._widget = QWidget()

        self._proxy_widget.setWidget(self._widget)
        self._scene.addItem(self._proxy_widget)

        self._initStyle()

    def _initStyle(self) -> None:
        self._view.setStyleSheet("background-color: transparent; border: none")
        self._view.setRenderHints(
            QPainter.Antialiasing
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )

    def sizeHint(self):
        return self.widget().sizeHint()

    def setMergeAnimations(self, *funcs) -> None:
        self._animation_funcs = funcs

    def mergeAnimations(self) -> List:
        return self._animation_funcs

    def widget(self) -> QWidget:
        return self._widget

    def graphicsProxyWidget(self) -> SiAnimatedTransformGraphicProxyWidget:
        return self._proxy_widget

    def setWidget(self, widget: QWidget) -> None:
        widget.setParent(None)
        self._widget = widget
        self._proxy_widget.setWidget(self._widget)

    def playMergeAnimations(self):
        for func in self._animation_funcs:
            func(self._proxy_widget)

    def playAnimations(self, alist: List):
        for func in alist:
            func(self._proxy_widget)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._view.setGeometry(0, 0, self.width(), self.height())
        self._scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))
        self._widget.resize(self.size())
        print(self.size())
        self._proxy_widget.setProperty(self._proxy_widget.Property.Center, QPointF(self.width() / 2, self.height() / 2))
