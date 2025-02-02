from typing import List, TypedDict


class StatementDict(TypedDict):
    Date: List[str]
    Transaction_Details: List[str]
    Amount: List[float]
    Balance: List[float]