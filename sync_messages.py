from typing import List
from typing_extensions  import Protocol
from struct import pack, unpack
from event_store_manager import EventStoreManager
from datetime import datetime as dt

from sync_client_repository import ClientRepository
from settings import DEFAULT_HASH

# Interface
class SyncMessage(Protocol):
    HEADER:bytes = None
    def serialize(self) -> bytes:
        pass
    @staticmethod
    def deserialize(data:bytes) -> 'SyncMessage':
        pass
    def __str__(self) -> str:
        pass

# Implementations
class DiscoveryMessage:
    HEADER = b"\x48\xF0"
    hash:str = None
    timestamp:dt = None
    def __init__(self, hash:str=None, timestamp:dt=None):
        self.hash = hash
        self.timestamp = timestamp
        if self.hash is None:
            self.hash = EventStoreManager().get_hash()
            if self.hash is None:
                self.hash = DEFAULT_HASH
        if self.timestamp is None:
            self.timestamp = dt.now()

    def serialize(self) -> bytes:
        data = self.HEADER
        data += pack("<Q", int(self.timestamp.timestamp() * 1000))
        data += self.hash.encode("utf-8")
        return data

    @staticmethod
    def deserialize(data:bytes) -> 'DiscoveryMessage':
        timestamp = dt.fromtimestamp(unpack('<Q', data[:8])[0] // 1000)
        hash = data[8:].decode('utf-8')
        return DiscoveryMessage(hash, timestamp)
    def __str__(self) -> str:
        return f"DiscoveryMessage(hash={self.hash}, timestamp={self.timestamp})"

class DiscoveryAckMessage:
    HEADER = b"\x48\xF1"
    def __init__(self, hash:str=None, known_clients:List[str]=None, timestamp:dt=None):
        self.hash = hash
        self.timestamp = timestamp
        self.known_clients = known_clients
        if self.hash is None:
            self.hash = EventStoreManager().get_hash()
            if self.hash is None:
                self.hash = DEFAULT_HASH
        if self.timestamp is None:
            self.timestamp = dt.now()
        if self.known_clients is None:
            self.known_clients = ClientRepository().ips()

    def serialize(self) -> bytes:
        data = self.HEADER
        data += pack("<Q", int(self.timestamp.timestamp() * 1000))
        data += bytes([len(self.known_clients)])
        for ip in self.known_clients:
            data += bytes([int(digits) for digits in map(int,ip.split('.'))])
        data += self.hash.encode("utf-8")
        return data

    @staticmethod
    def deserialize(data:bytes) -> 'DiscoveryMessage':
        timestamp = dt.fromtimestamp(unpack('<Q', data[:8])[0] // 1000)
        known_clients = []
        length = data[8]
        for i in range(length):
            ip = ""
            for j in range(4):
                ip += str(data[9+i*4+j])
                if j != 3:
                    ip += "."
            known_clients.append(ip)
        hash = data[9+length*4:].decode('utf-8')
        return DiscoveryAckMessage(hash, known_clients, timestamp)
    def __str__(self) -> str:
        return "DiscoveryAckMessage(hash={}, timestamp={}, known_clients={})".format(self.hash, self.timestamp, self.known_clients)

# Parser
class MessageParser:
    @staticmethod
    def parse(data:bytes) -> SyncMessage:
        message_type = {
            DiscoveryMessage.HEADER: DiscoveryMessage,
            DiscoveryAckMessage.HEADER: DiscoveryAckMessage
        }.get(data[:2], None)
        if message_type is None:
            raise Exception("Unknown message type")
        return message_type.deserialize(data[2:])