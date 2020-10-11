from tkinter import *
import tkinter.font as font
import enum
import pandas as pd
import numpy as np
from pandastable import Table
from csv import DictWriter
import json
from datetime import date


"""
Global Variables
"""
EMPLOYEE_FILE = "../data/employees.csv"
CUSTOMER_FILE = "../data/customers.csv"
VENDOR_FILE = "../data/vendors.csv"
INCOME_STMT = "../data/income_statement.csv"
BALANCE_SHT = "../data/balance_sheet.json"
PAYMENT_HIST = "../data/payroll_history.csv"

STATE_TAX = .0495
SSN_TAX = .062
MEDICARE_TAX = .0145

class func(enum.Enum):
    view_emp = 1
    add_emp = 2
    pay_emp = 3 # TODO finish linking ot balance sheet/income statement
    view_cust = 4
    add_cust = 5
    view_vendor = 6
    add_vendor = 7
    view_payroll = 8
    create_invoice = 9  # TODO
    invoice_hist = 10  # TODO
    create_PO = 11  # TODO
    PO_hist = 12  # TODO
    balance_st = 13
    income_stmt = 14
    inventory = 15  # TODO

def get_national_tax_rate(salary):
    if salary <= 9876:
        return 0.10
    elif salary <= 40125:
        return 0.12
    elif salary <= 85525:
        return 0.22
    elif salary <= 163300:
        return 0.24
    elif salary <= 207350:
        return .32
    elif salary <=518400:
        return .35
    else:
        return .37

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as word in the csv
        dict_writer.writerow(dict_of_elem)

def balance_sheet(newWindow):
    with open(BALANCE_SHT) as f:
        data = json.load(f)

    assets = data["Assets"]
    liabilities = data['Liabilities & Net Worth']
    Label(newWindow, text="Assets").grid(row=0, column=0)
    Label(newWindow, text="Liabilities & Net Worth").grid(row=0, column=2)

    asset_names = list(assets.keys())
    for idx in range(len(asset_names)):
        key = asset_names[idx]
        Label(newWindow, text=key).grid(row=(idx+1), column=0)
        Label(newWindow, text=str(assets[key])).grid(row=(idx+1), column=1)
    liability_names = list(liabilities.keys())
    for idx in range(len(liability_names)):
        key = liability_names[idx]
        Label(newWindow, text=key).grid(row=(idx + 1), column=2)
        Label(newWindow, text=str(liabilities[key])).grid(row=(idx + 1), column=3)



def process_emp_payment(employee, df, newWindow):
    print("in process emp payment)")
    emp_name = employee.get()
    full_salary = df[df.fullname == employee.get()].Salary.iloc[0]
    salary = full_salary/365 * 14
    #TODO process info in balance sheet
    # TODO income statement,
    # TODO payroll history,
    today = date.today()
    today = today.strftime("%m/%d/%y")
    fed_tax = salary * get_national_tax_rate(full_salary)
    state_tax = salary * STATE_TAX
    ssn = salary * SSN_TAX
    medicare = salary * MEDICARE_TAX
    withholding = fed_tax + state_tax + ssn + medicare
    disbursement = salary - withholding
    payroll_hist_labels = ['Date_Paid', 'Employee', 'Disbursement', 'Witholding', 'Salary', 'Bounce',
                           'Federal_Tax_Withheld', 'State_Tax_Withheld','Social_Security','Medicare','Amount_Paid']
    payroll_hist_values = [today, emp_name, disbursement, withholding, full_salary, 0, fed_tax, state_tax, ssn, medicare, disbursement]
    new_row = {}
    for idx in range(len(payroll_hist_labels)):
        new_row[payroll_hist_labels[idx]] = payroll_hist_values[idx]
    print(new_row)
    append_dict_as_row(PAYMENT_HIST, new_row, payroll_hist_labels)
    # TODO expenses

    newWindow.destroy()


def pay_employee(newWindow):
    newWindow.title("Pay an Employee")
    newWindow.geometry("300x600")
    Label(newWindow,
          text="Choose an employee to pay and enter amount:").grid(row=0)
    variable = StringVar(newWindow)
    variable.set("---")
    df = pd.read_csv(EMPLOYEE_FILE)
    df["fullname"] = df['First_Name'] + ' ' + df['Last_Name']
    options = df.fullname.values.tolist()
    w = OptionMenu(*(newWindow, variable) + tuple(options))
    w.grid(row=1)

    b1 = Button(newWindow, text="Pay Employee",
                command=lambda: process_emp_payment(variable, df, newWindow)).grid(row=2)


def view(newWindow, label, file):
    # sets the title of the
    # Toplevel widget
    newWindow.title(label)

    # sets the geometry of toplevel
    newWindow.geometry("1000x600")
    Label(newWindow,
          text=label).pack()
    df = pd.read_csv(file)
    if label == "income_statement":
        cols = df.columns.tolist()
        df = df.replace(np.nan, '', regex=True)
        df = df.T
        df.insert(0, " ", cols)
    if label == 'Payroll History':
        total_expense = df['Disbursement'].sum()
        total_withheld = df['Witholding'].sum()
        Label(newWindow,
             text="Total Payroll Expenses: " + str(total_expense)).pack(side=TOP)
        Label(newWindow,
              text="Total Withheld: " + str(total_withheld)).pack(side=TOP)
    f = Frame(newWindow)
    f.pack(fill=BOTH, expand=1)
    pt = Table(f, dataframe=df,showtoolbar=True, showstatusbar=True)
    pt.show()

def process_inputs(file, field_names, entries, newWindow):
    new_row = {}
    for idx in range(len(field_names)):
        new_row[field_names[idx]] = entries[idx].get()
    append_dict_as_row(file, new_row, field_names)
    newWindow.destroy()

def add(newWindow, func, file):
    # sets the title of the
    # Toplevel widget
    newWindow.title(func)
    df = pd.read_csv(file)
    labels = df.columns.tolist()
    # sets the geometry of toplevel
    newWindow.geometry("300x600")
    Label(newWindow,
          text=func).grid(row = 0)
    entries = []
    for idx in range(len(labels)):
        Label(newWindow, text=labels[idx]).grid(row=idx + 1)
        e1 = Entry(newWindow)
        e1.grid(row=idx + 1, column=1)
        entries.append(e1)

    b1 = Button(newWindow, text=func,
                   command=lambda: process_inputs(file,labels, entries, newWindow)).grid(row=len(labels) + 1)

def openNewWindow(master, functionality):
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)

    if functionality == func.view_emp:
        view(newWindow, "View Employees", EMPLOYEE_FILE)
    elif functionality == func.add_emp:
        add(newWindow, "Add Employee", EMPLOYEE_FILE)
    elif functionality == func.view_cust:
        view(newWindow, "View Customers", CUSTOMER_FILE)
    elif functionality == func.add_cust:
        add(newWindow, "Add Customer", CUSTOMER_FILE)
    elif functionality == func.view_vendor:
        view(newWindow, "View Vendors", VENDOR_FILE)
    elif functionality == func.add_vendor:
        add(newWindow, "Add Vendor", VENDOR_FILE)
    elif functionality == func.pay_emp:
        pay_employee(newWindow)
    elif functionality == func.income_stmt:
        view(newWindow, 'income_statement', INCOME_STMT)
    elif functionality == func.balance_st:
        balance_sheet(newWindow)
    elif functionality == func.view_payroll:
        view(newWindow, 'Payroll History', PAYMENT_HIST)


