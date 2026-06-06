from typing import TypedDict


class StatementRow(TypedDict):
    date: str
    balance: str
    amount: str
    details: str
    unfinished_flag: bool