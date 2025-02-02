import pandas as pd
import pdfplumber

from classes import StatementFactory, Utils
from enums import Bank


def convert(invoices: str, bank: Bank) -> pd.DataFrame:
    """
    Extracts content from statement file and then converts it to a DataFrame.
    """
    statement_factory = StatementFactory.create_statement(bank)
    statement_dict = initialize_statement_dict()
    temp_row = initialize_temp_row()
        
    for invoice in invoices:
        text = extract_text_from_pdf(invoice)
        statement = statement_factory.get_transactions(text)
        prepare_statement_dict(statement_dict, temp_row, statement_factory, statement, invoice)
        clear_temp_row(temp_row)
        
    df = pd.DataFrame(statement_dict, columns=["Date", "Transaction_Details", "Amount", "Balance"])
    return df

def prepare_statement_dict(statement_dict, temp_row, factory, statement, invoice_name):
    for line in statement:
        items = factory.adjust_year(line, invoice_name).split()
        last_item_is_number = Utils.is_float(items[-1])
        details_entered_yet = temp_row["details"] != ""
        starts_with_date = factory.is_date(items[0])
        
        if factory.amount_in_first_row:
            if starts_with_date and last_item_is_number and not details_entered_yet:
                add_first_row_to_dic(temp_row, items, factory.get_date(items[0]))
            elif starts_with_date and last_item_is_number:
                amount_first_add_row_to_dict(statement_dict, temp_row, items, starts_with_date=True, date=factory.get_date(items[0]))
            elif not starts_with_date and last_item_is_number:
                amount_first_add_row_to_dict(statement_dict, temp_row, items, starts_with_date=False)
            elif not starts_with_date and not last_item_is_number:
                add_to_previous_details(temp_row, items)
                        
        else:
            if starts_with_date and last_item_is_number and not details_entered_yet:
                add_first_row_to_dic(temp_row, items, factory.get_date(items[0]))
            elif starts_with_date and last_item_is_number: 
                amount_last_add_row_to_dic(temp_row, statement_dict, items, starts_with_date=True, last_item_is_number=True, date=factory.get_date(items[0]))
            elif starts_with_date and not last_item_is_number: 
                amount_last_add_row_to_dic(temp_row, statement_dict, items, starts_with_date=True, last_item_is_number=False, date=factory.get_date(items[0]))
            elif not starts_with_date and last_item_is_number:
                amount_last_add_row_to_dic(temp_row, statement_dict, items, starts_with_date=False, last_item_is_number=True)
            elif not starts_with_date and not last_item_is_number:
                amount_last_add_row_to_dic(temp_row, statement_dict, items, starts_with_date=False, last_item_is_number=False)
        
    if factory.amount_in_first_row:
        enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], "", temp_row["balance"])

            
def add_to_previous_details(temp_row, items):    
    temp_row["details"] = temp_row["details"] + " " + " ".join(items)

def amount_first_add_row_to_dict(statement_dict, temp_row, items, starts_with_date, date=None):
    has_two_amounts = Utils.is_float(items[-2])
    
    if starts_with_date:
        add_new_date_transaction(statement_dict, temp_row, items, has_two_amounts, date)
    else:
        add_same_date_transaction(statement_dict, temp_row, items, has_two_amounts, False)

def amount_last_add_row_to_dic(temp_row, statement_dict, items, starts_with_date, last_item_is_number, date=None):
    if len(items) > 1: 
        has_two_amounts = Utils.is_float(items[-2])
    else:
        has_two_amounts = False
    
    if starts_with_date:
        temp_row["date"] = date

        if has_two_amounts:
            temp_row["balance"] = items[-1]
            temp_row["amount"] = items[-2]
            temp_row["details"] = " ".join(items[1:-2])
            enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])

        elif last_item_is_number:
            temp_row["amount"] = items[-1]
            temp_row["details"] = " ".join(items[1:-1])
            enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])

        else:
            temp_row["details"] = " ".join(items[1:])
            temp_row["amount"] = ""

    else:

        if has_two_amounts:
            temp_row["balance"] = items[-1]
            temp_row["amount"] = items[-2]
            temp_row["details"] = temp_row["details"] + " " + " ".join(items[0:-2])
            enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])
        
        elif last_item_is_number:            
            temp_row["amount"] = items[-1]

            if temp_row["unfinished-flag"] is True:
                temp_row["details"] = temp_row["details"] + " " + " ".join(items[0:-1])
                temp_row["unfinished-flag"] = False
            
            else:
                temp_row["details"] = " ".join(items[0:-1])

            enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])
        
        else:
            temp_row["amount"] = ""
            temp_row["details"] = " ".join(items)
            temp_row["unfinished-flag"] = True

def add_new_date_transaction(statement_dict, temp_row, items, has_two_amounts, date):
    enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])
    temp_row["date"] = date

    if has_two_amounts:
        temp_row["balance"] = items[-1]
        temp_row["amount"] = items[-2]
        temp_row["details"] = " ".join(items[1:-2])
    else:
        temp_row["amount"] = items[-1]
        temp_row["details"] = " ".join(items[1:-1])  

def add_same_date_transaction(statement_dict, temp_row, items, has_two_amounts, add_sub_balance):
    if add_sub_balance:
        enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], "")
    else:
        enter_row_into_statement_dict(statement_dict, temp_row["date"], temp_row["details"], temp_row["amount"], temp_row["balance"])

    if has_two_amounts:
        temp_row["balance"] = items[-1]
        temp_row["amount"] = items[-2]
        temp_row["details"] = " ".join(items[0:-2])
    else:
        temp_row["amount"] = items[-1]
        temp_row["details"] = " ".join(items[0:-1])  
    
def add_first_row_to_dic(temp_row, items, date):
    temp_row["date"] = date
    temp_row["details"] = " ".join(items[1:-1])
    temp_row["balance"] = items[-1].replace(",","")
    
def enter_row_into_statement_dict(statement_dict, date, details, amount, balance):
    statement_dict["Date"] += [date]
    statement_dict["Transaction_Details"] += [details]
    statement_dict["Amount"] += [amount]
    statement_dict["Balance"] += [balance]

def clear_statement_dict(statement_dict):
    statement_dict["Date"] = []
    statement_dict["Transaction_Details"] = []
    statement_dict["Amount"] = []
    statement_dict["Balance"] = []

def clear_temp_row(temp_row):
    temp_row["date"] = ""
    temp_row["balance"] = ""
    temp_row["amount"] = ""
    temp_row["details"] = ""

def extract_text_from_pdf(invoice):
    with pdfplumber.open(invoice) as pdf:
        return " ".join([content.extract_text(x_tolerance=1) for content in pdf.pages])

def initialize_statement_dict():
    return {
        "Date": [],
        "Transaction_Details": [], 
        "Amount": [],
        "Balance": [] 
    }

def initialize_temp_row():
    return {
        "date": "",
        "balance": "",
        "amount": "",
        "details": "",
        "unfinished_flag": False
    }