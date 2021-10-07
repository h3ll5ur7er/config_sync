from abc import ABC, abstractmethod
from typing import List
from event_store_comparison_result import ComparisonResult
from event_store_events import Event
from event_store_model import EventStoreModel

class EventStoreInterface(ABC):
    @abstractmethod
    def add_event(self, event:Event) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_hash(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def delta_to(self, target_hash:str) -> List[Event]:
        raise NotImplementedError

    @abstractmethod
    def aggregate(self, target_hash:int=None) -> dict:
        raise NotImplementedError

    @abstractmethod
    def compress(self, target_hash:int=None) -> None:
        raise NotImplementedError

    @abstractmethod
    def compare_event_store(self, other:'EventStoreInterface') -> ComparisonResult:
        raise NotImplementedError

    @abstractmethod
    def compare_hash(self, other:str) -> ComparisonResult:
        raise NotImplementedError

    @abstractmethod
    def load(self, event_store:EventStoreModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, event_store:EventStoreModel) -> None:
        raise NotImplementedError

