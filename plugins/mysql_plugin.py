from plugins import BasePlugin
from plugins import PluginsData

from etllib.conf import Conf
from etllib.db import DB

class MySQLPlugin(BasePlugin):

    def field_names(self, cursor):
        if cursor.description:
            names = [item[0] for item in cursor.description]
        else:
            names = []
        return tuple(names)

    def run(self, rule, data=None):
        self.conf = Conf()
        if data:
            # Used as Egress 
            self.db = DB(config=rule['destination_node'])
            table = rule['destination_table']
            fields = ', '.join(data.fields)
            placeholders = ', '.join(['%s' for item in data.fields])
            values = data.values
            sql_str = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(
                table,
                fields, 
                placeholders
            )
            #print sql_str
            #print values[0:10]
            self.print_debug('SQL Insert: {0}'.format(sql_str))
            self.print_debug('SQL Values: {0}'.format(values[0:10]))
            self.db.executemany(sql_str, values, page_size=500)
        else:
            # Used as Ingress 
            self.db = DB(config=rule['source_node'])
            
            sql_cmds = [
                s + ';'
                for s in rule['action'].split(';') 
                if len(s.strip())
            ]

            ret_data = PluginsData()
            
            if not len(sql_cmds):
                # No SQL commands found
                # May be we should raise an exception
                raise Exception
            elif len(sql_cmds) == 1:
                # One SQL commands found
                sql_str = sql_cmds[0]
                self.db.execute(sql_str)
                ret_data.fields = DB.field_names(self.db.cursor)
                ret_data.values = self.db.cursor.fetchall()
                #self.db.cursor.close()
            else:
                # More than one SQL commands found
                # Execute commands, but return no data
                for sql_str in sql_cmds:
                    self.db.execute(sql_str)
                #self.db.cursor.close()
            return ret_data

def init(rule):
    return MySQLPlugin(rule)
