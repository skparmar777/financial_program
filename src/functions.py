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
# Files
EMPLOYEE_FILE = "../data/employees.csv"
CUSTOMER_FILE = "../data/customers.csv"
VENDOR_FILE = "../data/vendors.csv"
INCOME_STMT = "../data/income_statement.csv"
BALANCE_SHT = "../data/balance_sheet.json"
PAYMENT_HIST = "../data/payroll_history.csv"
PO_HIST = "../data/po_hist.csv"
INVENTORY_FILE = "../data/inventory.csv"

# Tax Info
STATE_TAX = .0495
SSN_TAX = .062
MEDICARE_TAX = .0145

# Inventory limit
INVENTORY = 10000

PARTS = {"Wheels": 0.01, "Windshield Glass": 0.05, 'Interior': 0.05,
         'Tank': 0.10, 'Axles': 0.01, 'Cab': 0.10, 'Body': 0.10, 'Box': 0.05}

# TODO figure out rest of income statement/balance sheet
class func(enum.Enum):
    view_emp = 1
    add_emp = 2
    pay_emp = 3
    view_cust = 4
    add_cust = 5
    view_vendor = 6
    add_vendor = 7
    view_payroll = 8
    create_invoice = 9  # TODO
    invoice_hist = 10  # TODO
    create_PO = 11
    PO_hist = 12
    balance_st = 13
    income_stmt = 14
    inventory = 15


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
    elif salary <= 518400:
        return .35
    else:
        return .37


def calculate_trucks(df):
    # 8 wheels, 1 windshield glass, 1 interior, 1 tank, 4 axles, 1 cab, 1 body, 1 box
    curr_wheels = df[df.Part == 'Wheels'].Quantity.iloc[0]
    curr_glass = df[df.Part == 'Windshield Glass'].Quantity.iloc[0]
    curr_interior = df[df.Part == 'Interior'].Quantity.iloc[0]
    curr_tank = df[df.Part == 'Tank'].Quantity.iloc[0]
    curr_axles = df[df.Part == 'Axles'].Quantity.iloc[0]
    curr_cab = df[df.Part == 'Cab'].Quantity.iloc[0]
    curr_body = df[df.Part == 'Body'].Quantity.iloc[0]
    curr_box = df[df.Part == 'Box'].Quantity.iloc[0]

    empty = False
    trucks = 0
    while not empty:
        curr_wheels -= 8
        curr_glass -= 1
        curr_interior -= 1
        curr_tank -= 1
        curr_axles -= 4
        curr_cab -= 1
        curr_body -= 1
        curr_box -= 1
        if curr_wheels <= 0 or curr_glass <= 0 or curr_interior <= 0 \
                or curr_tank <= 0 or curr_axles <= 0 or curr_cab <= 0 \
                or curr_body <= 0 or curr_box <= 0:
            empty = True
        else:
            trucks += 1
    return trucks


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
    assets['Total Current Assets'] = assets['Cash'] + assets['Accounts Recievable'] + assets['Inventory']
    assets["Total Fixed Assets"] = assets["Land/Buildings"] + assets["Equipment"] + assets["Furnitures and Fixtures"]
    assets["Total Assets"] = assets["Total Fixed Assets"] + assets['Total Current Assets']

    liabilities["Total Current Liabilities"] = liabilities["Accounts Payable"] + \
                                               liabilities["Notes Payable"] + liabilities["Accruals"]
    liabilities["Total Liabilities"] = liabilities["Total Current Liabilities"] + \
                                       liabilities['Mortgage'] + liabilities['Total Long Term Debt']
    liabilities['Net Worth'] = assets["Total Assets"] - liabilities["Total Liabilities"]
    liabilities['Total Liabilities and Net Worth'] = liabilities["Total Liabilities"] + liabilities['Net Worth']

    asset_names = list(assets.keys())
    for idx in range(len(asset_names)):
        key = asset_names[idx]
        Label(newWindow, text=key).grid(row=(idx + 1), column=0)
        Label(newWindow, text=str(assets[key])).grid(row=(idx + 1), column=1)
    liability_names = list(liabilities.keys())
    for idx in range(len(liability_names)):
        key = liability_names[idx]
        Label(newWindow, text=key).grid(row=(idx + 1), column=2)
        Label(newWindow, text=str(liabilities[key])).grid(row=(idx + 1), column=3)


