import os
from typing import List, Optional
from helpers import Singleton
from datetime import datetime as dt
from pydantic import BaseModel
from settings import DEFAULT_HASH

class Client(BaseModel):
    ip:Optional[str] = None
    hash:Optional[str] = None
    active:Optional[bool] = True
    last_seen:Optional[dt] = None
    def probe(self):
        self.active = os.system("ping -c 1 " + self.ip) is 0
    def __str__(self) -> str:
        return f"{1 if self.active else 0} {self.hash} {self.ip}\t{self.last_seen}"

class ClientRepository(metaclass=Singleton):
    def __init__(self):
        self._clients = {}

    def add_client(self, ip:str, hash:str=DEFAULT_HASH):
        if ip not in self._clients:
            client = Client(ip=ip, hash=hash, last_seen=dt.now(), active=True)
            self._clients[ip] = client
        else:
            if hash != DEFAULT_HASH:
                self._clients[ip].hash = hash
                self._clients[ip].last_seen = dt.now()

    def clients(self) -> List[Client]:
        return list(self._clients.values())

    def ips(self) -> List[str]:
        return [client.ip for client in self.clients()]

    def hashes(self) -> List[str]:
        return [client.hash for client in self.clients()]

    def active_clients(self) -> List[Client]:
        return [client for client in self.clients() if client.active]

    def active_ips(self) -> List[str]:
        return [client.ip for client in self.active_clients()]
    
    def active_hashes(self) -> List[str]:
        return [client.hash for client in self.active_clients()]

    def __str__(self) -> str:
        return "\n".join(map(str, self._clients.values()))


