from tkinter import *
import tkinter.font as font
import enum
import pandas as pd
import numpy as np
from pandastable import Table
from csv import DictWriter

"""
Global Variables
"""
EMPLOYEE_FILE = "../data/employees.csv"
CUSTOMER_FILE = "../data/customers.csv"
VENDOR_FILE = "../data/vendors.csv"
INCOME_STMT = "../data/income_statement.csv"


class func(enum.Enum):
    view_emp = 1
    add_emp = 2
    pay_emp = 3
    view_cust = 4
    add_cust = 5
    view_vendor = 6
    add_vendor = 7
    view_payroll = 8
    create_invoice= 9
    invoice_hist = 10
    create_PO = 11
    PO_hist = 12
    balance_st = 13
    income_stmt = 14
    inventory = 15



def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

def process_emp_payment(employee, df, newWindow):
    emp_name = employee.get()
    print("var", employee.get())
    salary = df[df.fullname == employee.get()].Salary.iloc[0]
    print(salary)
    #TODO process info in balance sheet, income statement, payroll history, and expenses
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

        print(df)
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


