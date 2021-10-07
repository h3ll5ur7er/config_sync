import socket
from typing import Callable
from time import sleep
from threading import Thread
from sync_client_repository import ClientRepository
from sync_messages import DiscoveryMessage, DiscoveryAckMessage, MessageParser
from datetime import datetime as dt, timedelta as td

class SyncClient(Thread):
    def __init__(self, port:int=54321, broadcast_addr:str="192.168.1.255", time_between_sync:td=td(seconds=10), time_between_retry:td=td(seconds=5), polling_interval_seconds:int=3):
        super().__init__()
        self.port = port
        self.broadcast_addr = broadcast_addr
        self.time_between_sync = time_between_sync
        self.time_between_retry = time_between_retry
        self.target_time = dt.now() - time_between_sync
        self.polling_interval_seconds = polling_interval_seconds
        self.daemon = True

    def _sync(self, message:bytes, response_handler:Callable[[bytes], None], read_timeout:int=5, buffer_size:int=1024) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        s.settimeout(read_timeout)

        s.sendto(message, (self.broadcast_addr, self.port))
        try:
            response_handler(s.recv(buffer_size))
            return True
        except socket.timeout:
            print("No server found")
            return False
        finally:
            s.close()

    def handle_discovery_ack(self, message:bytes) -> None:
        message = MessageParser.parse(message)
        for client in message.known_clients:
            ClientRepository().add_client(client)
        

    def start_sync(self) -> bool:
        message = DiscoveryMessage()
        return self._sync(message.serialize(), self.handle_discovery_ack)

    def run(self):
        while True:
            if dt.now() >= self.target_time:
                if self.start_sync():
                    self.target_time = dt.now() + self.time_between_sync
                else:
                    self.target_time = dt.now() + self.time_between_retry
            else:
                sleep(self.polling_interval_seconds)