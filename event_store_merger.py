from typing import List, Tuple
from typing_extensions import Protocol
from event_store_interface import EventStoreInterface
from event_store_events import Event
from helpers import ListOperations

class EventStoreConflictResolver(Protocol):
    @staticmethod
    def resolve_conflict( left:EventStoreInterface, right:EventStoreInterface) -> Tuple[bool, List[Event]]:
        raise NotImplementedError()
    @staticmethod
    def is_applicable(left:EventStoreInterface, right:EventStoreInterface) -> bool:
        raise NotImplementedError()

class EqualResolver:
    @staticmethod
    def resolve_conflict(left:EventStoreInterface, right:EventStoreInterface) -> Tuple[bool, List[Event]]:
        if left.get_hash() == right.get_hash():
            return True, []
        return False, []
    @staticmethod
    def is_applicable(left:EventStoreInterface, right:EventStoreInterface) -> bool:
        return True

class TimestampResolver:
    @staticmethod
    def resolve_conflict( left:EventStoreInterface, right:EventStoreInterface) -> Tuple[bool, List[Event]]:
        return True, ListOperations.order_by(left + right, "timestamp")
    @staticmethod
    def is_applicable(left:EventStoreInterface, right:EventStoreInterface) -> bool:
        return True

class NoConflictResolver:
    @staticmethod
    def resolve_conflict(left:EventStoreInterface, right:EventStoreInterface) -> Tuple[bool, List[Event]]:
        right_keys = list(map(lambda e: e.key, right))
        conflict = False
        for key in map(lambda e: e.key, left):
            if key in right_keys:
                conflict = True
                break
        if conflict:
            return False, []
        return True, left + right
    @staticmethod
    def is_applicable(left:EventStoreInterface, right:EventStoreInterface) -> bool:
        return True

class ReorderResolver:
    @staticmethod
    def resolve_conflict(left:EventStoreInterface, right:EventStoreInterface) -> Tuple[bool, List[Event]]:
        return True, left + right
    @staticmethod
    def is_applicable(left:EventStoreInterface, right:EventStoreInterface) -> bool:
        return True


class EventStoreMerger:

    RESOLVERS = [
        TimestampResolver,
        NoConflictResolver,
        ReorderResolver,
    ]

    @staticmethod
    def update(this:EventStoreInterface, other:EventStoreInterface) -> None:
        missing = []
        more = []
        if this.get_hash() == other.get_hash():
            print(">this is in sync")
            return

        elif this.get_hash() in other.get_all_hashes():
            print(">this is older")
            missing = other.delta_to(this.get_hash())
            print(">>>missing:")
            for event in missing:
                print(Event.__str__(event))
            print()

        elif other.get_hash() in this.get_all_hashes():
            print(">this is newer")
            more = this.delta_to(other.get_hash())
            print(">>>more:")
            for event in more:
                print(Event.__str__(event))
            print()

        else:
            print(">this is diverging")
            print(">>self:  ", this.get_all_hashes())
            print(">>other: ", other.get_all_hashes())
            
            common = None
            for event in reversed(this.events):
                if event.hash in other.get_all_hashes():
                    common = event.hash
                    break
            if common is None:
                raise ValueError("No common hash")
            print(">>common: ", common)
            missing = other.delta_to(common)
            more = this.delta_to(common)
            print(">>>missing:")
            for event in missing:
                print(Event.__str__(event))
            print(">>>more:")
            for event in more:
                print(Event.__str__(event))
            print()
        merged = ListOperations.order_by(missing, "timestamp")  + ListOperations.order_by(more, "timestamp")
        print(">>>merged:")
        for event in merged:
            print(Event.__str__(event))
        # TODO: do better
        # if missing is not None:
        #     for event in missing:
        #         self.add_event(event)