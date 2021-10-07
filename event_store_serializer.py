
from event_store_model import EventStoreModel
from event_store_interface import EventStoreInterface

class EventStoreSerializer():
    @staticmethod
    def serialize(store:EventStoreInterface) -> EventStoreModel:
        events = store.events.copy()
        for index, event in enumerate(events):
            event.index = index
        return EventStoreModel(initial_state=store.state, initial_state_hash=store.state_hash, initial_state_timestamp=store.state_timestamp, events=events)
        
    @staticmethod
    def deserialize(data:EventStoreModel) -> EventStoreInterface:
        from event_store import EventStore
        es = EventStore()
        es.state = data.initial_state
        es.state_hash = data.initial_state_hash
        es.state_timestamp = data.initial_state_timestamp
        es.events = data.events
        return es

    @staticmethod
    def serialize_state(store:dict) -> str:
        aggregate = ""
        for key in sorted(store):
            aggregate += f"{key}:{store[key]}\n"
        return aggregate
