from threading import Thread
from socketserver import UDPServer, BaseRequestHandler
from datetime import datetime as dt
from sync_client_repository import ClientRepository
from event_store_comparison_result import ComparisonResult
from event_store_manager import EventStoreManager
from sync_messages import MessageParser, DiscoveryMessage, DiscoveryAckMessage
from swagger_client import DefaultApi


def nop(*__,**___):
    pass

def synchronize(my_hash, old_hash, new_hash, client_endpoint):
    client = DefaultApi()
    client.api_client.configuration.host = f"http://{client_endpoint[0]}:8000"

    other_event_store = client.serialize()
    EventStoreManager().update(other_event_store)


    pass

class DiscoveryHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        client_ip = self.client_address[0]
        try:
            message:DiscoveryMessage = MessageParser.parse(data)
            if message.HEADER == DiscoveryMessage.HEADER:
                my_hash = EventStoreManager().get_hash()
                old_hash = ClientRepository()[client_ip]
                new_hash = message.hash
                ClientRepository().add_client(client_ip, new_hash)

                sync_handler = {
                    ComparisonResult.EQUAL: nop,
                    ComparisonResult.NEWER: nop,
                    ComparisonResult.OLDER_OR_DIVERGING: synchronize
                }.get(EventStoreManager().compare_hash(new_hash), nop)

                sync_handler(my_hash, old_hash, new_hash, self.client_address)

                ack_message = DiscoveryAckMessage(EventStoreManager().get_hash(), ClientRepository().active_ips())
                socket.sendto(ack_message.serialize(), self.client_address)
        except Exception as e:
            print("invalid message received: ", e)
            return

class SyncServer(Thread):
    def __init__(self, port:int=54321):
        super().__init__()
        self.port = port
        self.server = None
        self.daemon = True

    def run(self):
        self.server = UDPServer(('', self.port), DiscoveryHandler)
        print("starting listener on " + self.server.server_address[0] + ":" + str(self.server.server_address[1]))
        self.server.serve_forever()

def start():
    server = SyncServer(port=54321)
    server.start()

if __name__ == "__main__":
    start()
