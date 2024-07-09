import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import databases
import customtkinter
import sqlite3
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
class IntermediatePage:
    def __init__(self, master):
        self.master = master
        self.master.title('Intermediate Page')
        self.master.geometry('400x200')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 14, 'bold')

        attendance_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Attendance",
                                                     command=self.open_attendance_page)
        attendance_button.place(x=50, y=30)

        salary_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Salary",
                                                 command=self.open_salary_page)
        salary_button.place(x=125, y=80)

        leave_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Apply for Leave",
                                               command=self.open_leave_page)
        leave_button.place(x=200, y=30)

        self.back_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Back to Login",
                                                   command=self.back_to_login)
        self.back_button.place(x=125, y=130)

    def back_to_login(self):
        self.master.destroy()
        root = customtkinter.CTk()
        login_page = LoginPage(root)
        root.mainloop()

    def open_attendance_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        employee_system = EmployeeManagementSystem(root, page_type="Attendance")
        root.mainloop()

    def open_salary_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        salary_page = SalaryPage(root)
        root.mainloop()

    def open_leave_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        leave_page = LeavePage(root)
        root.mainloop()

class SalaryPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Salary Page')
        self.master.geometry('600x400')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 14, 'bold')
        font2 = ('Arial', 12, 'bold')

        employee_names = [employee[1] for employee in databases.fetch_employees()]

        self.employee_label = customtkinter.CTkLabel(self.master, font=font1, text='Employee:', text_color='#fff',
                                                     bg_color="#161C25")
        self.employee_label.place(x=20, y=20)

        self.employee_combobox = ttk.Combobox(self.master, values=employee_names, font=font1, state="readonly")
        self.employee_combobox.place(x=200, y=20)

        self.salary_label = customtkinter.CTkLabel(self.master, font=font1, text='Salary:', text_color='#fff',
                                                   bg_color="#161C25")
        self.salary_label.place(x=20, y=80)

        self.salary_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                                   border_color='#0C9295', border_width=2, width=180)
        self.salary_entry.place(x=160, y=80)

        self.add_salary_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Add Salary",
                                                         command=self.add_salary)
        self.add_salary_button.place(x=30, y=120)

        self.update_salary_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Update Salary",
                                                            command=self.update_salary)
        self.update_salary_button.place(x=200, y=120)
        self.back_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Back to Intermediate",command=self.back_to_intermediate_page)

        self.back_button.place(x=400, y=120)



        self.salary_tree = ttk.Treeview(self.master, height=10, columns=('Employee', 'Salary'))
        self.salary_tree.column('#0', width=0, stretch=tk.NO)
        self.salary_tree.column('Employee', anchor=tk.CENTER, width=200)
        self.salary_tree.column('Salary', anchor=tk.CENTER, width=200)
        self.salary_tree.heading('Employee', text='Employee')
        self.salary_tree.heading('Salary', text='Salary')
        self.salary_tree.place(x=20, y=200)

        # Display initial employees
        self.display_employees()

    def add_salary(self):
        employee_name = self.employee_combobox.get()
        salary_amount = self.salary_entry.get()

        if not all((employee_name, salary_amount)):
            messagebox.showerror('Error', 'Please fill in all required fields.')
            return

        employee_id = databases.get_employee_id_by_name(employee_name)

        databases.insert_salary(employee_id, salary_amount)

        self.display_employees()

        self.employee_combobox.set('')
        self.salary_entry.delete(0, tk.END)

    def update_salary(self):
        selected_item = self.salary_tree.focus()

        if not selected_item:
            messagebox.showerror('Error', 'Please select an employee to update the salary.')
            return

        employee_id = self.salary_tree.item(selected_item)['values'][0]
        new_salary = self.salary_entry.get()

        if not new_salary:
            messagebox.showerror('Error', 'Please enter the new salary.')
            return

        databases.update_salary(employee_id, new_salary)

        self.display_employees()

        self.employee_combobox.set('')
        self.salary_entry.delete(0, tk.END)

    def display_employees(self):
        self.salary_tree.delete(*self.salary_tree.get_children())
        rows = databases.update_tree()  # Adjust this based on your implementation
        for i in rows:
            self.salary_tree.insert("", 'end', values=i)

    def back_to_intermediate_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        intermediate_page = IntermediatePage(root)
        root.mainloop()


