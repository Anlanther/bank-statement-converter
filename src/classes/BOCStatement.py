import re
from datetime import datetime

from .Statement import Statement


class BOCStatement(Statement):
    def __init__(self):
        self.date_format = '[0-9]{4}/'
        self.adjusted_date_format = '%Y-%m-%d'
        self.amount_in_first_row = True
        
    def get_transactions(self, text: str):
        start = next(i for i, s in enumerate(text.split("\n")) if 'Balance Brought Forward' in s)
        end = next(i for i, s in enumerate(text.split("\n")) if 'Balance Carried Forward' in s)
        statement = [row.replace(",", "") for row in text.split("\n")[start:end+1]]
        return statement

    def adjust_year(self, line, invoice_name):
        line_has_date = self.test_for_date(line)
        
        if line_has_date:
            return line.replace("/", "-")

        return line
        
    def get_date(self, date):
        date = datetime.strptime(date, self.adjusted_date_format)
        return date
    
    def is_date(self, date):
        try:
            self.get_date(date)
            return True
        except ValueError:
            return False
        
    def test_for_date(self, line):
        date_in_line = re.search(self.date_format, line)
        
        return True if date_in_line else False