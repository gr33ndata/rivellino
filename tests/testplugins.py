import unittest

from plugins import PluginEngine

class TestPlugins(unittest.TestCase):

    def setUp(self):
        pass

    def test_plugins_load(self): 
        pe = PluginEngine()
        for plugin in pe:
            self.assertEqual(pe[plugin].init(rule={
                'rule_name': 'test'
            }).probe(), True)


if __name__ == '__main__':

    unittest.main()