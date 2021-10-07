
from helpers import Singleton
from event_store import EventStore
from event_store_comparison_result import ComparisonResult
from event_store_events import Event
from event_store_model import EventStoreModel
from event_store_serializer import EventStoreSerializer

class EventStoreManager(metaclass=Singleton):
    event_store:EventStore = None
    def __init__(self):
        self.event_store = EventStore()

    def add_event(self, event:Event) -> int:
        return self.event_store.add_event(event)

    def get_hash(self) -> str:
        return self.event_store.get_hash()

    def aggregate(self, target_hash:int=None) -> dict:
        return self.event_store.aggregate(target_hash)

    def compress(self, target_hash:int=None) -> None:
        return self.event_store.compress(target_hash)

    def __str__(self) -> str:
        return str(self.event_store)

    def compare_event_store(self, other:EventStore) -> ComparisonResult:
        return self.event_store.compare_event_store(other)

    def compare_hash(self, other:str) -> ComparisonResult:
        return self.event_store.compare_hash(other)

    def serialize(self) -> EventStoreModel:
        return EventStoreSerializer.serialize(self.event_store)
    
    def deserialize(self, raw_data:EventStoreModel) -> EventStore:
        return EventStoreSerializer.deserialize(raw_data)

    def set_event_store(self, event_store:EventStore) -> None:
        self.event_store = event_store

    def load(self, event_store:EventStoreModel) -> None:
        other = self.deserialize(event_store)
        self.event_store = other

    def update(self, event_store:EventStoreModel) -> None:
        other = self.deserialize(event_store)
        self.event_store.update(other)

