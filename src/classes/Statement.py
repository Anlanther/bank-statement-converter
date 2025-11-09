from abc import ABC, abstractmethod
from typing import TypedDict


class NetPosition(TypedDict):
    date: str
    amount: str

class Statement(ABC):
    @abstractmethod
    def get_transactions(self, text: str) -> list:
        pass

    @abstractmethod
    def get_date(self, date: str) -> list:
        pass

    @abstractmethod
    def is_date(self, date: str) -> list:
        pass
    
    @abstractmethod
    def test_for_date(self, date: str) -> list:
        pass

    @abstractmethod
    def get_total(self, path: str, text: str) -> NetPosition:
        pass