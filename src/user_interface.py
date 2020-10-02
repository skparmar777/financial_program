from tkinter import *
import tkinter.font as font
from functions import *

class Financial_Application:
    def __init__(self):
        self.root = Tk()
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>",
                         lambda event: self.root.attributes("-fullscreen",
                                    not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>",
                         lambda event: self.root.attributes("-fullscreen",
                                    False))

        frame = Frame(self.root)
        frame.pack()

        leftframe = Frame(self.root)
        leftframe.pack(side=LEFT)

        rightframe = Frame(self.root)
        rightframe.pack(side=LEFT)

        bottomframe = Frame(self.root)
        bottomframe.pack(side=LEFT)

        frame4 = Frame(self.root)
        frame4.pack(side=LEFT)

        title_font = font.Font(family='Helvetica', size=40, weight='bold')
        label = Label(frame, text="Welcome to your Financial Tracker!")
        label['font'] = title_font
        label.pack()
        pX = 100
        pY = 30

        view_emp = Button(leftframe, text="View Employees", command=lambda: openNewWindow(self.root, func.view_emp))
        view_emp.pack(padx=pX, pady=pY)
        add_emp = Button(leftframe, text="Add Employees", command=lambda: openNewWindow(self.root, func.add_emp))
        add_emp.pack(padx=pX, pady=pY)

        pay_emp = Button(leftframe, text="Pay an Employee", command=lambda: openNewWindow(self.root, func.pay_emp))
        pay_emp.pack(padx=pX, pady=pY)
        view_payroll = Button(leftframe, text="View Payroll Events", command=lambda: openNewWindow(self.root, func.view_payroll))
        view_payroll.pack(padx=pX, pady=pY)

        view_cust = Button(rightframe, text="View Customers", command=lambda: openNewWindow(self.root, func.view_cust))
        view_cust.pack(padx=pX, pady=pY)
        add_cust = Button(rightframe, text="Add Customers", command=lambda: openNewWindow(self.root, func.add_cust))
        add_cust.pack(padx=pX, pady=pY)

        create_invoice = Button(bottomframe, text="Create Invoice", command=lambda: openNewWindow(self.root, func.create_invoice))
        create_invoice.pack(padx=pX, pady=pY)
        invoice_hist = Button(bottomframe, text="Invoice History", command=lambda: openNewWindow(self.root, func.invoice_hist))
        invoice_hist.pack(padx=pX, pady=pY)

        view_vendors = Button(rightframe, text="View Vendors", command=lambda: openNewWindow(self.root, func.view_vendor))
        view_vendors.pack(padx=pX, pady=pY)
        add_vendors = Button(rightframe, text="Add Vendors", command=lambda: openNewWindow(self.root, func.add_vendor))
        add_vendors.pack(padx=pX, pady=pY)

        create_PO = Button(bottomframe, text="Create PO", command=lambda: openNewWindow(self.root, func.create_PO))
        create_PO.pack(padx=pX, pady=pY)
        PO_hist = Button(bottomframe, text="PO History", command=lambda: openNewWindow(self.root, func.PO_hist))
        PO_hist.pack(padx=pX, pady=pY)

        balance_sheet = Button(frame4, text="Balance Sheet", command=lambda: openNewWindow(self.root, func.balance_st))
        balance_sheet.pack(padx=pX, pady=pY)
        income_statement = Button(frame4, text="Income Statement", command=lambda: openNewWindow(self.root, func.income_stmt))
        income_statement.pack(padx=pX, pady=pY)

        inventory = Button(frame4, text="Inventory", command=lambda: openNewWindow(self.root, func.inventory))
        inventory.pack(padx=pX, pady=pY)


        self.root.title("Test")
        self.root.mainloop()

if __name__ == '__main__':
    app = Financial_Application()