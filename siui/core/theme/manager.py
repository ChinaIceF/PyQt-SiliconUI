from enum import Enum, auto
from typing import Any

from PyQt6 import sip
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget


class SiThemeManager(QObject):
    themeChanged = pyqtSignal()
    _instance = None

    @classmethod
    def getInstance(cls) -> "SiThemeManager":
        if cls._instance is None or sip.isdeleted(cls._instance):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._currentTheme: str
        self._themeMappings: dict[str, dict]

        self._currentTheme = "normal"
        self._themeMappings = {"normal": {
            TestStyleData: {TestStyleData.Token.BackgroundColor: QColor("#114514")}
        }}

    def getMapping(self, cls: type) -> dict:
        mapping = self._themeMappings[self._currentTheme]
        return mapping[cls]

    def changeTheme(self, name: str) -> None:
        self._currentTheme = name
        self.themeChanged.emit()


class StyleData(QObject):
    styleUpdated = pyqtSignal()

    class Token(Enum):
        pass

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._mapping: dict
        self._isMappingDirty: bool
        self._tokenClass: type

        self._mapping = {}
        self._isMappingDirty = True
        self._tokenClass = self.__class__.Token

        self._initSignal()

    def _initSignal(self) -> None:
        mgr = SiThemeManager.getInstance()
        mgr.themeChanged.connect(self._onThemeChanged)
        self.destroyed.connect(self._onSelfDestroyed)

    def _onSelfDestroyed(self) -> None:
        mgr = SiThemeManager.getInstance()
        mgr.themeChanged.disconnect(self._onThemeChanged)

    def _onThemeChanged(self) -> None:
        self._isMappingDirty = True
        self.styleUpdated.emit()

    def _loadMapping(self) -> None:
        mgr = SiThemeManager.getInstance()
        self._mapping = mgr.getMapping(self.__class__)

    def get(self, token: Enum) -> Any:
        if not isinstance(token, Enum):
            raise ValueError(f"Token {token} 的类型 {type(token)} 不是 Enum")
        if token.__class__ != self._tokenClass:
            raise ValueError(f"Token {token} 的类型 {type(token)} 不是 {self.__class__} 的主题属性枚举")

        if self._isMappingDirty:
            self._loadMapping()

        return self._mapping[token]


class TestStyleData(StyleData):
    class Token(Enum):
        BackgroundColor = auto()


