import tkinter as tk
from tkinter import END, ttk

from constants import ALL_DAYS, ALL_MONTH, ALL_RECORDS, ALL_YEARS
from saveload import reading_data_from_file, writing_data_to_file
from validators import vallide_bday, correct_phone

# create main window

root = tk.Tk()
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)
root.title("Notebook")
root.geometry("725x500+300+100")
root.config(bg="#eadcc6")
root.resizable(False, False)

# table for elemets phone book

columns = ("Name", "Phone", "Birthday")
all_contacts = ttk.Treeview(columns=columns, show="headings")
all_contacts.grid(row=1, rowspan=5, column=1, columnspan=3, sticky="ns")


def sort():
    rows = [(all_contacts.set(item, 'Name').lower(), item)
            for item in all_contacts.get_children('')]
    rows.sort()

    for index, (values, item) in enumerate(rows):
        all_contacts.move(item, '', index)


all_contacts.heading("Name", text="Name (press to abc sorting)", command=sort)

all_contacts.heading("Phone", text="Phone")
all_contacts.heading("Birthday", text="Birthday")

# def sort():
#     rows = [(all_contacts.set(item, 'Name').lower(), item) for item in all_contacts.get_children('')]
#     rows.sort()

#     for index, (values, item) in enumerate(rows):
#         all_contacts.move(item, '', index)


title_phonebook = tk.Label(
    root, bg="#eadcc6", text="You Phone Book", font=("Times new roman", 20, "italic")
).grid(row=0, column=1, columnspan=2, sticky="we")

# data recovery after restart


def recreate_table(ALL_RECORDS):
    new_records = reading_data_from_file()
    if new_records:
        for el in new_records:
            ALL_RECORDS.append(el)
        for el in ALL_RECORDS:
            record = (el["name"], el["phone"], el["birthday"])
            all_contacts.insert("", END, values=record)


recreate_table(ALL_RECORDS)

# button and function for adding new contact to phone book


def add_contact():

    win = tk.Tk()
    win.resizable(False, False)
    win.geometry("220x130+550+350")
    win.title("add")

    tk.Label(win, text="Name", font=(
        "Times new roman", 12)).grid(row=0, column=0)

    name = tk.Entry(win)
    name.grid(row=0, column=1)

    tk.Label(win, text="Phone", font=(
        "Times new roman", 12)).grid(row=1, column=0)

    phone = tk.Entry(win)
    phone.grid(row=1, column=1)
    phone.insert(0, "+")

    def yes_add():
        person = {"name": name.get(), "phone": [
            correct_phone(phone.get())], "birthday": "-"}
        ALL_RECORDS.append(person)

        record = (person["name"], person["phone"], person["birthday"])
        all_contacts.insert("", END, values=record)
        win.destroy()

    def exit():
        win.destroy()

    tk.Button(win, text="Exit", width=10, height=4, command=exit).grid(
        row=2, column=0, padx=5, pady=5
    )

    tk.Button(win, text="OK", width=10, height=4, command=yes_add).grid(
        row=2, column=1, padx=5, pady=5
    )


button_add_contact = tk.Button(
    root,
    command=add_contact,
    text="Add contact",
    font=("Times new roman", 10),
    width=14,
    height=6,
).grid(row=1, column=0)

# decoration element for separate buttons group

line = tk.Label(root, text="", bg="#eadcc6").grid(row=2, column=0)

# button and function for adding new phone number to contact in phone book


def add_phone():
    try:
        item = all_contacts.selection()[0]
        name = all_contacts.item(item)["values"][0]

        win_add = tk.Tk()
        win_add.resizable(False, False)
        win_add.geometry("170x190+550+350")
        win_add.title("add phone")

        tk.Label(
            win_add,
            font=("Times new roman", 12),
            text=f"""
Enter new phone for
{name}""",
        ).grid(row=0, column=0, columnspan=2)

        new_phone = tk.Entry(win_add)
        new_phone.grid(padx=15, pady=15, row=1, column=0, columnspan=2)
        new_phone.insert(0, "+")

        def exit():
            win_add.destroy()

        tk.Button(win_add, text="Exit", width=8, height=3, command=exit).grid(
            row=2, column=0
        )

        def adding_phone():
            for el in ALL_RECORDS:
                if el["name"] == name:
                    el["phone"].append(correct_phone(new_phone.get()))

                    changed_contact = (el["name"], el["phone"], el["birthday"])
                    all_contacts.delete(item)
                    all_contacts.insert("", END, values=changed_contact)
                    win_add.destroy()

        tk.Button(win_add, text="Ok", width=8, height=3, command=adding_phone).grid(
            row=2, column=1
        )

    except IndexError:
        error_win = tk.Tk()
        error_win.resizable(False, False)
        error_win.geometry("150x120+550+350")
        error_win.title("error")

        tk.Label(
            error_win,
            text="""Select one contact,
    before use this function""",
        ).grid()

        def exit_error():
            error_win.destroy()

        tk.Button(error_win, text="Ok", width=10,
                  height=4, command=exit_error).grid()


button_add_phone = tk.Button(
    root,
    command=add_phone,
    text="Add phone",
    font=("Times new roman", 10),
    width=14,
    height=6,
).grid(row=3, column=0)

# button and function for delete phone numer to contact in phone book


