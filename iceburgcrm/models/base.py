from orator import Model
from orator import Collection

class BaseModel(Model):
    __hidden__ = [] 

    def to_dict(self):
        data = {}
        for key, value in self.get_attributes().items():
            if key not in self.__hidden__:
                if isinstance(value, Model):
                    data[key] = value.to_dict()
                elif isinstance(value, Collection):
                    data[key] = [item.to_dict() for item in value]
                else:
                    data[key] = value
        return data