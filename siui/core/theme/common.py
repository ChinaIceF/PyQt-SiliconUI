from enum import Enum, auto

from PyQt6.QtGui import QColor

from siui.core.theme.manager import SiThemeManager, StyleData


class SiCommonStyleData(StyleData):
    class Token(Enum):
        BackgroundFill = auto()
        BackgroundCard = auto()


SiThemeManager.getInstance().register(
    themeName=SiThemeManager.Preset.Light,
    styleDataName=SiCommonStyleData.__name__,
    mapping={
        SiCommonStyleData.Token.BackgroundFill: QColor("#EEEEEE"),
        SiCommonStyleData.Token.BackgroundCard: QColor("#FFFFFF"),
    }
)

SiThemeManager.getInstance().register(
    themeName=SiThemeManager.Preset.Dark,
    styleDataName=SiCommonStyleData.__name__,
    mapping={
        SiCommonStyleData.Token.BackgroundFill: QColor("#111111"),
        SiCommonStyleData.Token.BackgroundCard: QColor("#222222"),
    }
)

