from time import sleep
from swagger_client import DefaultApi

CLIENT_0 = "http://localhost:8000"
CLIENT_1 = "http://192.168.1.103:8000"
if __name__ == '__main__':
    client0 = DefaultApi()
    client0.api_client.configuration.host = CLIENT_0

    client1 = DefaultApi()
    client1.api_client.configuration.host = CLIENT_1
def phase1():
    # Phase 1
    print("Phase 1")
    client0.delete_entry("c")

    sleep(10)

    print("Phase 1 - resolved")
    client1.delete_entry("c")

    sleep(10)
    
def phase2():
    # Phase 2
    print("Phase 2")
    client1.create_entry("c", "c")

    sleep(10)
    print("Phase 2 - resolved")
    client0.create_entry("c", "c")

    sleep(10)

def phase3():
    # Phase 3
    print("Phase 3")
    client0.create_entry("q", "w")
    client0.create_entry("a", "s")
    client1.create_entry("a", "s")
    client1.create_entry("q", "w")

# phase1()
# phase2()
phase3()