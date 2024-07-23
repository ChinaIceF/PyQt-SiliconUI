from enum import Enum, Flag, auto


class SiWidgetFlags(Flag):
    # Flags for SiWidget
    FlashOnHintUpdated = auto()         # 在工具提示被重新设置时，使工具提示闪烁
    InstantMove = auto()                # 是否立即移动而不运行动画
    InstantResize = auto()              # 是否立即重设大小而不运行动画
    InstantSetOpacity = auto()          # 是否立即重设透明度而不运行动画
    HasMoveLimits = auto()              # 是否有移动限定区域
    AdjustSizeOnTextChanged = auto()    # 是否在setText被调用时自动调整空间大小
    EnableAnimationSignals = auto()     # 是否启用moved，resized，opacityChanged信号


class SiSomethingEnums(Enum):
    NameA = 1


class Si(Flag):
    # the namespace of SiliconUI
    FlashOnHintUpdated = SiWidgetFlags.FlashOnHintUpdated.value
    InstantMove = SiWidgetFlags.InstantMove.value
    InstantResize = SiWidgetFlags.InstantResize.value
    InstantSetOpacity = SiWidgetFlags.InstantSetOpacity.value
    HasMoveLimits = SiWidgetFlags.HasMoveLimits.value
    AdjustSizeOnTextChanged = SiWidgetFlags.AdjustSizeOnTextChanged.value
    EnableAnimationSignals = SiWidgetFlags.EnableAnimationSignals.value

    NameA = SiSomethingEnums.NameA.value