import os
import glob
import imp

plugins_path = os.path.dirname(os.path.realpath(__file__))

class PluginsData:

    def __init__(self, fields=None, values=None):
        self.fields = list(fields) if fields else None
        self.values = list(values) if values else None

    def __str__(self):
        s = 'PluginsData: {0} rows with fields [{1}]'.format(
            str(len(self.values)),
            ', '.join(self.fields)
        )
        return s

    def __getitem__(self, item):
        if isinstance(item, int):
            col_id = item
        elif isinstance(item, str):
            col_id = self.fields.index(item)
        else:
            raise KeyError
        col_data = [
            row[col_id]
            for row in self.values
        ]
        return col_data

    def get_field_id(self, field_name):
        return self.fields.index(field_name)


class BasePlugin:

    def __init__(self, rule):
        self.rule = rule
        self.debug = self.rule.get('debug', False)
        self.debug_file = self.rule.get('debug_file', False)
        if self.debug_file:
            self.debug_file_fd = open(self.debug_file, 'r+')
        self.init(rule)
        self.print_debug('Plugin {0} initialized'.format(
            self.rule['rule_name']
        ))

    def init(self, rule):
        pass

    def print_debug(self, msg):
        if self.debug:
            print 'DEBUG: {0}'.format(msg)

    def dump_debug(self, msg):
        if self.debug_file:
            self.debug_file_fd.write(msg)

    def probe(self):
        return True

    def run(self, rule, data=None):
        raise NotImplementedError

    def exit(self):
        self.print_debug('Plugin {0} exit'.format(
            self.rule['rule_name']
        ))
        if self.debug_file:
            self.debug_file_fd.close()

class PluginEngine:
    
    def __init__(self):
        self.plugins = {}
        for path in glob.glob(os.path.join(plugins_path,'[!_]*.py')):
            name, ext = os.path.splitext(os.path.basename(path))
            self.plugins[name] = imp.load_source(name, path)
    
    def __iter__(self):
        for name in self.plugins:
            yield name

    def __getitem__(self, name): 
        # In case of an unknown plugin, we run dummy_plugin  
        return self.plugins.get(name, self.plugins['dummy_plugin'])

