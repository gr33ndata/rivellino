from plugins import BasePlugin
from plugins import PluginsData

class ScreenDumpPlugin(BasePlugin):

    def run(self, rule, data=None, rows_display_limit = 100):
        if data and isinstance(data, PluginsData):
            print 'Fields:'
            for field in data.fields:
                print ' {0}'.format(field)          
            print 'Values:'
            for row in data.values[:rows_display_limit]:
                print '  ', ', '.join([str(field) for field in row])
            if len(data.values) > rows_display_limit:
                print '   ... Showing {0} of {1} items'.format(rows_display_limit, len(data.values)) 
        else:
            pass

def init(rule):
    return ScreenDumpPlugin(rule)
