import os
import json

class Config():

    config = {}
    files = []

    _paths = ['../../config/secrets', '../../config/app']

    def __init__(self):
        self._readConfigFiles()

    def _getConfigFiles(self):
        """
        This method will read all Config Files located at self._paths
        :return:
        """
        for folder in self._paths:
            path = os.path.join(os.path.dirname(__file__), folder)
            for element in os.listdir(path):
                if element[0] == ".":
                    continue

                new_path = os.path.join(path, element)

                if os.path.isfile(new_path):
                    self.files.append(new_path)

    def _readConfigFiles(self):
        """
        This mehod will combine all config files into one dictionary
        :return:
        """
        self._getConfigFiles()
        for file in self.files:
            with open(file, "r") as config_file:
                filename = os.path.basename(config_file.name).replace('.json', '')

                config = config_file.read()
                self.config[filename] = json.loads(config, encoding="UTF-8")