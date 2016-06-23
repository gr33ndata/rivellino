import os
import sys

from etllib.yaml_helper import YAMLHelper

class Conf:

    def __init__(self, file_path=''):
        
        if file_path:
            self.file_path = file_path
        else:
            cwd = os.path.dirname(os.path.realpath(__file__))
            self.file_path = os.path.join(cwd, '..', 'config.yml') 
        
        self.conf_dict = YAMLHelper(self.file_path).read()
 
    def get_conf_dict(self):
        return self.conf_dict

    def get_data_nodes(self, node_name=None):
        if node_name:
            return self.conf_dict['data_nodes'].get(node_name, 'NaN')
        else:
            return self.conf_dict['data_nodes'].keys()

if __name__ == '__main__':
    
    c = Conf()
    c.get_data_nodes()
