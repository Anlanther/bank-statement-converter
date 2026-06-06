import re
from datetime import datetime

from .Statement import Statement


class HSBCOneStatement(Statement):
    def __init__(self):
        self.date_format = '([0-9]{2}|[0-9]) [a-zA-Z]{3}'
        self.adjusted_date_format = '%d-%b%Y'
        self.amount_in_first_row = False
    
    def get_transactions(self, text: str) -> list:
        list_of_values = self.get_rows_with_values(text)
        statement = self.remove_page_brake(list_of_values)
        
        return statement
    
    def get_rows_with_values(self, text):
        start_identifier = 'B/F BALANCE'
        end_identifier_if_current_exists = 'C/F BALANCE'
        end_identifier_if_time_depo_exits = 'Time Deposits'
        end_identifier_default = 'Total Relationship Balance'
        
        start = next((i for i, s in enumerate(text.split("\n")) if start_identifier in s), None)
        
        if end_identifier_if_current_exists in text:
            end = next((i for i, s in reversed(list(enumerate(text.split("\n")))) if end_identifier_if_current_exists in s), None)
        elif end_identifier_if_time_depo_exits in text:
            end = next((i for i, s in reversed(list(enumerate(text.split("\n")))) if end_identifier_if_time_depo_exits in s), None)
        else:
            end = next((i for i, s in reversed(list(enumerate(text.split("\n")))) if end_identifier_default in s), None)
        
        statement = [row.replace(",", "") for row in text.split("\n")[start:end-1]]
        return statement
    
    def remove_page_brake(self, text):
        page_brake_identifier = 'The Hongkong and Shanghai Banking Corporation'
        end_page_brake_identifier = 'Date'
        joint_text = " ".join(text)
        
        if (page_brake_identifier not in joint_text):
            return text
        
        start_index = next(i for i, s in enumerate(text) if page_brake_identifier in s)
        end_index = next(i for i, s in enumerate(text) if end_page_brake_identifier in s)

        adjusted_transactions = text[:start_index] + text[end_index + 1:]
        return adjusted_transactions

    def adjust_year(self, line, invoice_name):
        line_has_date = self.test_for_date(line)       
       
        if line_has_date:
            double_digit_date = re.search('[0-9]{2} [a-zA-Z]{3}', line[:6])
            if double_digit_date:
                line = line[:2] + '-' + line[3:]
            else:
                line = line[:1] + '-' + line[2:]
        
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
        start_identifier = 'Net Position'
        line_with_amount = next(s for s in text.split("\n") if start_identifier in s)
        amount = float(line_with_amount.split(' ')[-1].replace(',', ''))
        statement_date = re.search(r'(\d{4}-\d{2})', path).group(1)
        
        return {'date': statement_date, 'amount': amount}