class LeavePage:
    def __init__(self, master):
        self.master = master
        self.master.title('Leave Management')
        self.master.geometry('1200x500')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 20, 'bold')
        font2 = ('Arial', 16, 'bold')
        entry_width = 25
        vertical_padding = 15

        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
        style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.leave_tree = ttk.Treeview(self.master, height=15)
        self.leave_tree['columns'] = ('ID', 'Date', 'Starting Date', 'Ending Date', 'Leave Type', 'Total Days', 'Leave Status')

        for col in ('ID', 'Date', 'Starting Date', 'Ending Date', 'Leave Type', 'Total Days', 'Leave Status'):
            self.leave_tree.column('#0', width=0, stretch=tk.NO)
            self.leave_tree.column(col, anchor=tk.CENTER, width=120)
            self.leave_tree.heading(col, text=col)

        self.leave_tree.place(x=600, y=30)

        self.entry_id = tk.Entry(self.master, font=font2, width=entry_width)
        self.entry_date = DateEntry(self.master, font=font2, width=entry_width, date_pattern='yyyy-mm-dd')
        self.entry_start_date = DateEntry(self.master, font=font2, width=entry_width, date_pattern='yyyy-mm-dd')
        self.entry_end_date = DateEntry(self.master, font=font2, width=entry_width, date_pattern='yyyy-mm-dd')

        common_leave_types = ['Vacation', 'Sick Leave', 'Maternity Leave', 'Paternity Leave', 'Public Holiday']
        self.entry_leave_type = ttk.Combobox(self.master, values=common_leave_types + ['Other'], font=font2, width=entry_width)


        leave_status_options = ['Pending', 'Approved', 'Denied']
        self.entry_leave_status = ttk.Combobox(self.master, values=leave_status_options, font=font2, width=entry_width)

        label_id = tk.Label(self.master, text='ID:', font=font2, bg='#161C35', fg='#fff')
        label_date = tk.Label(self.master, text='Date:', font=font2, bg='#161C35', fg='#fff')
        label_start_date = tk.Label(self.master, text='Starting Date:', font=font2, bg='#161C35', fg='#fff')
        label_end_date = tk.Label(self.master, text='Ending Date:', font=font2, bg='#161C35', fg='#fff')
        label_leave_type = tk.Label(self.master, text='Leave Type:', font=font2, bg='#161C35', fg='#fff')
        label_leave_status = tk.Label(self.master, text='Leave Status:', font=font2, bg='#161C35', fg='#fff')

        labels = [label_id, label_date, label_start_date, label_end_date, label_leave_type,
                  label_leave_status]
        entries = [self.entry_id, self.entry_date, self.entry_start_date, self.entry_end_date,
                   self.entry_leave_type, self.entry_leave_status]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            label.grid(row=i + 1, column=0, pady=vertical_padding, padx=10, sticky=tk.E)
            entry.grid(row=i + 1, column=1, pady=vertical_padding, padx=10, sticky=tk.W)

        self.add_leave_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Add Leave",
                                                        command=self.add_leave)
        self.add_leave_button.place(x=200, y=430)

        self.display_leave_data()
        self.back_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Back to Intermediate",
                                                   command=self.back_to_intermediate_page)
        self.back_button.place(x=520, y=430)
        self.delete_leave_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Delete Leave",
                                                           command=self.delete_leave)
        self.delete_leave_button.place(x=350, y=430)

    def delete_leave(self):
        selected_item = self.leave_tree.selection()

        if not selected_item:
            messagebox.showinfo("Information", "Please select a row to delete.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected leave?")
        if confirmation:
            leave_id = self.leave_tree.item(selected_item, "values")[0]
            databases.delete_leave(leave_id)
            self.display_leave_data()


    def back_to_intermediate_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        intermediate_page = IntermediatePage(root)
        root.mainloop()

    def add_leave(self):
        date = self.entry_date.get()
        starting_date = self.entry_start_date.get()
        ending_date = self.entry_end_date.get()
        leave_type = self.entry_leave_type.get()
        leave_status = self.entry_leave_status.get()

        if not all((starting_date, ending_date, leave_type, leave_status)):
            messagebox.showerror('Error', 'Please fill in all required fields.')
            return

        try:
            start_date = datetime.strptime(starting_date, '%Y-%m-%d')
            end_date = datetime.strptime(ending_date, '%Y-%m-%d')
            total_days = (end_date - start_date).days + 1
        except ValueError:
            messagebox.showerror('Error', 'Invalid date format.')
            return

        databases.insert_leave(date, starting_date, ending_date, leave_type, total_days, leave_status)

        self.display_leave_data()

        self.entry_id.delete(0, tk.END)

        if date:
            self.entry_date.set_date('')
        self.entry_start_date.set_date('')
        self.entry_end_date.set_date('')
        self.entry_leave_type.set('')
        self.entry_leave_status.set('')

    def display_leave_data(self):
        self.leave_tree.delete(*self.leave_tree.get_children())
        rows = databases.update_leave_tree()
        for i in rows:
            print(i)
            self.leave_tree.insert("", 'end', values=i)


