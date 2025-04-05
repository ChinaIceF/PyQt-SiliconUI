from PyQt5.QtCore import QPointF, Qt, pyqtProperty
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsProxyWidget

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
        self.scale_ani.init(1/6, 0.01, self._scale, self._scale)
        self.center_ani.init(1/6, 0.01, self._center, self._center)
        self.opacity_ani.init(1/16, 0.01, self._opacity, self._opacity)
        self.translate_ani.init(1/6, 0.01, self._translate, self._translate)

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