def process_emp_payment(employee, df, newWindow):
    print("in process emp payment)")
    emp_name = employee.get()
    full_salary = df[df.fullname == employee.get()].Salary.iloc[0]
    salary = full_salary / 365 * 14

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
                           'Federal_Tax_Withheld', 'State_Tax_Withheld', 'Social_Security', 'Medicare', 'Amount_Paid']
    payroll_hist_values = [today, emp_name, disbursement, withholding, full_salary, 0, fed_tax, state_tax, ssn,
                           medicare, disbursement]
    new_row = {}
    for idx in range(len(payroll_hist_labels)):
        new_row[payroll_hist_labels[idx]] = payroll_hist_values[idx]
    print(new_row)
    append_dict_as_row(PAYMENT_HIST, new_row, payroll_hist_labels)
    # TODO process info in balance sheet
    with open(BALANCE_SHT) as f:
        data = json.load(f)
    data['Assets']['Cash'] -= disbursement
    with open(BALANCE_SHT, 'w') as fp:
        json.dump(data, fp)
    # TODO income statement,
    income_statement_df = pd.read_csv(INCOME_STMT)
    curr_payroll = income_statement_df['Payroll'].iloc[0]
    curr_payroll += disbursement
    income_statement_df['Payroll'].iloc[0] = curr_payroll
    curr_withholding = income_statement_df['Payroll_Withholding'].iloc[0]
    curr_withholding += withholding
    income_statement_df['Payroll_Withholding'].iloc[0] = curr_withholding
    income_statement_df.to_csv(INCOME_STMT, index=False)
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


def process_po(variable, e1, newWindow):
    part_name = variable.get()
    quantity = int(e1.get())
    today = date.today()
    today = today.strftime("%m/%d/%y")

    vendor_df = pd.read_csv(VENDOR_FILE)
    supplier = vendor_df[vendor_df.Part == part_name]['Company_Name'].iloc[0]
    print(supplier)
    price = PARTS[part_name]
    print(quantity, type(quantity))
    total = quantity*price
    # TODO update history of POs
    labels = ['Date', 'Supplier', 'Part', 'Quantity', 'Price/Part', 'Total']
    values = [today, supplier, part_name, quantity, price, total]
    new_row = {}
    for idx in range(len(labels)):
        new_row[labels[idx]] = values[idx]
    print(new_row)
    append_dict_as_row(PO_HIST, new_row, labels)
    # TODO update inventory of parts
    inventory_df = pd.read_csv(INVENTORY_FILE)
    inventory_df['idx'] = inventory_df['Part'].copy()
    inventory_df.set_index("idx", inplace=True)
    print(inventory_df)
    curr_quantity = inventory_df[inventory_df.Part == part_name].Quantity.iloc[0]
    curr_quantity += quantity
    print("new quantity:", curr_quantity)
    inventory_df.loc[part_name, 'Quantity'] = curr_quantity
    print(inventory_df)
    inventory_df.Value = inventory_df.Quantity * inventory_df['Price/Unit']
    inventory_df.to_csv(INVENTORY_FILE, index=False)

    # TODO update balance sheet
    with open(BALANCE_SHT) as f:
        data = json.load(f)
    data['Liabilities & Net Worth']['Accounts Payable'] += total
    with open(BALANCE_SHT, 'w') as fp:
        json.dump(data, fp)
    newWindow.destroy()


def create_po(newWindow):
    newWindow.title("Create a Purchase Order")
    newWindow.geometry("300x600")
    Label(newWindow,
          text="Select Part:").grid(row=0)
    variable = StringVar(newWindow)
    variable.set("---")
    options = list(PARTS.keys())
    w = OptionMenu(*(newWindow, variable) + tuple(options))
    w.grid(row=1)
    Label(newWindow, text="Quantity").grid(row=2)
    e1 = Entry(newWindow)
    e1.grid(row=2, column=1)

    b1 = Button(newWindow, text="Submit Order",
                command=lambda: process_po(variable, e1, newWindow)).grid(row=3)


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
    elif label == 'Payroll History':
        total_expense = df['Disbursement'].sum()
        total_withheld = df['Witholding'].sum()
        Label(newWindow,
              text="Total Payroll Expenses: " + str(total_expense)).pack(side=TOP)
        Label(newWindow,
              text="Total Withheld: " + str(total_withheld)).pack(side=TOP)
    elif label == "Inventory":
        num_trucks = calculate_trucks(df)
        df['Reorder'] = np.where(df['Quantity'] < INVENTORY, 'X', " ")
        Label(newWindow,
              text="Total Complete Units that can be built with current inventory: " + str(num_trucks)).pack(side=TOP)

    f = Frame(newWindow)
    f.pack(fill=BOTH, expand=1)
    pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
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
          text=func).grid(row=0)
    entries = []
    for idx in range(len(labels)):
        Label(newWindow, text=labels[idx]).grid(row=idx + 1)
        e1 = Entry(newWindow)
        e1.grid(row=idx + 1, column=1)
        entries.append(e1)

    b1 = Button(newWindow, text=func,
                command=lambda: process_inputs(file, labels, entries, newWindow)).grid(row=len(labels) + 1)


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
    elif functionality == func.PO_hist:
        view(newWindow, "Purchase Order History", PO_HIST)
    elif functionality == func.inventory:
        view(newWindow, "Inventory", INVENTORY_FILE)
    elif functionality == func.create_PO:
        create_po(newWindow)
