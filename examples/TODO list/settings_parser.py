
class SettingsParser:
    def __init__(self, path):
        self.ini_path = path
        self.options = {}

        self.load()

    def load(self):
        """
        Load keys and values from .ini file
        """
        ini_file = open(self.ini_path, encoding="utf-8")
        options = {}

        for line in ini_file.readlines():
            line = line.strip()
            if self._is_a_legal_line(line) is False:
                continue

            key, value = line.split("=")
            key = key.strip()
            value = value.strip()
            options[key] = self._match_type(value)

        # update the options dict
        self.options.update(options)

    def modify(self, key, value):
        """
        Modify the dict instead of using valuation
        :param key: key
        :param value: value
        """
        self.options[key] = value

    def write(self):
        """
        Write current options dict into .ini file
        """
        ini_file = open(self.ini_path, "w", encoding="utf-8")
        for key, value in self.options.items():
            ini_file.write(f"{key} = {value}\n")

        ini_file.close()

    @staticmethod
    def _match_type(string: str):
        """
        If possible, convert string input into type it should be.\n
        Instances:
            str(1.234) -> float(1.234)\n
            str(False) -> bool(False)\n
            str(name) -> str(name)  (this method does nothing)\n
        :return: result of converting
        """
        if string == "True":
            return True

        if string == "False":
            return False

        try:
            if float(string) % 1 == 0:
                return int(float(string))
            else:
                return float(string)
        except ValueError:
            return string

    @staticmethod
    def _is_a_legal_line(line: str):
        """
        To check whether the line is a legal one which contains a key and a value
        :param line: a line in .ini file
        """
        if line.count("=") != 1:
            return False

        key, value = line.split("=")
        key = key.strip()
        value = value.strip()

        if key == "" or value == "":
            return False

        return True
