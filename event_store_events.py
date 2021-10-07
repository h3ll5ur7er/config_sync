from typing import Optional
from datetime import datetime as dt
from pydantic import BaseModel
from settings import DEFAULT_HASH
class Event(BaseModel):
    __args__ = ["key", "value"]

    type:str = None
    key:Optional[str] = None
    value:Optional[str] = None
    index:Optional[int] = None
    timestamp:Optional[dt] = None
    hash:Optional[str] = None

    def __init__(self, key:str=None, value:str=None, timestamp:dt=None, hash:str=None, index:int=None, *a, **kw):
        super().__init__(key=key, value=value, timestamp=timestamp, hash=hash, index=index, *a, **kw)
        self.key = key
        self.value = value
        self.timestamp = timestamp if timestamp else dt.now()
        self.hash = hash if hash else None

    def apply(self, state:dict) -> dict:
        # if self.type == "AddEvent":
        #     AddEvent.apply(self, state)
        # elif self.type == "DeleteEvent":
        #     DeleteEvent.apply(self, state)
        if self.type == "ModifyEvent":
            ModifyEvent.apply(self, state)
        else:
            raise NotImplementedError("Event.apply() must be implemented")

    def __str__(self) -> str:
        arguments = [f"{arg}={getattr(self, arg)}" for arg in Event.__args__ if hasattr(self, arg) and getattr(self, arg)]
        return f"{self.type}({', '.join(arguments)})"

    def __repr__(self) -> str:
        return f"{self} | {self.hash} | {self.timestamp}"


# class AddEvent(Event, BaseModel):
#     type = "AddEvent"
#     def apply(self, state:dict) -> dict:
#         state[self.key] = self.value

class ModifyEvent(Event, BaseModel):
    type = "ModifyEvent"
    def apply(self, state:dict) -> dict:
        state[self.key] = self.value

class RootEvent(Event, BaseModel):
    type = "RootEvent"
    def __init__(self):
        super().__init__(key=None, value=None, timestamp=None, hash=DEFAULT_HASH, index=None)
    def apply(self, state:dict) -> dict:
        pass

# class DeleteEvent(Event, BaseModel):
#     type = "DeleteEvent"
#     def apply(self, state:dict) -> dict:
#         del state[self.key]

