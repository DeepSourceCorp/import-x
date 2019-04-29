import json
from pathlib import Path

from import_x import ExtensionLoader


class JsonLoader(ExtensionLoader):
    extension = '.json'
    auto_enable = True

    @staticmethod
    def handle_module(module, path):
        """
        Load the json file and set as `data` attribute of the module.
        """
        json_file = Path(path)
        content = json_file.read_text()
        try:
            data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            data = {}
        module.data = data