class EmployeeManagementSystem:
    def __init__(self, master, page_type=""):
        self.master = master
        self.master.title('Employee Management System')
        self.master.geometry('1200x500')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 20, 'bold')
        font2 = ('Arial', 12, 'bold')

        def add_to_treeview(sort_by=None):
            employees = databases.fetch_employees()

            if sort_by == 'name':
                employees.sort(key=lambda x: x[1].lower())
            elif sort_by == 'id':
                employees.sort(key=lambda x: int(x[0]))

            tree.delete(*tree.get_children())
            for employee in employees:
                tree.insert('', tk.END, values=employee)

        def clear(*clicked):
            if clicked:
                tree.selection_remove(tree.focus())
                tree.focus('')
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            role_entry.delete(0, tk.END)
            gender_entry.set('')  # Clear the Combobox selection
            status_entry.delete(0, tk.END)

        def display_data(event):
            selected_item = tree.focus()
            if selected_item:
                row = tree.item(selected_item)['values']
                clear()
                id_entry.insert(0, row[0])
                name_entry.insert(0, row[1])
                role_entry.insert(0, row[2])
                gender_entry.set(row[3])  # Set the Combobox selection
                status_entry.insert(0, row[4])

        def delete():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Choose an employee to delete.')
            else:
                id_val = id_entry.get()
                databases.delete_employee(id_val)
                add_to_treeview()
                clear()
                messagebox.showinfo('Success', 'Data has been deleted.')

        def update():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Choose an employee to update.')
            else:
                id_val = id_entry.get()
                name = name_entry.get()
                role = role_entry.get()
                gender = gender_entry.get()
                status = status_entry.get()
                databases.update_employee(name, role, gender, status, id_val)
                add_to_treeview()
                clear()
                messagebox.showinfo('Success', 'Data has been updated.')

        def insert():
            id_val = id_entry.get()
            name = name_entry.get()
            role = role_entry.get()
            gender = gender_entry.get()
            status = status_entry.get()

            if not all((id_val, name, role, gender, status)):
                messagebox.showerror('Error', 'Please fill in all required fields.')
                return

            if not id_val.isdigit():
                messagebox.showerror('Error', 'ID must be a numeric value.')
                return

            if databases.id_exists(id_val):
                messagebox.showerror('Error', 'ID already exists.')
                return

            databases.insert_employee(id_val, name, role, gender, status)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', "Data has been inserted.")

        def search_employee():
            search_text = search_entry.get().lower()
            employees = databases.fetch_employees()
            filtered_employees = [employee for employee in employees if search_text in employee[1].lower()]

            tree.delete(*tree.get_children())
            for employee in filtered_employees:
                tree.insert('', tk.END, values=employee)

        id_label = customtkinter.CTkLabel(self.master, font=font1, text='ID:', text_color='#fff', bg_color="#161C25")
        id_label.place(x=20, y=20)

        id_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                          border_color='#0C9295', border_width=2, width=180)
        id_entry.place(x=100, y=20)

        name_label = customtkinter.CTkLabel(self.master, font=font1, text='Name:', text_color='#fff', bg_color="#161C25")
        name_label.place(x=20, y=80)

        name_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                            border_color='#0C9295', border_width=2, width=180)
        name_entry.place(x=100, y=80)

        role_label = customtkinter.CTkLabel(self.master, font=font1, text='Role:', text_color='#fff', bg_color="#161C25")
        role_label.place(x=20, y=140)

        role_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                            border_color='#0C9295', border_width=2, width=180)
        role_entry.place(x=100, y=140)

        gender_label = customtkinter.CTkLabel(self.master, font=font1, text='Gender:', text_color='#fff',
                                              bg_color="#161C25")
        gender_label.place(x=20, y=200)

        gender_choices = ['Male', 'Female']
        gender_entry = ttk.Combobox(self.master, values=gender_choices, font=font1, state='readonly')
        gender_entry.place(x=120, y=250)

        status_label = customtkinter.CTkLabel(self.master, font=font1, text='Status:', text_color='#fff',
                                              bg_color="#161C25")
        status_label.place(x=20, y=260)

        status_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                              border_color='#0C9295', border_width=2, width=180)
        status_entry.place(x=100, y=260)

        search_label = customtkinter.CTkLabel(self.master, font=font1, text='Search:', text_color='#fff',
                                              bg_color="#161C25")
        search_label.place(x=20, y=320)

        search_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                               border_color='#0C9295', border_width=2, width=180)
        search_entry.place(x=100, y=320)

        add_button = customtkinter.CTkButton(master=self.master, command=insert, corner_radius=10, text="Add Employee")
        add_button.place(x=20, y=370)

        update_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Update Employee",
                                                 command=update)
        update_button.place(x=180, y=370)

        clear_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="New Employee",
                                               command=clear)
        clear_button.place(x=350, y=370)

        delete_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Delete Employee",
                                                 command=delete)
        delete_button.place(x=520, y=370)

        sort_name_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Sort by Name",
                                                    command=lambda: add_to_treeview(sort_by='name'))
        sort_name_button.place(x=20, y=430)

        sort_id_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Sort by ID",
                                                  command=lambda: add_to_treeview(sort_by='id'))
        sort_id_button.place(x=180, y=430)

        search_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Search",
                                                 command=search_employee)
        search_button.place(x=350, y=430)

        self.back_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Back to Intermediate",
                                                   command=self.back_to_intermediate_page)
        self.back_button.place(x=520, y=430)

        style = ttk.Style(self.master)
        style.theme_use('clam')
        style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
        style.map('Treeview', background=[('selected', '#1A8F2D')])

        tree = ttk.Treeview(self.master, height=15)
        tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Status')

        tree.column('#0', width=0, stretch=tk.NO)
        tree.column('ID', anchor=tk.CENTER, width=120)
        tree.column('Name', anchor=tk.CENTER, width=120)
        tree.column('Role', anchor=tk.CENTER, width=120)
        tree.column('Gender', anchor=tk.CENTER, width=100)
        tree.column('Status', anchor=tk.CENTER, width=120)

        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Role', text='Role')
        tree.heading('Gender', text='Gender')
        tree.heading('Status', text='Status')

        tree.place(x=600, y=30)
        tree.bind('<ButtonRelease>', display_data)
        add_to_treeview()

    def back_to_intermediate_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        intermediate_page = IntermediatePage(root)
        root.mainloop()
