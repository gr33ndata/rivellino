import os
import sys
import yaml

from etllib.conf import Conf
from etllib.yaml_helper import YAMLHelper
from plugins import PluginEngine

class RulesEngine(list):

    def __init__(self):
        self.rules_path = os.path.dirname(os.path.realpath(__file__))
        self.conf = Conf()
        self.load()
        self.filter_recursion()
        self.pe = PluginEngine()
    
    def parse_rule_file(self, file_path):
        yaml_data = YAMLHelper(file_path).read()
        yaml_data['rule_name'] = os.path.split(file_path)[1]
        if yaml_data['rule_type'] == 'group':
            # Group Rule, i.e. with child rules
            pass
        else:
            # Single Rule, i.e. with no child rules
            # Get Data Nodes parameters from Config file
            src = yaml_data['source_node']
            dst = yaml_data['destination_node']
            yaml_data['source_node'] = self.conf.get_data_nodes(src)
            yaml_data['destination_node'] = self.conf.get_data_nodes(dst)
        return yaml_data

    def load(self):
        rule_files = [os.path.join(self.rules_path, f) 
                  for f in os.listdir(self.rules_path) 
                  if os.path.isfile(os.path.join(self.rules_path, f))
                  and f.endswith('.yml') 
        ]
        for rule_file in rule_files:
            self.append(self.parse_rule_file(rule_file))

    def filter_recursion(self):
        # Filter out group rules with members of type groups
        for rule in self:
            if rule['rule_type'] == 'group':
                rule_members = [
                    child for child in rule['members']
                    if self.get_rule_by_name(child)['rule_type'] == 'single'
                ]
                rule['members'] = rule_members

    def get_rule_by_name(self, rule_name):
        for rule in self:
            if rule['rule_name'] == rule_name:
                return rule
        #print 'rule not found'

    def expand_action(self, action):
        if isinstance(action, str): 
            if action.startswith('$rule:'):
                _, subrule_name, subrule_field = action.strip().split(':')
                subrule = self.get_rule_by_name(subrule_name)
                return self.apply_rule_ingress(subrule)[subrule_field]
            else:
                return action
        elif isinstance(action, dict):
            for key, val in action.iteritems(): 
                action[key] = self.expand_action(val)
            return action
        else:
            return action   


    def apply_rule_ingress(self, rule):
        ingress_plugin_name = rule['ingress_plugin']
        ingress_plugin_runnable = self.pe[ingress_plugin_name].init(rule)
        data = ingress_plugin_runnable.run(rule, None)
        ingress_plugin_runnable.exit()
        return data

    def apply_rule_egress(self, rule, data):
        egress_plugin_name = rule['egress_plugin']
        egress_plugin_runnable = self.pe[egress_plugin_name].init(rule)
        egress_plugin_runnable.run(rule, data)
        egress_plugin_runnable.exit()

    def apply_data_processors(self, rule, data):
        if not rule.get('data_processors', False):
            return data
        if type(rule['data_processors']) is str:
            data_processors = [rule['data_processors']]
        else:
            data_processors = rule['data_processors']
        for processor_plugin_name in data_processors:
            processor_plugin_runnable = self.pe[processor_plugin_name].init(rule)
            data = processor_plugin_runnable.run(rule, data)
            processor_plugin_runnable.exit()
        return data

    def apply_rule(self, rule):
        print 'Applying {0}'.format(rule['rule_name'])
        if rule['rule_type'] == 'single':
            rule['action'] = self.expand_action(rule['action'])
            data = self.apply_rule_ingress(rule)
            data = self.apply_data_processors(rule, data)
            self.apply_rule_egress(rule, data)
        else:
            for child_rule_name in rule['members']:
                self.apply_rule_by_name(child_rule_name)

    def apply_rule_by_name(self, rule_name):
        for rule in self:
            if rule['rule_name'] == rule_name:
                self.apply_rule(rule)
                break
        else:
            sys.exit('Error! Rule not found')

    def apply_rules(self):
        for rule in self:
            if rule['active']:
                self.apply_rule(rule)
            