from pathlib import Path
from json import loads



class Dict(dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.__dict__ = self
    
    def __getattribute__(self, name: str):
        try:
            if isinstance(name, str):
                return super().__getattribute__(name)
        except AttributeError:
            pass




class JsonParser:
    data = Path(r'assets\data\settings.json')

    json_file = open(data, 'r', encoding='utf-8').read()
    config = loads(json_file, object_hook=lambda dict: Dict(**dict))

    def __new__(cls):
        return cls.config
