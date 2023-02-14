import io
import json
import zipfile
from django.conf import settings


class Configurator:
    def __init__(self, mappings, config):
        self._mappings = mappings
        self._config = config

        self._file_mappings = None
        self._file_config = None

    def read_json(self):
        with open(settings.MAPPINGS_PATH, 'r', encoding='utf8') as file:
            return json.load(file)

    def create_file(self, data):
        file = io.StringIO()
        json.dump(data, file, indent=2, ensure_ascii=False)

        return file.getvalue()

    def create_config(self):
        data = {'database': self._config}

        return self.create_file(data)

    def create_mapping(self):
        jsons = self.read_json()
        data = {'properties': {}}
        for item in self._mappings:
            key = jsons.get(item, None)
            if key:
                data['properties'][item] = key

        return self.create_file(data)

    def generate_zip(self):
        file_mappings = self.create_mapping()
        file_config = self.create_config()

        with zipfile.ZipFile(settings.MEDIA_ROOT + 'config.zip', 'w') as myzip:
            myzip.writestr(settings.PATH_CONFIGURATOR_MAPPINGS, file_mappings)
            myzip.writestr(settings.PATH_CONFIGURATOR_CONFIG, file_config)

        return settings.MEDIA_URL + 'config.zip'