class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Login Page')
        self.master.geometry('400x200')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 14, 'bold')

        self.username_label = customtkinter.CTkLabel(self.master, font=font1, text='Username:',
                                                     text_color='#fff', bg_color="#161C25")
        self.username_label.place(x=50, y=30)

        self.username_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                                     border_color='#0C9295', border_width=2, width=180)
        self.username_entry.place(x=180, y=30)

        self.password_label = customtkinter.CTkLabel(self.master, font=font1, text='Password:',
                                                     text_color='#fff', bg_color="#161C25")
        self.password_label.place(x=50, y=80)

        self.password_entry = customtkinter.CTkEntry(self.master, font=font1, show='*', text_color='#000',
                                                     fg_color='#fff', border_color='#0C9295', border_width=2,
                                                     width=180)
        self.password_entry.place(x=180, y=80)

        self.login_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Login",
                                                    command=self.login)
        self.login_button.place(x=50, y=130)

        self.signup_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Signup",
                                                     command=self.open_signup_page)
        self.signup_button.place(x=200, y=130)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        user_exists = databases.get_user(username)

        conn = sqlite3.connect('Employees.db')
        cursor = conn.cursor()

        # Execute a query to fetch user data
        query = "SELECT * FROM Users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, hashed_password))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            messagebox.showinfo('Login Successful', 'Welcome, ' + username + '!')
            self.open_employee_management_system()
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password')

    def open_employee_management_system(self):
        self.master.destroy()
        root = customtkinter.CTk()
        intermediate_page = IntermediatePage(root)
        root.mainloop()

    def open_signup_page(self):
        self.master.destroy()
        root = customtkinter.CTk()
        signup_page = SignupPage(root, self)
        root.mainloop()

