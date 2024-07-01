import pyodbc
import matplotlib.pyplot as plt

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    r"Server=DESKTOP-2M280GH\SQLEXPRESS;"
    "Database=MYWALLET;"
    "Trusted_connection=yes;"
)

cursor = conn.cursor()


def register_user(first_name, last_name, username, hashed_password, email):
    try:
        cursor.execute("INSERT INTO Users (FirstName, LastName, Username, Password, Email) "
                       "VALUES (?, ?, ?, ?, ?)", first_name, last_name, username, hashed_password, email)
        conn.commit()
        return True, "You have successfully registered"
    except Exception as e:
        return False, str(e)


def check_user(username):
    cursor.execute("SELECT * FROM Users WHERE Username=?", username)
    result = cursor.fetchone()

    if result:
        return result
    else:
        return None


def check_user_password(username):
    cursor.execute("SELECT Password FROM Users WHERE Username=?", username)
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None


def calculate_net_balance(username):
    cursor.execute("SELECT SUM(Amount) FROM Incomes "
                   "WHERE UserID IN (SELECT UserID FROM Users where Username = ?)", username)
    total_incomes = cursor.fetchone()

    cursor.execute("SELECT SUM(Amount) FROM Expenses "
                   "WHERE UserID IN (SELECT UserID FROM Users where Username = ?)", username)
    total_expenses = cursor.fetchone()

    income_amount = total_incomes[0] if total_incomes[0] is not None else 0
    expense_amount = total_expenses[0] if total_expenses[0] is not None else 0

    balance = income_amount - expense_amount

    return balance


def get_incomes_summary(username):
    cursor.execute("SELECT SUM(Amount), Categories.CategoryName FROM Incomes, Categories "
                   "WHERE UserID IN (SELECT UserID FROM Users WHERE Username=?) AND "
                   "Incomes.CategoryID = Categories.CategoryID "
                   "GROUP BY Categories.CategoryName", username)
    info = cursor.fetchall()

    if not info or all(row[0] is None for row in info):
        fig, ax = plt.subplots()
        ax.pie([1], colors=["#d3d3d3"], startangle=90)
        plt.title("No Incomes")

    else:
        labels = [row[1] for row in info]
        values = [row[0] if row[0] is not None else 0 for row in info]
        fix, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.2f%%")
        plt.title("Incomes")

    plt.show()


def get_expenses_summary(username):
    cursor.execute("SELECT SUM(Amount), Categories.CategoryName FROM Expenses, Categories "
                   "WHERE UserID IN (SELECT UserID FROM Users WHERE Username=?) AND "
                   "Expenses.CategoryID = Categories.CategoryID "
                   "GROUP BY Categories.CategoryName", username)
    info = cursor.fetchall()

    if not info or all(row[0] is None for row in info):
        fig, ax = plt.subplots()
        ax.pie([1], colors=["#d3d3d3"], startangle=90)
        plt.title("No Expenses")

    else:
        labels = [row[1] for row in info]
        values = [row[0] if row[0] is not None else 0 for row in info]
        fix, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.2f%%")
        plt.title("Expenses")

    plt.show()
