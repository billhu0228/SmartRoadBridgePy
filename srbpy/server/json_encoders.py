import json

from srbpy.model import Model


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
            data2 = json.dumps(data)
            return data2
