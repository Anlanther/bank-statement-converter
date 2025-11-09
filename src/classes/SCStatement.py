import re
from datetime import datetime

from .Statement import Statement


class SCStatement(Statement):
    def __init__(self):
        self.date_format = '[0-9]{2} [a-zA-Z]{3}'
        self.adjusted_date_format = '%d-%b%Y'
        self.amount_in_first_row = True
        
    def get_transactions(self, text: str):
        start = next(i for i, s in enumerate(text.split("\n")) if 'BALANCE FROM PREVIOUS STATEMENT' in s)
        end = next(i for i, s in enumerate(text.split("\n")) if 'CLOSING BALANCE' in s)
        statement = [row.replace(",", "") for row in text.split("\n")[start:end+1]]
        return statement

    def adjust_year(self, line, invoice_name):
        line_has_date = self.test_for_date(line)
        
        if line_has_date:
            line = line[:2] + '-' + line[3:]

        invoice_is_jan = "-01." in invoice_name
        line_has_dec = "-Dec " in line
        year = invoice_name[invoice_name.rfind('/')+1:invoice_name.find('-')]

        if invoice_is_jan and line_has_dec:
            return line.replace("-Dec", f"-Dec{int(year) - 1}")
        elif not line_has_date:
            return line
        else:
            adjusted_date_with_year = f"{line.split()[0] + year} {' '.join(line.split()[1:])}"
            return adjusted_date_with_year
        
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

    def get_total(self, path: str, text: str):
        start_identifier = 'NET POSITION'
        line_with_amount = next(s for s in text.split("\n") if start_identifier in s)
        amount = float(line_with_amount.split(' ')[-1].replace(',', ''))
        statement_date = re.search(r'(\d{4}-\d{2})', path).group(1)
        
        return {'date': statement_date, 'amount': amount}