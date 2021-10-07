
from event_store_manager import EventStoreManager
from event_store_events import ModifyEvent
# from event_store_events import AddEvent, DeleteEvent, ModifyEvent

def generate_events():
    # EventStoreManager().add_event(AddEvent("a", 1))
    EventStoreManager().add_event(ModifyEvent("a", 1))
    # EventStoreManager().add_event(AddEvent("b", 2))
    EventStoreManager().add_event(ModifyEvent("b", 2))
    # EventStoreManager().add_event(AddEvent("c", 3))
    EventStoreManager().add_event(ModifyEvent("c", 3))
    EventStoreManager().add_event(ModifyEvent("b", 4))
    # EventStoreManager().add_event(DeletaEvent("a"))
    EventStoreManager().add_event(ModifyEvent("a", None))