import tkinter as tk
import matplotlib.pyplot as plt
import pyodbc
import bcrypt

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    r"Server=DESKTOP-2M280GH\SQLEXPRESS;"
    "Database=MYWALLET;"
    "Trusted_connection=yes;"
)

cursor = conn.cursor()


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


class Register:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Sign Up")
        self.root.configure(background='Navy Blue')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (320 // 2)
        y_coordinate = (screen_height // 2) - (540 // 2)
        self.root.geometry(f"{320}x{540}+{x_coordinate}+{y_coordinate}")

        self.myWallet_label = tk.Label(self.root, text="MyWallet",
                                       font=("Arial", 15), fg='white', background='Navy Blue')
        self.myWallet_label.pack(pady=30)

        self.firstName_label = tk.Label(self.root, text="First Name",
                                        font=("Arial", 12), fg='white', background='Navy Blue')
        self.firstName_label.pack(pady=5)
        self.firstName_entry = tk.Entry(self.root, width=30)
        self.firstName_entry.pack()

        self.lastName_label = tk.Label(self.root, text="Last Name",
                                       font=("Arial", 12), fg='white', background='Navy Blue')
        self.lastName_label.pack(pady=5)
        self.lastName_entry = tk.Entry(self.root, width=30)
        self.lastName_entry.pack()

        self.username_label = tk.Label(self.root, text="Username*",
                                       font=("Arial", 12), fg='white', background='Navy Blue')
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password*",
                                       font=("Arial", 12), fg='white', background='Navy Blue')
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show='•')
        self.password_entry.pack()

        self.confirm_password_label = tk.Label(self.root, text="Confirm Password*",
                                               font=("Arial", 12), fg='white', background='Navy Blue')
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.root, width=30, show='•')
        self.confirm_password_entry.pack()

        self.email_label = tk.Label(self.root, text="Email",
                                    font=("Arial", 12), fg='white', background='Navy Blue')
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack()

        self.signUp_button = tk.Button(self.root, text="Sign up", font=("Arial", 12), command=self.register_user)
        self.signUp_button.pack(pady=20)

        self.error_label = tk.Label(self.root, text="", font=("Arial", 10),
                                    fg='red', background='Navy Blue')
        self.error_label.pack()

        self.root.mainloop()

    def register_user(self):
        first_name = self.firstName_entry.get()
        last_name = self.lastName_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()

        if not username or not password or not confirm_password:
            self.error_label.configure(text="Fill in all fields marked with *.",
                                       font=("Arial", 10), fg='red', background='Navy Blue')
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match.",
                                       font=("Arial", 10), fg='red', background='Navy Blue')
            return

        cursor.execute("SELECT * FROM Users WHERE username=?", username)
        existing_user = cursor.fetchone()

        if existing_user:
            self.error_label.config(text="Username already exists!\nPlease choose another one.")
            return

        hashed_password = hash_password(password)

        try:
            cursor.execute("INSERT INTO Users (FirstName, LastName, Username, Password, Email) "
                           "VALUES (?, ?, ?, ?, ?)", first_name, last_name, username, hashed_password, email)
            conn.commit()
            self.error_label.configure(text="You have successfully registered",
                                       font=("Arial", 10), fg='green', background='Navy Blue')
        except Exception as e:
            self.error_label.configure(text=str(e))


class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Log In")
        self.root.configure(background='Navy Blue')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (320 // 2)
        y_coordinate = (screen_height // 2) - (410 // 2)
        self.root.geometry(f"{320}x{410}+{x_coordinate}+{y_coordinate}")

        self.welcome_label = tk.Label(self.root, text="Welcome to MyWallet",
                                      font=("Arial", 15), fg='white', background='Navy Blue')
        self.welcome_label.pack(pady=30)

        self.username_label = tk.Label(self.root, text="Username", font=("Arial", 11),
                                       fg='white', background='Navy Blue')
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password", font=("Arial", 11),
                                       fg='white', background='Navy Blue')
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show='•')
        self.password_entry.pack()

        self.logIn_button = tk.Button(self.root, text="Log In", command=self.check_user, font=("Arial", 12))
        self.logIn_button.pack(pady=20)

        self.label_visible = tk.BooleanVar(value=False)
        self.error_label = tk.Label(self.root, text="Sorry, your username or password was incorrect.\n"
                                                    "Please double-check your username or password.",
                                    font=("Arial", 10), fg='red', background='Navy Blue')

        self.signUp_label = tk.Label(self.root, text="Don't have an account?",
                                     font=("Arial", 12), fg='white', background='Navy Blue')
        self.signUp_label.pack()

        self.signUp_button = tk.Button(self.root, text="Sign up", font=("Arial", 12),
                                       command=self.show_registration_form)
        self.signUp_button.pack(pady=5)

        self.root.mainloop()

    def check_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT Password FROM Users WHERE Username=?", username)
        result = cursor.fetchone()
        if result:
            hashed_password = result[0]

            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                self.root.destroy()
                Home(username)
            else:
                if not self.label_visible.get():
                    self.error_label.pack(pady=5)
                    self.label_visible.set(True)
        else:
            if not self.label_visible.get():
                self.error_label.pack(pady=5)
                self.label_visible.set(True)

    def show_registration_form(self):
        Register(self.root)


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


