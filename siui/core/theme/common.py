from enum import Enum, auto

from PyQt6.QtGui import QColor

from siui.core.theme.manager import SiThemeManager, StyleData


class GlobalStyleData(StyleData):
    class Token(Enum):
        Accent = auto()
        Border = auto()
        Flash = auto()

        SurfaceBase = auto()
        SurfaceLevel1 = auto()
        SurfaceLevel2 = auto()
        SurfaceLevel3 = auto()

        TextOnAccent = auto()
        TextLevel1 = auto()
        TextLevel2 = auto()
        TextMuted = auto()


GlobalStyleData.registerData(
    themeName=SiThemeManager.Preset.Light,
    mapping={
        GlobalStyleData.Token.Accent:             QColor(),
        GlobalStyleData.Token.Border:             QColor(),
        GlobalStyleData.Token.Flash:              QColor(),
        GlobalStyleData.Token.SurfaceBase:        QColor(),
        GlobalStyleData.Token.SurfaceLevel1:      QColor(),
        GlobalStyleData.Token.SurfaceLevel2:      QColor(),
        GlobalStyleData.Token.SurfaceLevel3:      QColor(),
        GlobalStyleData.Token.TextOnAccent:       QColor(),
        GlobalStyleData.Token.TextLevel1:         QColor(),
        GlobalStyleData.Token.TextLevel2:         QColor(),
        GlobalStyleData.Token.TextMuted:          QColor()
    }
)

GlobalStyleData.registerData(
    themeName=SiThemeManager.Preset.Dark,
    mapping={
        GlobalStyleData.Token.Accent:             QColor("#D087DF"),
        GlobalStyleData.Token.Border:             QColor("#38383D"),
        GlobalStyleData.Token.Flash:              QColor("#FFFFFF"),
        GlobalStyleData.Token.SurfaceBase:        QColor("#181818"),
        GlobalStyleData.Token.SurfaceLevel1:      QColor("#202021"),
        GlobalStyleData.Token.SurfaceLevel2:      QColor("#272729"),
        GlobalStyleData.Token.SurfaceLevel3:      QColor("#3C3C42"),
        GlobalStyleData.Token.TextOnAccent:       QColor("#FFFFFF"),
        GlobalStyleData.Token.TextLevel1:         QColor("#CBCBD4"),
        GlobalStyleData.Token.TextLevel2:         QColor("#8B8B98"),
        GlobalStyleData.Token.TextMuted:          QColor("#56565E")
    }
)


StyleData.setGlobalStyleData(GlobalStyleData)
