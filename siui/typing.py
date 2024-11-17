"""
## This module defines global shared types

Use Python's Type Hint syntax, reference:
- [`typing`](https://docs.python.org/3/library/typing.html)
- [`PEP 484`](https://www.python.org/dev/peps/pep-0484/)
- [`PEP 526`](https://www.python.org/dev/peps/pep-0526/)
"""

from typing import Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from typing_extensions import TypeAlias

T_WidgetParent: TypeAlias = Optional[QWidget]
"""Type of widget parent"""

T_ObjectParent: TypeAlias = Optional[QObject]
"""Type of object parent"""
