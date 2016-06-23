from plugins import BasePlugin
from plugins import PluginsData

from etllib.conf import Conf
from etllib.csv import CSV

import os

class CSVPlugin(BasePlugin):

    def field_names(self):
        pass

    def file_path(self, rule=None, position='in'):
        this_path = os.path.dirname(os.path.realpath(__file__))
        if position == 'in':
            path = '/'.join([
                this_path, 
                '..', 
                rule['source_node']['path']
            ])
        else:
            pass
        filename = rule['action']
        return os.path.join(path, filename)


    def run(self, rule, data=None):
        if data:
            # Used as Egress 
            lines = []
            header = ', '.join([str(i) for i in data.fields])
            lines.append('{}\n'.format(header))
            for record in data.values:
                line = ', '.join([str(i) for i in record])
                lines.append('{}\n'.format(line))
            CSV(filepath=rule['destination_table']).write(lines) 
        else:
            # Used as Ingress 
            csv_file = self.file_path(rule=rule, position='in')
            data = CSV(filepath=csv_file).read()
            ret_data = PluginsData(data['fields'], data['values'])
            return ret_data

def init(rule):
    return CSVPlugin(rule)
       