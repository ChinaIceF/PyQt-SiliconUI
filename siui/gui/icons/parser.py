import os


class SiGlobalIconPack:
    current_module_path = os.path.dirname(os.path.abspath(__file__))
    package_folder_path = os.path.join(current_module_path, 'packages')

    def __init__(self):
        self.icons = {}

        # load internal icon packages
        self.reload_internals()

    def reload_internals(self):
        for package_filename in os.listdir(self.package_folder_path):
            full_path = os.path.join(self.package_folder_path, package_filename)
            self.load_from_file(full_path)

    def load_from_file(self, path):
        with open(path, encoding="utf-8") as file:
            for line in file.readlines():
                if line[0:2] == "##":
                    continue
                if line.strip() == "":
                    continue

                line = line.strip()
                icon_name, icon_data = line.split("////")
                self.append(icon_name, icon_data)

    def append(self, name, data):
        self.icons[name] = data

    def get(self, name, color_code: str = "#212121"):
        return self.icons[name].replace("<<<COLOR_CODE>>>", color_code).encode()

    def get_dict(self):
        return self.icons


mypack = SiGlobalIconPack()
print(mypack.get("ic_fluent_calendar_3_day_light", "#FFFFFF"))