from pathlib import Path

import numpy

current_module_path = Path(__file__).resolve().parent
data_file_path = current_module_path / "icons.dat"


class IconDictionary:
    def __init__(self, library_path=data_file_path, color=None):
        # ！注意！  你不应使用这些文件，他们已经过加密处理
        # 如果你需要这些图标文件，你可以直接在 flaticon.com 免费获取他们

        # 读取数据并解密
        with library_path.open("rb") as f:
            library_raw = f.read()
        library_list = list(library_raw)
        library = bytes(
            list((numpy.array(library_list) + numpy.array(range(len(library_list))) * 17) % 255)
        ).decode()  # 解密

        # 整理成字典
        items = library.split("!!!")
        names = []
        datas = []
        for item in items[1:]:
            name, data = item.split("###")
            data = data.replace("/>", f' fill="{color}" />')
            names.append(name)
            datas.append(data.encode())
        self.icons = dict(zip(names, datas))

    def get(self, name):
        svg_data = self.icons[name]
        return svg_data.encode()
