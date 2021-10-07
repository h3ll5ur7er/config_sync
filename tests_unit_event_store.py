import unittest
from event_store import EventStore
from event_store_events import AddEvent, DeleteEvent, ModifyEvent

class TestEventStore(unittest.TestCase):
    event_store: EventStore
    def setUp(self) -> None:
        self.event_store = self._generate_test_event_store()

    def _generate_test_event_store(self):
        store = EventStore()
        store.add_event(AddEvent("a", 1))
        store.add_event(AddEvent("b", 2))
        store.add_event(AddEvent("c", 3))
        store.add_event(ModifyEvent("b", 4))
        store.add_event(DeleteEvent("a"))
        return store

    def test_add_modify_delete_aggregate(self):
        value = self.event_store.aggregate()
        self.assertEqual(len(value), 2)
        self.assertIn("b", value)
        self.assertEqual(value["b"], 4)
        self.assertIn("c", value)
        self.assertEqual(value["c"], 3)

    def test_serialize_deserialize(self):
        serialized = self.event_store.serialize()
        print()
        print("serialized:")
        print(serialized)
        deserialized = self.event_store.deserialize(serialized)
        print()
        print("deserialized:")
        print(deserialized)
        self.assertEqual(self.event_store.get_hash(), deserialized.get_hash())

    def test_compress(self):
        value_before = self.event_store.aggregate()
        hash_before = self.event_store.get_hash()

        self.event_store.compress("1fa81afda2bdf9f499348a1f2673dce0")

        value_after = self.event_store.aggregate()
        hash_after = self.event_store.get_hash()

        self.assertDictEqual(value_before, value_after)
        self.assertEqual(hash_before, hash_after)


if __name__ == "__main__":
    unittest.main()