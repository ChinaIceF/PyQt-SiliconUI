import warnings
from enum import Enum, auto
from typing import Any

from PyQt6 import sip
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget


class SiThemeManager(QObject):
    themeChanged = pyqtSignal()
    _instance = None

    class Preset:
        Light = "PresetLight"
        Dark = "PresetDark"

    @classmethod
    def getInstance(cls) -> "SiThemeManager":
        if cls._instance is None or sip.isdeleted(cls._instance):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._currentTheme: str
        self._themeMappings: dict[str, dict]

        self._currentTheme = self.Preset.Light
        self._themeMappings = {}

    def register(self, themeName: str, styleDataName: str, mapping: dict[Enum, object]) -> None:
        if themeName not in self._themeMappings:
            self._themeMappings[themeName] = {}
        themeMapping: dict = self._themeMappings[themeName]

        if styleDataName not in themeMapping:
            themeMapping[styleDataName] = {}
        existMapping: dict = themeMapping[styleDataName]

        for token, color_value in mapping.items():
            existMapping[token] = color_value

    def getMapping(self, className: str) -> dict:
        mapping = self._themeMappings[self._currentTheme]
        return mapping[className]

    def changeTheme(self, name: str) -> None:
        self._currentTheme = name
        self.themeChanged.emit()


class StyleData(QObject):
    styleUpdated = pyqtSignal()

    _globalStyleData: type = None
    _globalTokenClass: type = None

    class Token(Enum):
        pass

    @classmethod
    def setGlobalStyleData(cls, styleDataClass: type) -> None:
        if not issubclass(styleDataClass, cls):
            raise TypeError(f"传入的全局 StyleData 类型 {styleDataClass} 不是一个 StyleData 类型")

        cls._globalStyleData = styleDataClass
        cls._globalTokenClass = styleDataClass.Token

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._mapping: dict
        self._globalMapping: dict
        self._isMappingDirty: bool
        self._tokenClass: type

        self._mapping = {}
        self._globalMapping = {}
        self._isMappingDirty = True
        self._tokenClass = self.__class__.Token

        self._initSignal()
        self._checkHasGlobalStyleData()

    def _initSignal(self) -> None:
        mgr = SiThemeManager.getInstance()
        mgr.themeChanged.connect(self._onThemeChanged)
        self.parent().destroyed.connect(self._onParentDestroyed)

    def _checkHasGlobalStyleData(self) -> None:
        if self._globalStyleData is None:
            raise RuntimeError("在指定全局 StyleData 前尝试实例化 StyleData。请首先使用 StyleData.setGlobalStyleData")
        if self._globalTokenClass is None:
            raise RuntimeError("指定的全局 StyleData 不具有 Token 成员")

    def _onParentDestroyed(self) -> None:
        mgr = SiThemeManager.getInstance()
        try:
            mgr.themeChanged.disconnect(self._onThemeChanged)
        except (TypeError, RuntimeError) as e:
            warnings.warn(f"_onParentDestroyed 断开信号失败：{e}")

    def _onThemeChanged(self) -> None:
        self._isMappingDirty = True
        self.styleUpdated.emit()

    def _loadMapping(self) -> None:
        mgr = SiThemeManager.getInstance()
        self._mapping = mgr.getMapping(self.__class__.__name__)
        self._globalMapping = mgr.getMapping(self._globalStyleData.__name__)

    def get(self, token: Enum) -> Any:
        if not isinstance(token, Enum):
            raise ValueError(f"Token {token} 的类型 {type(token)} 不是 Enum")

        if self._isMappingDirty:
            self._loadMapping()
            self._isMappingDirty = False

        if token.__class__ == self._tokenClass:
            return self._mapping[token]

        if token.__class__ == self._globalTokenClass:
            return self._globalMapping[token]

        raise ValueError(f"{token} 不是此 StyleData 和设定的全局 StyleData 的 Token")


class TestStyleData(StyleData):
    class Token(Enum):
        BackgroundColor = auto()
        TextColor = auto()
        AccentColor = auto()


SiThemeManager.getInstance().register(
    themeName=SiThemeManager.Preset.Light,
    styleDataName=TestStyleData.__name__,
    mapping={
        TestStyleData.Token.BackgroundColor: QColor("#111111"),
        TestStyleData.Token.TextColor: QColor("#222222"),
        TestStyleData.Token.AccentColor: QColor("#333333")
    }
)