def delete_phone():
    try:
        item = all_contacts.selection()[0]
        name = all_contacts.item(item)["values"][0]
        phones = [(all_contacts.item(item)["values"][1])]
        for el in phones:
            if type(el) is int:
                new_list_phones = el
            if type(el) is str and " " in el:
                new_list_phones = el.split()
            else:
                new_list_phones = el

        win_del = tk.Tk()
        win_del.resizable(False, False)
        win_del.geometry("185x190+550+350")
        win_del.title("del phone")

        tk.Label(
            win_del,
            font=("Times new roman", 12),
            text=f"""
Select phone 
{name}
to delete""",
        ).grid(row=0, column=0, columnspan=2, rowspan=3, padx=20)

        phones_list = ttk.Combobox(win_del, values=new_list_phones)
        phones_list.grid(row=4, column=0, columnspan=2, padx=20)

        def exit():
            win_del.destroy()

        tk.Button(win_del, text="Exit", width=10, height=4, command=exit).grid(
            row=5, column=0, pady=10
        )

        def delete_num():
            num_to_del = phones_list.get()
            for el in ALL_RECORDS:
                if el["name"] == name:
                    if num_to_del in el["phone"]:
                        el["phone"].remove(num_to_del)

                        all_contacts.delete(item)
                        changed_contact = (
                            el["name"], el["phone"], el["birthday"])
                        all_contacts.insert("", END, values=changed_contact)
                        win_del.destroy()

    except IndexError:
        error_win = tk.Tk()
        error_win.resizable(False, False)
        error_win.geometry("150x120+550+350")
        error_win.title("error")

        tk.Label(
            error_win,
            text="""Select one contact,
    before use this function""",
        ).grid()

        def exit_error():
            error_win.destroy()

        tk.Button(error_win, text="Ok", width=10,
                  height=4, command=exit_error).grid()

    tk.Button(win_del, text="Ok", width=10, height=4, command=delete_num).grid(
        row=5, column=1, pady=10
    )


button_del_num = tk.Button(
    root,
    command=delete_phone,
    text="Delete phone",
    font=("Times new roman", 10),
    width=14,
    height=6,
).grid(row=4, column=0)

# button and function for add birthday date to contact in phone book


def add_birthday():
    try:
        item = all_contacts.selection()[0]
        name = all_contacts.item(item)["values"][0]

        birth_win = tk.Tk()
        birth_win.resizable(False, False)
        birth_win.geometry("220x205+550+350")
        birth_win.title("add birthday")

        tk.Label(
            birth_win,
            padx=10,
            font=("Times new roman", 12),
            text=f"""
Enter birthday for
{name}""",
        ).grid(row=0, column=0, columnspan=2)

        tk.Label(birth_win, text="Year", pady=2).grid(row=1, column=0)
        enter_year = ttk.Combobox(birth_win, values=ALL_YEARS)
        enter_year.grid(row=1, column=1)

        tk.Label(birth_win, text="Month", pady=2).grid(row=2, column=0)
        enter_month = ttk.Combobox(birth_win, values=ALL_MONTH)
        enter_month.grid(row=2, column=1)

        tk.Label(birth_win, text="Day", pady=2).grid(row=3, column=0)
        enter_day = ttk.Combobox(birth_win, values=ALL_DAYS)
        enter_day.grid(row=3, column=1)

        def exit():
            birth_win.destroy()

        tk.Button(birth_win, text="Exit", command=exit, width=7, height=3).grid(
            row=4, column=0, padx=5
        )

        def birth_for_record():
            date = f"{enter_day.get()} {enter_month.get()}, {enter_year.get()}"
            if vallide_bday(enter_day.get(), enter_month.get(), enter_year.get()):
                for el in ALL_RECORDS:
                    if el["name"] == name:
                        el["birthday"] = date

                        all_contacts.delete(item)
                        changed_contact = (
                            el["name"], el["phone"], el["birthday"])
                        all_contacts.insert("", END, values=changed_contact)
                        birth_win.destroy()
            else:
                error_win = tk.Tk()
                error_win.resizable(False, False)
                error_win.geometry("135x110+550+350")
                error_win.title("error")

                tk.Label(error_win, text="""Enter vallide date""").grid(padx=15)

                def exit_error():
                    error_win.destroy()

                tk.Button(
                    error_win, text="Ok", width=10, height=4, command=exit_error
                ).grid(padx=15)

        tk.Button(
            birth_win, text="Ok", width=7, height=3, command=birth_for_record
        ).grid(row=4, column=1, pady=5)

    except:
        error_win = tk.Tk()
        error_win.resizable(False, False)
        error_win.geometry("150x120+550+350")
        error_win.title("error")

        tk.Label(
            error_win,
            text="""Select one contact,
    before use this function""",
        ).grid()

        def exit_error():
            error_win.destroy()

        tk.Button(error_win, text="Ok", width=10,
                  height=4, command=exit_error).grid()


button_add_bday = tk.Button(
    root,
    text="Add birthday",
    font=("Times new roman", 10),
    command=add_birthday,
    width=14,
    height=6,
).grid(row=5, column=0)

# button and function for delete contact from phone book


def del_func():
    item = all_contacts.selection()[0]
    name = all_contacts.item(item)["values"][0]
    for el in ALL_RECORDS:
        if el["name"] == name:
            ALL_RECORDS.remove(el)
    all_contacts.delete(item)


delete_func = ttk.Button(
    text="del contact", command=del_func).grid(column=3, pady=10)

# mainloop

if __name__ == "__main__":
    try:
        root.mainloop()
    finally:
        writing_data_to_file()