class Home:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("My Wallet")
        self.root.configure(background="Navy Blue")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (400 // 2)
        y_coordinate = (screen_height // 2) - (700 // 2)
        self.root.geometry(f"{400}x{700}+{x_coordinate}+{y_coordinate}")

        cursor.execute("SELECT * FROM Users WHERE Username=?", username)
        self.user = cursor.fetchone()

        self.welcome_label = tk.Label(self.root, text=f"Welcome {self.user[3]}",
                                      font=("Arial", 15), fg='white', background='Navy Blue')
        self.welcome_label.pack(pady=30)

        self.balance_label = tk.Label(self.root, text=f"Current account balance",
                                      font=("Arial", 12), fg='white', background='Navy Blue')
        self.balance_label.pack(anchor="w", padx=15)

        self.balance_amount_label = tk.Label(self.root, text=f"$ {calculate_net_balance(self.user[3])}",
                                             font=("Arial", 17), fg='white', background='Navy Blue')
        self.balance_amount_label.pack(anchor="w", padx=15)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.configure(background="Navy Blue")

        self.incomes_label = tk.Label(self.info_frame, text="Incomes",
                                      font=("Arial", 13), fg='white', background='Navy Blue')
        self.incomes_label.grid(row=0, column=0, pady=10)

        self.incomes_button = tk.Button(self.info_frame, text="See incomes", font=("Arial", 13),
                                        command=self.get_incomes_summary)
        self.incomes_button.grid(row=1, column=0, padx=20)

        self.expenses_label = tk.Label(self.info_frame, text="Expenses", font=("Arial", 13),
                                       fg='white', background='Navy Blue')
        self.expenses_label.grid(row=0, column=1, pady=10)

        self.expenses_button = tk.Button(self.info_frame, text="See expenses", font=("Arial", 13),
                                         command=self.get_expenses_summary)
        self.expenses_button.grid(row=1, column=1, padx=20)

        self.info_frame.pack()

    def get_incomes_summary(self):
        cursor.execute("SELECT SUM(Amount), Categories.CategoryName FROM Incomes, Categories "
                       "WHERE UserID IN (SELECT UserID FROM Users WHERE Username=?) AND "
                       "Incomes.CategoryID = Categories.CategoryID "
                       "GROUP BY Categories.CategoryName", self.user[3])
        info = cursor.fetchall()

        if not info or all(row[0] is None for row in info):
            fig, ax = plt.subplots()
            ax.pie([1], colors=["#d3d3d3"], startangle=90)
            plt.title("No Incomes")

        else:
            labels = [row[1] for row in info]
            values = [row[0] if row[0] is not None else 0 for row in info]
            fix, ax = plt.subplot()
            ax.pie(values, labels=labels, autopct="%1.2f%%")
            plt.title("Incomes")

        plt.show()

    def get_expenses_summary(self):
        cursor.execute("SELECT SUM(Amount), Categories.CategoryName FROM Expenses, Categories "
                       "WHERE UserID IN (SELECT UserID FROM Users WHERE Username=?) AND "
                       "Expenses.CategoryID = Categories.CategoryID "
                       "GROUP BY Categories.CategoryName", self.user[3])
        info = cursor.fetchall()

        if not info or all(row[0] is None for row in info):
            fig, ax = plt.subplots()
            ax.pie([1], colors=["#d3d3d3"], startangle=90)
            plt.title("No Expenses")

        else:
            labels = [row[1] for row in info]
            values = [row[0] if row[0] is not None else 0 for row in info]
            fix, ax = plt.subplot()
            ax.pie(values, labels=labels, autopct="%1.2f%%")
            plt.title("Expenses")

        plt.show()


if __name__ == "__main__":
    Login()
