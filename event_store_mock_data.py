
from event_store import EventStoreManager
from events import AddEvent, DeleteEvent, ModifyEvent

def generate_events():
    EventStoreManager().add_event(AddEvent("a", 1))
    EventStoreManager().add_event(AddEvent("b", 2))
    EventStoreManager().add_event(AddEvent("c", 3))
    EventStoreManager().add_event(ModifyEvent("b", 4))
    EventStoreManager().add_event(DeleteEvent("a"))