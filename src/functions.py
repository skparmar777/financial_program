from tkinter import *
import tkinter.font as font
import enum
import pandas as pd
import numpy as np
from pandastable import Table
from csv import DictWriter

EMPLOYEE_FILE = "../data/employees.csv"

class func(enum.Enum):
    view_emp = 1
    add_emp = 2
    pay_emp = 3

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

def view_employee(newWindow):
    # sets the title of the
    # Toplevel widget
    newWindow.title("View Employees")

    # sets the geometry of toplevel
    newWindow.geometry("1000x600")
    Label(newWindow,
          text="View Employees").pack()
    employees = pd.read_csv(EMPLOYEE_FILE)
    f = Frame(newWindow)
    f.pack(fill=BOTH, expand=1)
    pt = Table(f, dataframe=employees,showtoolbar=True, showstatusbar=True)
    pt.show()

def process_employee(field_names, entries, newWindow):
    new_emp = {}
    for idx in range(len(field_names)):
        new_emp[field_names[idx]] = entries[idx].get()
    append_dict_as_row(EMPLOYEE_FILE, new_emp, field_names)
    newWindow.destroy()

def add_employee(newWindow):
    # sets the title of the
    # Toplevel widget
    newWindow.title("Add Employee")

    # sets the geometry of toplevel
    newWindow.geometry("300x600")
    Label(newWindow,
          text="Add Employees").grid(row = 0)
    labels = ["First_Name", "Last_Name", "Address1", "Address2", "City", "State", "Zipcode", "SSN", "Withholdings", "Salary"]
    entries = []
    for idx in range(len(labels)):
        Label(newWindow, text=labels[idx]).grid(row=idx + 1)
        e1 = Entry(newWindow)
        e1.grid(row=idx + 1, column=1)
        entries.append(e1)

    b1 = Button(newWindow, text='Add Employee',
                   command=lambda: process_employee(labels, entries, newWindow)).grid(row=len(labels) + 1)

def openNewWindow(master, functionality):
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)

    if functionality == func.view_emp:
        view_employee(newWindow)
    elif functionality == func.add_emp:
        add_employee(newWindow)


