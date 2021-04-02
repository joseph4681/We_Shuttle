from tkinter import *
import tkinter as tk


class DropDate:

    def __init__(self, parent):
        self.parent = parent
        self.year_options = []
        self.month_options = []
        self.date_options = []

        self.year_options_func()
        self.month_options_func()
        self.date_options_default_func()

        self.year_entered = IntVar()
        self.month_entered = IntVar()
        self.date_entered = IntVar()

        self.year_entered.set(self.year_options[0])
        self.month_entered.set(self.month_options[0])
        self.date_entered.set(self.date_options[0])

        self.year_l = Label(self.parent, text="Year", width=12, anchor=W)
        self.month_l = Label(self.parent, text="Month", width=12, anchor=W)
        self.date_l = Label(self.parent, text="Date", width=12, anchor=W)

        self.year_om = OptionMenu(self.parent, self.year_entered, *self.year_options,
                                  command=self.check_leap_year_func)
        self.month_om = OptionMenu(self.parent, self.month_entered, *self.month_options,
                                   command=self.check_leap_year_func)
        self.date_om = OptionMenu(self.parent, self.date_entered, *self.date_options)

    def year_options_func(self):
        for x in range(2020, 2030):
            self.year_options.append(x)

    def month_options_func(self):
        for x in range(1, 13):
            x = str(x).zfill(2)
            self.month_options.append(x)

    def date_options_func(self, is_leap_year):
        months_31 = [1, 3, 5, 7, 8, 10, 12]
        months_30 = [4, 6, 9, 11]

        if self.month_entered.get() == 2:
            if is_leap_year:
                self.date_options = []
                for x in range(1, 30):
                    x = str(x).zfill(2)
                    self.date_options.append(x)
                if self.date_options.count(str(self.date_entered.get()).zfill(2)) == 0:
                    self.date_entered.set(self.date_options[-1])
            else:
                self.date_options = []
                for x in range(1, 29):
                    x = str(x).zfill(2)
                    self.date_options.append(x)
                if self.date_options.count(str(self.date_entered.get()).zfill(2)) == 0:
                    self.date_entered.set(self.date_options[-1])
        else:
            if months_31.count(self.month_entered.get()) > 0:
                self.date_options = []
                for x in range(1, 32):
                    x = str(x).zfill(2)
                    self.date_options.append(x)
                if self.date_options.count(str(self.date_entered.get()).zfill(2)) == 0:
                    self.date_entered.set(self.date_options[-1])
            elif months_30.count(self.month_entered.get()) > 0:
                self.date_options = []
                for x in range(1, 31):
                    x = str(x).zfill(2)
                    self.date_options.append(x)
                if self.date_options.count(str(self.date_entered.get()).zfill(2)) == 0:
                    self.date_entered.set(self.date_options[-1])

        menu = self.date_om["menu"]
        menu.delete(0, END)
        for option in self.date_options:
            menu.add_command(label=option, command=tk._setit(self.date_entered, option))

    def date_options_default_func(self):
        for x in range(1, 32):
            x = str(x).zfill(2)
            self.date_options.append(x)

    def check_leap_year_func(self, event):
        leap_year = self.year_entered.get() % 4
        if leap_year == 0:
            self.date_options_func(True)
        else:
            self.date_options_func(False)

    def get_year(self):
        return self.year_entered.get()

    def get_month(self):
        return self.month_entered.get()

    def get_date(self):
        return self.date_entered.get()

    def set_default(self):
        self.year_entered.set(self.year_options[0])
        self.month_entered.set(self.month_options[0])
        self.date_entered.set(self.date_options[0])
