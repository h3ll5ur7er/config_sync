import fastapi
from fastapi.routing import APIRoute
from typing import List

from event_store_model import EventStoreModel
from event_store_manager import EventStoreManager
from event_store_mock_data import generate_events
from event_store_events import ModifyEvent
# from event_store_events import AddEvent, ModifyEvent, DeleteEvent

from sync_client_repository import Client, ClientRepository
from sync_server import SyncServer
from sync_client import SyncClient


app = fastapi.FastAPI()
sync_server = SyncServer()
sync_client = SyncClient()

@app.on_event("startup")
async def startup_event():
    sync_server.start()
    sync_client.start()
    await setup()

@app.get("/hash")
async def get_hash():
    return EventStoreManager().get_hash()

@app.get("/known_clients", response_model=List[Client])
async def known_clients():
    return ClientRepository().clients()

@app.get("/value")
async def get_all_values():
    return EventStoreManager().aggregate()

@app.get("/value/{key}")
async def read_entry(key:str):
    values = EventStoreManager().aggregate()
    if key not in values:
        return None
    return values[key]

@app.post("/value/{key}")
async def create_entry(key:str, value:str):
    EventStoreManager().add_event(ModifyEvent(key, value))
    # EventStoreManager().add_event(AddEvent(key, value))
    return EventStoreManager().get_hash()

@app.put("/value/{key}")
async def update_entry(key:str, value:str):
    EventStoreManager().add_event(ModifyEvent(key, value))
    return EventStoreManager().get_hash()

@app.delete("/value/{key}")
async def delete_entry(key:str):
    EventStoreManager().add_event(ModifyEvent(key, None))
    # EventStoreManager().add_event(DeleteEvent(key))
    return EventStoreManager().get_hash()

@app.post("/compress/{target_hash}")
async def compress(target_hash:str):
    EventStoreManager().compress(target_hash)
    return EventStoreManager().get_hash()

@app.get("/serialize", response_model=EventStoreModel)
async def serialize():
    return EventStoreManager().serialize()

@app.post("/compare/event_store")
async def compare_event_store(serialized:EventStoreModel):
    other = EventStoreManager().deserialize(serialized)
    return EventStoreManager().compare_event_store(other)

@app.post("/compare/hash/{hash}")
async def compare_hash(hash:str):
    return EventStoreManager().compare_hash(hash)

@app.post("/load")
async def load(serialized:EventStoreModel):
    EventStoreManager().load(serialized)
    return EventStoreManager().get_hash()

@app.post("/update")
async def update(serialized:EventStoreModel):
    EventStoreManager().update(serialized)
    return EventStoreManager().get_hash()

@app.post("/setup")
async def setup():
    generate_events()
    return EventStoreManager().get_hash()

for route in app.routes:
    if isinstance(route, APIRoute):
            route.operation_id = route.name
