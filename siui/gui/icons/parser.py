import os


class SiGlobalIconPack:
    current_module_path = os.path.dirname(os.path.abspath(__file__))
    package_folder_path = os.path.join(current_module_path, 'packages')

    def __init__(self):
        self.default_color = None

        self.icons = {}
        self.icons_classified = {
            "__unclassified__": {}
        }

        # load internal icon packages
        self.reload_internals()

    def set_default_color(self, code):
        self.default_color = code

    def reload_internals(self):
        for package_filename in os.listdir(self.package_folder_path):
            full_path = os.path.join(self.package_folder_path, package_filename)
            if os.path.isfile(full_path):
                self.load_from_file(full_path)

    def load_from_file(self, path):
        class_name = os.path.basename(path)
        self.append_class(class_name)
        with open(path, encoding="utf-8") as file:
            for line in file.readlines():
                if line[0:2] == "##":
                    continue
                if line.strip() == "":
                    continue

                line = line.strip()
                icon_name, icon_data = line.split("////")
                self.append(icon_name, icon_data, class_name)

    def append_class(self, class_name, force=False):
        if class_name in self.icons_classified.keys() and (force is False):
            raise ValueError("Class name {} is already exist.".format(class_name))
        self.icons_classified[class_name] = {}

    def append(self, name, data, class_name: str = "__unclassified__"):
        self.icons[name] = data
        self.icons_classified[class_name][name] = data

    def get(self, name, color_code: str = None):
        color_code = self.default_color if color_code is None else color_code
        return self.icons[name].replace("<<<COLOR_CODE>>>", color_code).encode()

    def get_from_data(self, data, color_code: str = None):
        color_code = self.default_color if color_code is None else color_code
        return data.replace("<<<COLOR_CODE>>>", color_code).encode()

    def get_dict(self, class_name=None):
        """
        Get dictionary of an icon package.
        If class name is assigned, returns the specific package dictionary.
        If class name is None, returns a dictionary that contains all icons.
        """
        if class_name is None:
            return self.icons
        else:
            return self.icons_classified[class_name]

    def get_class_names(self):
        return self.icons_classified.keys()
