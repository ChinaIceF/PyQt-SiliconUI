from enum import Enum, auto


class Si(Enum):
    # the namespace of SiliconUI
    # Flags for SiWidget
    FlashOnHintUpdated = auto()         # 在工具提示被重新设置时，使工具提示闪烁
    InstantMove = auto()                # 是否立即移动而不运行动画
    InstantResize = auto()              # 是否立即重设大小而不运行动画
    InstantSetOpacity = auto()          # 是否立即重设透明度而不运行动画
    HasMoveLimits = auto()              # 是否有移动限定区域
    AdjustSizeOnTextChanged = auto()    # 是否在setText被调用时自动调整空间大小
    EnableAnimationSignals = auto()     # 是否启用moved，resized，opacityChanged信号
    DeleteOnHidden = auto()             # 下一次被隐藏时，运行 deleteLater()
    DeleteCenterWidgetOnCenterWidgetHidden = auto()  # 中心控件下一次被隐藏时，运行 centerWidget().deleteLater()
