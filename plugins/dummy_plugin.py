from plugins import BasePlugin
from plugins import PluginsData

class DummyPlugin(BasePlugin):

    def run(self, rule, data=None):
        pass

def init(rule):
    return DummyPlugin(rule)