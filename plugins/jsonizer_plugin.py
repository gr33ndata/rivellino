from plugins import BasePlugin
from plugins import PluginsData

from etllib.conf import Conf
from etllib.db import DB
from etllib.metrics import Metrics
from etllib.json_helper import JSONHelper as jh

from operator import itemgetter

import json
import re

class Transformations:

    def __init__(self, tr=[], first_field='eid', last_field='json'):
        self.defaul_type = 'string'
        self.defaul_regex = None
        self.defaul_sub_key = 'year'
        self.defaul_template = {}
        self.defaul_is_sql_feild = False
        self.first_field = first_field
        self.last_field = last_field
        self.t = {}
        self.sql_fields = []
        self.all_sql_fields = []
        self.load(tr, first_field, last_field)

    def load(self, tr, first_field, last_field):
        for tr_item in tr:
            field = tr_item['field']
            ftype = tr_item.get('type', 'string')
            fisql = tr_item.get('sql_field', False)
            fregx = tr_item.get('regex', None)
            ftemp = tr_item.get('template', None)
            self.t[field] = {
                'type': ftype,
                'sql_field': fisql,
                'regex': fregx,
                'template': ftemp
            }
            if fisql:
                self.sql_fields.append(field)
        self.all_sql_fields = [first_field] + self.sql_fields + [last_field]

    def get_type(self, key):
        try:
            return self.t[key]['type']
        except:
            return self.defaul_type

    def get_regex(self, key):
        try:
            return self.t[key]['regex']
        except:
            return self.defaul_regex

    def get_sub_key(self, key):
        try:
            return self.t[key]['sub_key']
        except:
            return self.defaul_sub_key

    def get_template(self, key):
        try:
            return json.loads(self.t[key]['template'])
        except:
            if self.t[key]['type'] == 'map':
                raise
            return self.defaul_template

    def is_sql_field(self, key):
        try:
            return self.t[key]['sql_field']
        except:
            return self.defaul_is_sql_feild

    def get_sql_fields(self):
        return self.sql_fields

    def get_all_sql_fields(self):
        return self.all_sql_fields

    def encode(self, s):
        try:
            return unicode(s, errors='ignore').encode("utf-8")
        except:
            return s

    def regex_extract(self, k, v):
        regex_str = self.get_regex(k)
        if regex_str:
            try: 
                v = re.match(regex_str, v).group('extract')
            except:
                v = ''
        return v

class JsonizerPlugin(BasePlugin):

    def init(self, rule):
        self.match_rules = []
        self.transformations = None

    def get_params(self, rule):
        return rule['action'].get('params', {})

    def load_transformations(self, rule, first_field, last_field):
        t = rule['action'].get('transformations', {})
        self.transformations = Transformations(t, first_field, last_field)

    def get_sql(self, rule):
        params = self.get_params(rule)
        sql = rule['action'].get('data', '')
        for k, v in params.items():
            p = '${0}'.format(k)
            v = str(v)
            sql = sql.replace(p, v)
        return sql

    def make_entities(self, data):
        e = {} 
        for record in data.values:
            #eid = record[data.get_field_id('planid')]
            eid = record[0]
            k = record[data.get_field_id('k')]
            v = record[data.get_field_id('v')]
            v = self.transformations.encode(v)
            v = self.transformations.regex_extract(k,v)
            if self.transformations.get_type(k) == 'list':
                e[eid] = e.get(eid, {
                    'id': eid
                })
                e[eid][k] = e[eid].get(k, [])
                e[eid][k].append(v)
            elif self.transformations.get_type(k) == 'map':
                e[eid] = e.get(eid, {
                    'id': eid
                })
                template = self.transformations.get_template(k)
                sub_k_name = self.transformations.get_sub_key(k) 
                sub_k = record[data.get_field_id(sub_k_name)]
                e[eid][k] = e[eid].get(k, template)
                if not template:
                    e[eid][k][sub_k] = v
                else: 
                    sub_k = type(template.keys()[0])(sub_k)
                    if sub_k in e[eid][k].keys():
                        e[eid][k][sub_k] = type(template[sub_k])(v)
            else:
                e[eid] = e.get(eid, {
                    'id': eid
                })
                regex_str = self.transformations.get_regex(k)
                e[eid][k] = v
        return e
     
    def package_entities(self, entities):
        e = PluginsData()
        allsqlfields = self.transformations.get_all_sql_fields()
        subsqlfields = self.transformations.get_sql_fields()
        e.fields = allsqlfields
        e.values = []
        for eid in entities:
            eid_str = str(eid)
            try:
                ejson_str = json.dumps(entities[eid])
            except:
                print entities[eid]
                raise
            v = [eid_str] + [
                entities[eid].get(sqlfield, '')
                for sqlfield in subsqlfields
            ] + [ejson_str]
            e.values.append(tuple(v))
        return e

    def load_data(self, rule):
        self.db = DB(config=rule['source_node'])
        sql_str = self.get_sql(rule)
        #self.print_debug(sql_str)
        data_item = PluginsData()
        self.db.execute(sql_str)
        data_item.fields = DB.field_names(self.db.cursor)
        data_item.values = self.db.cursor.fetchall()
        self.print_debug('Loaded {0} rows'.format(
                len(data_item.values)
            )
        ) 
        return data_item
    
   
    def run(self, rule, data=None):
        data = self.load_data(rule)
        first_field = data.fields[0]
        last_field = 'json'
        self.load_transformations(rule, first_field, last_field)
        e = self.make_entities(data)
        return self.package_entities(e)

def init(rule):
    return JsonizerPlugin(rule)
