"""
## This module defines global shared types

Use Python's Type Hint syntax, reference:
- [`typing`](https://docs.python.org/3/library/typing.html)
- [`PEP 484`](https://www.python.org/dev/peps/pep-0484/)
- [`PEP 526`](https://www.python.org/dev/peps/pep-0526/)
"""

from typing import Optional, Union

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QColor, QGradient, QPainter, QPen
from PyQt5.QtWidgets import QWidget
from typing_extensions import TypeAlias

T_WidgetParent: TypeAlias = Optional[QWidget]
"""Type of widget parent"""

T_ObjectParent: TypeAlias = Optional[QObject]
"""Type of object parent"""

T_PenStyle: TypeAlias = Union[QPen, Qt.PenStyle, QColor, Qt.GlobalColor]
"""Type of QPen style"""

T_Brush: TypeAlias = Optional[Union[QGradient, QColor, Qt.GlobalColor]]
"""Type of QBrush"""

T_RenderHint: TypeAlias = Optional[Union[QPainter.RenderHint, int]]
"""Type of QPainter.RenderHint"""