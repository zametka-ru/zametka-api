from abc import ABC

from typing import TypeVar, Union


class Event(ABC):
    pass


EventT = TypeVar("EventT", bound=Event)  # e.g Event1
EventsT = TypeVar("EventsT", bound=Union[Event])  # e.g Event1 | Event 2
