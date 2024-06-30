import os
from dataclasses import dataclass


@dataclass(frozen=True)
class GithubUrl:
    Author_Home: str = "https://github.com/ChinaIceF"
    SiliconUI_Home: str = Author_Home + "/PyQt-SiliconUI"
    Issues_New: str = SiliconUI_Home + "/issues/new"
    SiLabel: str = SiliconUI_Home + "/blob/main/SiliconUI/SiLabel.py"
    SiButton: str = SiliconUI_Home + "/blob/main/SiliconUI/SiButton.py"
    SiComboBox: str = SiliconUI_Home + "/blob/main/SiliconUI/SiComboBox.py"
    SiSwitch: str = SiliconUI_Home + "/blob/main/SiliconUI/SiSwitch.py"
    SiSliderBar: str = SiliconUI_Home + "/blob/main/SiliconUI/SiSliderBar.py"
    SiInputBox: str = SiliconUI_Home + "/blob/main/SiliconUI/SiInputBox.py"


@dataclass(frozen=True)
class BiliBiliUrl:
    Author_Home: str = "https://space.bilibili.com/390832893"


def browse(url: str):
    os.system(f"start {url}")


if __name__ == "__main__":
    # Example usage:
    browse(GithubUrl.SiliconUI_Home)
