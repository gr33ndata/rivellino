import yaml

class YAMLHelper:

    def __init__(self, filename=''):
        self.filename = filename

    def read(self):
        data = None
        with open(self.filename, 'r') as fd:
            data = yaml.load(fd)
        return data