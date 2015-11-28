import json
import os


class ConfigParser(object):
    def __init__(self):
        self._config = {}

    def read(self, path):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            raise OSError('{} does not exist'.format(path))
        with open(path, 'rb') as f:
            try:
                self._config = json.loads(f.read())
            except ValueError, e:
                raise e

    def get(self, key):
        try:
            return self._config[key]
        except ValueError, e:
            raise e

try:
    config = ConfigParser()
    config.read('~/.gitlab')
    PRIVATE_TOKEN = config.get('private_token')
except OSError:
    PRIVATE_TOKEN = None