class SignupPage:
    def __init__(self, master, login_page):
        self.master = master
        self.master.title('Signup Page')
        self.master.geometry('400x200')
        self.master.config(bg='#161C35')
        self.master.resizable(False, False)

        font1 = ('Arial', 14, 'bold')

        self.username_label = customtkinter.CTkLabel(self.master, font=font1, text='Username:',
                                                     text_color='#fff', bg_color="#161C25")
        self.username_label.place(x=50, y=30)

        self.username_entry = customtkinter.CTkEntry(self.master, font=font1, text_color='#000', fg_color='#fff',
                                                     border_color='#0C9295', border_width=2, width=180)
        self.username_entry.place(x=180, y=30)

        self.password_label = customtkinter.CTkLabel(self.master, font=font1, text='Password:',
                                                     text_color='#fff', bg_color="#161C25")
        self.password_label.place(x=50, y=80)

        self.password_entry = customtkinter.CTkEntry(self.master, font=font1, show='*', text_color='#000',
                                                     fg_color='#fff', border_color='#0C9295', border_width=2,
                                                     width=180)
        self.password_entry.place(x=180, y=80)

        self.signup_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Signup",
                                                    command=self.signup)
        self.signup_button.place(x=50, y=130)

        self.back_button = customtkinter.CTkButton(master=self.master, corner_radius=10, text="Back to Login",
                                                   command=self.back_to_login)
        self.back_button.place(x=200, y=130)

        self.login_page = login_page

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        if not all((username, password)):
            messagebox.showerror('Error', 'Please fill in all required fields.')
            return

        user_exists = databases.get_user(username)
        if user_exists:
            messagebox.showerror('Error', 'Username already exists. Please choose another username.')
            return

        databases.insert_user(username, hashed_password)
        messagebox.showinfo('Signup Successful', 'Account created successfully. You can now login.')
        self.back_to_login()

    def back_to_login(self):
        self.master.destroy()
        root = customtkinter.CTk()
        login_page = LoginPage(root)
        root.mainloop()

    def open_employee_management_system(self):
        self.master.destroy()
        root = customtkinter.CTk()
        intermediate_page = IntermediatePage(root)
        root.mainloop()

if __name__ == "__main__":
    root = customtkinter.CTk()
    login_page = LoginPage(root)
    root.mainloop()