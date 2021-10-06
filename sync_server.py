from threading import Thread
from socketserver import UDPServer, BaseRequestHandler
from datetime import datetime as dt
from sync_client_repository import ClientRepository
from event_store import EventStoreManager
from sync_messages import MessageParser, DiscoveryMessage, DiscoveryAckMessage

class DiscoveryHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        try:
            message:DiscoveryMessage = MessageParser.parse(data)
            if message.HEADER == DiscoveryMessage.HEADER:
                ClientRepository().add_client(self.client_address[0], message.hash)
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
