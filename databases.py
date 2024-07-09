import tkinter as tk
from tkcalendar import Calendar
import sqlite3
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect('Employees.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            gender TEXT,
            status TEXT
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Salaries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            amount REAL,
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Leave (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                starting_date DATE NOT NULL,
                ending_date DATE NOT NULL,
                leave_type TEXT NOT NULL,
                total_days INTEGER NOT NULL,
                leave_status TEXT NOT NULL
            )
        ''')

    conn.commit()
    conn.close()
def fetch_employees():
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Employees')
        employees = cursor.fetchall()
    return employees

def insert_employee(id_val, name, role, gender, status):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Employees (id, name, role, gender, status) VALUES (?, ?, ?, ?, ?)',
                       (id_val, name, role, gender, status))
        conn.commit()


def delete_employee(employee_id):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Employees WHERE id = ?', (employee_id,))
        conn.commit()

def update_employee(new_name, new_role, new_gender, new_status, employee_id):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Employees SET name = ?, role = ?, gender = ?, status = ? WHERE id = ?",
                       (new_name, new_role, new_gender, new_status, employee_id))
        conn.commit()

def id_exists(employee_id):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Employees WHERE id = ?', (employee_id,))
        result = cursor.fetchone()
    return result[0] > 0

def get_employee_id_by_name(employee_name):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Employees WHERE name = ?', (employee_name,))
        result = cursor.fetchone()
    return result[0] if result else None

def insert_salary(employee_id, salary_amount):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Salaries (employee_id, amount)
            VALUES (?, ?)
        ''', (employee_id, salary_amount))
        conn.commit()

def update_tree():
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        query = "SELECT Employees.name, Salaries.amount FROM Employees JOIN Salaries ON Employees.id = Salaries.employee_id"
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

def get_user(username):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
    return result

def insert_user(username, password):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

def get_employee_salary_by_id(employee_id):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        query = "SELECT Salaries.amount FROM Salaries WHERE Salaries.employee_id = ?"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()
    return result[0] if result else None

def insert_leave(date, starting_date, ending_date, leave_type, total_days, leave_status):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Leave (date, Starting_date, ending_date, Leave_type, Total_days, Leave_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, starting_date, ending_date, leave_type, total_days, leave_status))
        conn.commit()

def update_leave_tree():
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Leave"
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

def update_salary(employee_name, new_salary):
    with sqlite3.connect('Employees.db') as conn:
        cursor = conn.cursor()

        # Check if the employee_name exists in the Employees table
        cursor.execute("SELECT id FROM Employees WHERE name = ?", (employee_name,))
        result = cursor.fetchone()

        if result:
            employee_id = result[0]
            cursor.execute("SELECT COUNT(*) FROM Salaries WHERE employee_id = ?", (employee_id,))
            if cursor.fetchone()[0] > 0:
                query = "UPDATE Salaries SET amount = ? WHERE employee_id = ?"
                cursor.execute(query, (new_salary, employee_id))
                conn.commit()
            else:
                print(f"Employee with name {employee_name} does not have a salary record.")
        else:
            print(f"Employee with name {employee_name} not found in Employees table.")


def delete_leave(leave_id):
    try:
        connection = sqlite3.connect('Employees.db')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Leave WHERE id=?", (leave_id,))

        connection.commit()
        messagebox.showinfo("Information", "Leave deleted successfully.")
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error deleting leave: {error}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    create_table()
    get_employee_salary_by_id(3)
