
from typing import List, Dict, Tuple

from datetime import datetime as dt

from event_store_comparison_result import ComparisonResult
from event_store_model import EventStoreModel
from event_store_events import Event, RootEvent
from event_store_interface import EventStoreInterface
from event_store_merger import EventStoreMerger
from event_store_serializer import EventStoreSerializer

from settings import HASH_ALGORITHM

class EventStore(EventStoreInterface):
    events:List[Event] = None
    state:Dict[str,str] = None
    state_hash:str = None
    state_timestamp:dt = None

    def __init__(self, state:dict=None, state_hash:str=None, state_timestamp:dt=None, events:List[Event]=None):
        self.events = [RootEvent()] if events is None else events
        self.state = {} if state is None else state
        self.state_hash = state_hash
        self.state_timestamp = state_timestamp

    def add_event(self, event:Event) -> int:
        state = self.aggregate()
        next_state = state.copy()
        event.apply(next_state)
        

        # prev_hash = self.events[-1].hash if len(self.events) > 0 else ""
        # hash_input = prev_hash + Event.__str__(event)
        hash_input = EventStoreSerializer.serialize_state(next_state)
        event.hash = HASH_ALGORITHM(hash_input.encode("utf-8")).hexdigest()
        self.events.append(event)
        return event.hash

    def __len__(self) -> int:
        return len(self.events)

    def get_all_hashes(self) -> List[str]:
        return [event.hash for event in self.events]

    def get_hash(self) -> str:
        if len(self.events) == 0:
            if self.state_hash is not None:
                return self.state_hash
            return None
        return self.events[-1].hash

    def get_by_hash(self, hash:str) -> Tuple[int, Event]:
        for index, event in enumerate(self.events):
            if event.hash == hash:
                return index, event
        raise ValueError("Invalid hash")

    def delta_to(self, target_hash:str) -> List[Event]:
        if target_hash not in self.get_all_hashes():
            raise ValueError("Invalid target hash")

        index, target_event = self.get_by_hash(target_hash)
        return self.events[index+1:]

    def aggregate(self, target_hash:int=None) -> dict:
        if target_hash is None:
            target_hash = self.events[-1].hash
        state = self.state.copy()
        for event in self.events:
            event.apply(state)
            if event.hash == target_hash:
                break
        return state

    def compress(self, target_hash:int=None) -> None:
        if len(self.events) == 0:
            return

        if target_hash is None:
            target_hash = self.events[-1].hash

        if target_hash not in self.get_all_hashes():
            raise ValueError("Invalid target hash")

        self.state = self.aggregate(target_hash)
        self.state_hash = target_hash

        done = target_hash == self.events[0].hash
        while not done:
            target_event = self.events.pop(0)
            self.state_timestamp = target_event.timestamp
            done = target_hash == self.events[0].hash
        target_event = self.events.pop(0)

    def __str__(self) -> str:
        nl = "\n"
        sep = "\n\t"
        return f"EventStore({sep}state:{self.state}, {sep}state_hash:{self.state_hash}, {sep}state_timestamp:{self.state_timestamp}{sep}{(sep.join(map(repr, self.events)))}{nl})"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EventStore):
            return False
        return o.get_hash() == self.get_hash()

    def compare_event_store(self, other:'EventStore') -> ComparisonResult:
        if self.get_hash() == other.get_hash():
            return ComparisonResult.EQUAL
        elif self.get_hash() in other.get_all_hashes():
            return ComparisonResult.OLDER
        elif other.get_hash() in self.get_all_hashes():
            return ComparisonResult.NEWER
        else:
            return ComparisonResult.DIVERGING

    def compare_hash(self, hash:str) -> ComparisonResult:
        if self.get_hash() == hash:
            return ComparisonResult.EQUAL
        elif hash in self.get_all_hashes():
            return ComparisonResult.NEWER
        else:
            return ComparisonResult.OLDER_OR_DIVERGING

    def update(self, other:'EventStore') -> None:
        EventStoreMerger.update(self, other)

    def load(self, event_store: EventStoreModel) -> None:
        pass
        # TODO: do better
        # if missing is not None:
        #     for event in missing:
        #         self.add_event(event)


        

