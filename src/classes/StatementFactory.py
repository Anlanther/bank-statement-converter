from enums.Bank import Bank

# from models import StatementClassDict
from .BOCStatement import BOCStatement
from .HSBCOneStatement import HSBCOneStatement
from .HSBCStatement import HSBCStatement
from .SCStatement import SCStatement
from .Statement import Statement


class StatementFactory:
    @staticmethod
    def create_statement(statement_type: Bank) -> Statement:
        statement_map = {
        Bank.HSBC: HSBCStatement,
        Bank.HSBC_ONE: HSBCOneStatement,
        Bank.SC: SCStatement,
        Bank.BOC: BOCStatement
        }    
        return statement_map[statement_type]()