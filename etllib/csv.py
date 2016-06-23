class CSV:

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self, header=True):

        with open(self.filepath, 'r') as fd:
            fields = []
            values = []
            if header:
                fields = [
                    field.strip()
                    for field in fd.readline().split(',')
                ]
            for line in fd.readlines():
                line_array = [
                    item.strip()
                    for item in line.strip().split(',')
                ]
                values.append(tuple(line_array))
        
        return {
            'fields': fields, 
            'values': values
        }

    def write(self, lines):

        with open(self.filepath, 'w') as fd:
            for line in lines:
                fd.write(line)
        fd.close()
