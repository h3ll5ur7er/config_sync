from datetime import datetime as dt
from typing import List, Dict, Optional
from pydantic.main import BaseModel
from event_store_events import Event

class EventStoreModel(BaseModel):
    initial_state:Optional[Dict[str,str]] = None
    initial_state_hash:Optional[str] = None
    initial_state_timestamp:Optional[dt] = None
    events:Optional[List[Event]] = None

