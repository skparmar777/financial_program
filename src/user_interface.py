from tkinter import *
import tkinter.font as font

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

        view_emp = Button(leftframe, text="View Employees")
        view_emp.pack(padx=pX, pady=pY)
        add_emp = Button(leftframe, text="Add Employees")
        add_emp.pack(padx=pX, pady=pY)

        pay_emp = Button(leftframe, text="Pay an Employee")
        pay_emp.pack(padx=pX, pady=pY)
        view_payroll = Button(leftframe, text="View Payroll Events")
        view_payroll.pack(padx=pX, pady=pY)

        view_cust = Button(rightframe, text="View Customers")
        view_cust.pack(padx=pX, pady=pY)
        add_cust = Button(rightframe, text="Add Customers")
        add_cust.pack(padx=pX, pady=pY)

        create_invoice = Button(bottomframe, text="Create Invoice")
        create_invoice.pack(padx=pX, pady=pY)
        invoice_hist = Button(bottomframe, text="Invoice History")
        invoice_hist.pack(padx=pX, pady=pY)

        view_vendors = Button(rightframe, text="View Vendors")
        view_vendors.pack(padx=pX, pady=pY)
        add_vendors = Button(rightframe, text="Add Vendors")
        add_vendors.pack(padx=pX, pady=pY)

        create_PO = Button(bottomframe, text="Create PO")
        create_PO.pack(padx=pX, pady=pY)
        PO_hist = Button(bottomframe, text="PO History")
        PO_hist.pack(padx=pX, pady=pY)

        balance_sheet = Button(frame4, text="Balance Sheet")
        balance_sheet.pack(padx=pX, pady=pY)
        income_statement = Button(frame4, text="Income Statement")
        income_statement.pack(padx=pX, pady=pY)

        inventory = Button(frame4, text="Inventory")
        inventory.pack(padx=pX, pady=pY)


        self.root.title("Test")
        self.root.mainloop()

if __name__ == '__main__':
    app = Financial_Application()