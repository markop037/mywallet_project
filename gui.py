import tkinter as tk
import bcrypt
from database import *


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

        existing_user = check_user(username)
        if existing_user:
            self.error_label.config(text="Username already exists!\nPlease choose another one.",
                                    font=("Arial", 10), fg='red', background='Navy Blue')
            return

        hashed_password = self.hash_password(password)

        success, message = register_user(first_name, last_name, username, hashed_password, email)

        if success:
            self.error_label.configure(text=message, font=("Arial", 10), fg='green', background='Navy Blue')
        else:
            self.error_label.configure(text=message, font=("Arial", 10), fg='red', background='Navy Blue')

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")


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

        hashed_password = check_user_password(username)

        if hashed_password:
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


class Home:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("My Wallet")
        self.root.configure(background="Navy Blue")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (400 // 2)
        y_coordinate = (screen_height // 2) - (860 // 2)
        self.root.geometry(f"{400}x{860}+{x_coordinate}+{y_coordinate}")

        self.user = check_user(username)

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

        self.info_frame.pack(pady=30)

        self.add_label = tk.Label(self.root, text="Add income or expense",
                                  font=("Arial", 13), fg='white', background='Navy Blue')
        self.add_label.pack(pady=10)

        self.amount_label = tk.Label(self.root, text="Amount*",
                                     font=('Arial', 11), fg='white', background='Navy Blue')
        self.amount_label.pack(pady=10)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.description_label = tk.Label(self.root, text="Description",
                                          font=('Arial', 11), fg='white', background='Navy Blue')
        self.description_label.pack(pady=10)

        self.description_text = tk.Text(self.root, height=4, width=20)
        self.description_text.pack()

        self.categories_income_dic = {1: "Salary",
                                      2: "Passive income",
                                      3: "Other income"}

        self.categories_expense_dic = {4: "Rent",
                                       5: "Transport",
                                       6: "Food and drink",
                                       7: "Health",
                                       8: "Clothes",
                                       9: "Other expenses"}

        self.add_frame = tk.Frame(self.root)
        self.add_frame.configure(background="Navy Blue")

        self.categories_income_label = tk.Label(self.add_frame, text="Income Categories*",
                                                font=('Arial', 11), fg='white', background='Navy Blue')
        self.categories_income_label.grid(row=0, column=0, pady=10, padx=20)

        self.categories_income_listbox = tk.Listbox(self.add_frame)
        for value in self.categories_income_dic.items():
            self.categories_income_listbox.insert(tk.END, f"{value[1]}")
        self.categories_income_listbox.grid(row=1, column=0, padx=20)

        self.categories_expenses_label = tk.Label(self.add_frame, text="Expenses Categories*",
                                                  font=('Arial', 11), fg='white', background='Navy Blue')
        self.categories_expenses_label.grid(row=0, column=1, pady=10, padx=20)

        self.categories_expenses_listbox = tk.Listbox(self.add_frame)
        for value in self.categories_expense_dic.items():
            self.categories_expenses_listbox.insert(tk.END, f"{value[1]}")
        self.categories_expenses_listbox.grid(row=1, column=1, padx=20)

        self.add_income_button = tk.Button(self.add_frame, text="Add income",
                                           font=('Arial', 13), command=self.add_income)
        self.add_income_button.grid(row=2, column=0, pady=10, padx=20)

        self.add_expense_button = tk.Button(self.add_frame, text="Add expense",
                                            font=('Arial', 13), command=self.add_expense)
        self.add_expense_button.grid(row=2, column=1, pady=10, padx=20)

        self.add_frame.pack()

        self.error_add_label = tk.Label(self.root, text="", font=("Arial", 10),
                                        fg='red', background='Navy Blue')
        self.error_add_label.pack()

        self.root.mainloop()

    def get_incomes_summary(self):
        get_incomes_summary(self.user[3])

    def get_expenses_summary(self):
        get_expenses_summary(self.user[3])

    def add_income(self):
        if self.categories_income_listbox.curselection():
            selected_index = self.categories_income_listbox.curselection()[0]
            selected_value = self.categories_income_listbox.get(selected_index)
        else:
            selected_value = None

        selected_key = None
        for key, value in self.categories_income_dic.items():
            if value == selected_value:
                selected_key = key
                break

        amount = self.amount_entry.get()

        if amount and selected_key:
            cursor.execute("INSERT INTO Incomes (UserID, CategoryID, Amount, Description)"
                           "VALUES (?, ?, ?, ?)", self.user[0], selected_key,
                           float(self.amount_entry.get()), self.description_text.get("1.0", tk.END))

            cursor.commit()
            self.balance_amount_label.configure(text=f"$ {calculate_net_balance(self.user[3])}")
            self.error_add_label.configure(text="")
        else:
            self.error_add_label.configure(text="Fill in all fields marked with *.")

    def add_expense(self):
        if self.categories_expenses_listbox.curselection():
            selected_index = self.categories_expenses_listbox.curselection()[0]
            selected_value = self.categories_expenses_listbox.get(selected_index)
        else:
            selected_value = None

        selected_key = None
        for key, value in self.categories_expense_dic.items():
            if value == selected_value:
                selected_key = key

        amount = self.amount_entry.get()

        if amount and selected_key is not None:
            cursor.execute("INSERT INTO Expenses (UserID, CategoryID, Amount, Description)"
                           "VALUES (?, ?, ?, ?)", self.user[0], selected_key,
                           float(self.amount_entry.get()), self.description_text.get("1.0", tk.END))

            cursor.commit()
            self.balance_amount_label.configure(text=f"$ {calculate_net_balance(self.user[3])}")
            self.error_add_label.configure(text="")
        else:
            self.error_add_label.configure(text="Fill in all fields marked with *.")
