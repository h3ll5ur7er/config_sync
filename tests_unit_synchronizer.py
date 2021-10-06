import unittest
from datetime import datetime as dt
from sync_messages import DiscoveryMessage, DiscoveryAckMessage, MessageParser

class TestSynchronizer(unittest.TestCase):


    def test_discovery_message_serialization(self):
        test_timestamp = dt(2021, 1, 1, 1, 1, 1)
        test_hash = "test_hash"
        message = DiscoveryMessage(test_hash, test_timestamp)

        serialized = message.serialize()
        self.assertSequenceEqual(serialized[:2], DiscoveryMessage.HEADER)

        deserialized = DiscoveryMessage.deserialize(serialized[2:])
        self.assertLess(abs(test_timestamp.timestamp() - deserialized.timestamp.timestamp()), 1)
        self.assertEqual(test_hash, deserialized.hash)

        parsed = MessageParser.parse(serialized)
        self.assertLess(abs(test_timestamp.timestamp() - parsed.timestamp.timestamp()), 1)
        self.assertEqual(test_hash, parsed.hash)

    def test_discovery_ack_message_serialization(self):
        test_timestamp = dt(2021, 1, 1, 1, 1, 1)
        test_hash = "test_hash"
        test_known_clients = ["1.2.3.4", "123.123.123.123"]
        message = DiscoveryAckMessage(test_hash, test_known_clients, test_timestamp)

        serialized = message.serialize()
        self.assertSequenceEqual(serialized[:2], DiscoveryAckMessage.HEADER)

        deserialized = DiscoveryAckMessage.deserialize(serialized[2:])
        self.assertLess(abs(test_timestamp.timestamp() - deserialized.timestamp.timestamp()), 1)
        self.assertEqual(test_hash, deserialized.hash)
        self.assertSequenceEqual(test_known_clients, deserialized.known_clients)

        parsed = MessageParser.parse(serialized)
        self.assertLess(abs(test_timestamp.timestamp() - parsed.timestamp.timestamp()), 1)
        self.assertEqual(test_hash, parsed.hash)
        self.assertSequenceEqual(test_known_clients, parsed.known_clients)


if __name__ == "__main__":
    unittest.main()