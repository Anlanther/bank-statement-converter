from enums.Bank import Bank

# from models import StatementClassDict
from .BOCStatement import BOCStatement
from .CitiStatement import CitiStatement
from .HSBCOneStatement import HSBCOneStatement
from .HSBCStatement import HSBCStatement
from .HSStatement import HSStatement
from .SCStatement import SCStatement
from .Statement import Statement


class StatementFactory:
    @staticmethod
    def create_statement(statement_type: Bank) -> Statement:
        statement_map = {
        Bank.HSBC: HSBCStatement,
        Bank.HSBC_ONE: HSBCOneStatement,
        Bank.SC: SCStatement,
        Bank.BOC: BOCStatement,
        Bank.CITI: CitiStatement,
        Bank.HS: HSStatement,
        }    
        return statement_map[statement_type]()