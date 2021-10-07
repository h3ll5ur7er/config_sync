from typing import List, Generic, TypeVar
T = TypeVar('T')
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ListOperations(Generic[T]):
    @staticmethod
    def order_by(l:List[T], key:str) -> List[T]:
        return list(sorted(l, key=lambda entry: getattr(entry, key)))
