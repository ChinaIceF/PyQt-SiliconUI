import os

from PyQt5.QtCore import QByteArray, QSize, Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon
from PyQt5.QtSvg import QSvgRenderer


class GlobalIconPack:
    current_module_path = os.path.dirname(os.path.abspath(__file__))
    package_folder_path = os.path.join(current_module_path, "packages")

    def __init__(self):
        self.default_color = None

        self.icons = {}
        self.icons_classified = {
            "__unclassified__": {}
        }

        # load internal icon packages
        self.reload_internals()

    def setDefaultColor(self, code) -> None:
        self.default_color = code

    @property
    def defaultColor(self) -> str:
        return self.default_color

    def reload_internals(self) -> None:
        for package_filename in os.listdir(self.package_folder_path):
            full_path = os.path.join(self.package_folder_path, package_filename)
            if os.path.isfile(full_path):
                self.load_from_file(full_path)

    def load_from_file(self, path) -> None:
        class_name = os.path.basename(path)
        self.append_class(class_name)
        with open(path, encoding="utf-8") as file:
            for line in file.readlines():
                if line[0:2] == "##":
                    continue
                if line.strip() == "":
                    continue

                line = line.strip()
                icon_name, icon_data = line.split("////")
                self.append(icon_name, icon_data, class_name)

    def append_class(self, class_name, force=False) -> None:
        if class_name in self.icons_classified.keys() and (force is False):
            raise ValueError(f"Class name {class_name} is already exist.")
        self.icons_classified[class_name] = {}

    def append(self, name, data, class_name: str = "__unclassified__") -> None:
        self.icons[name] = data
        self.icons_classified[class_name][name] = data

    def get(self, name, color_code: str = None) -> bytes:
        color_code = self.default_color if color_code is None else color_code
        return self.icons[name].replace("<<<COLOR_CODE>>>", color_code).encode()

    def getFromData(self, data, color_code: str = None) -> bytes:
        color_code = self.default_color if color_code is None else color_code
        return data.replace("<<<COLOR_CODE>>>", color_code).encode()

    def getByteArray(self, name, color_code: str = None) -> QByteArray:
        svg_bytes = self.get(name, color_code)
        return QByteArray(svg_bytes)

    def getDict(self, class_name=None) -> dict:
        """
        Get dictionary of an icon package.
        If class name is assigned, returns the specific package dictionary.
        If class name is None, returns a dictionary that contains all icons.
        """
        if class_name is None:
            return self.icons
        else:
            return self.icons_classified[class_name]

    def getClassNames(self) -> dict.keys:
        return self.icons_classified.keys()

    def toPixmap(self, name: str, size: QSize = QSize(64, 64), color_code: str = None):
        svg_bytes = self.get(name, color_code)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_bytes)
        svg_renderer.render(painter)
        painter.end()
        return pixmap

    def toIcon(self, name: str, size: QSize = QSize(64, 64), color_code: str = None) -> QIcon:
        return QIcon(self.toPixmap(name, size, color_code))

