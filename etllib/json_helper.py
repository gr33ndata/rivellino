import json

class JSONHelper:

    def __init__(self):
        pass

    @classmethod
    def encode(cls, json_str):
        #print type(json_str)
        return unicode(json_str, errors='ignore').encode("utf-8")


    @classmethod
    def load(cls, json_str):
        return json.loads(json_str)

    @classmethod
    def traverse(cls, d, fields_str):
        if not d:
            return d 
        if not fields_str:
            return d
        fields = fields_str.split('.',1)
        if len(fields) != 2:
            return d.get(fields[0])
        field, rest = fields
        new_d = d.get(field, {})
        return cls.traverse(new_d, rest)