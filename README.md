MyWallet

## Table of Contents

1. [Introduction](#introduction)
2. [Process and Information Flow Analysis](#process-and-information-flow-analysis)
3. [Analysis of Relevant Documents](#analysis-of-relevant-documents)
4. [Conceptual and Physical Model](#conceptual-and-physical-model)
5. [Implementation Conditions](#implementation-conditions)
6. [Test Data](#test-data)
7. [Description of Implemented Database and Potential Enhancements](#description-of-implemented-database-and-potential-enhancements)

## Introduction
The provided code consists of two parts: a Python script for database interaction and a Tkinter GUI application for user registration, login, and management of income and expenses. This document describes the process and information flow, analysis of relevant documents, conceptual and physical models, implementation conditions, test data, and the description of the implemented database along with potential enhancements.

## Process and Information Flow Analysis
The system allows users to register, log in, manage their income and expenses, and visualize financial summaries. The process starts with user registration, where details are saved in the database. Users can log in using their credentials, view their current balance, add income or expenses, and see summaries of their transactions.

## Analysis of Relevant Documents
The relevant documents include:
- User registration and login forms.
- Income and expense entry forms.
- Database schema for storing user information, transactions, and categories.
- Code documentation for understanding the functionality and flow of the application.

## Conceptual and Physical Model
**Conceptual Model:**
1. **Users**: Stores user information including first name, last name, username, password, and email.
2. **Incomes**: Stores income transactions with references to user and category.
3. **Expenses**: Stores expense transactions with references to user and category.
4. **Categories**: Stores categories for income and expense transactions.

**Physical Model:**
- **Users** table with columns: `UserID` (Primary Key), `FirstName`, `LastName`, `Username`, `Password`, `Email`.
- **Incomes** table with columns: `IncomeID` (Primary Key), `UserID` (Foreign Key), `CategoryID` (Foreign Key), `Amount`, `Description`.
- **Expenses** table with columns: `ExpenseID` (Primary Key), `UserID` (Foreign Key), `CategoryID` (Foreign Key), `Amount`, `Description`.
- **Categories** table with columns: `CategoryID` (Primary Key), `CategoryName`.

## Implementation Conditions
The implementation requires:
- Python 3.x with `pyodbc`, `matplotlib`, `bcrypt`, and `tkinter` libraries.
- SQL Server with a database named 'MYWALLET'.
- ODBC Driver 17 for SQL Server for database connectivity.

## Test Data
Test data includes:
- User registration data: first name, last name, username, password, email.
- Income data: user reference, category reference, amount, description.
- Expense data: user reference, category reference, amount, description.
- Categories: predefined set of categories for income and expenses.

## Description of Implemented Database and Potential Enhancements
The implemented database stores user information, income and expense transactions, and categories. The application provides functionalities for user registration, login, income and expense management, and summary visualization.

Potential enhancements include:
- Adding functionality for updating and deleting transactions.
- Enhancing security features such as password reset.
- Improving the user interface for a better user experience.
- Adding more detailed financial analysis and reporting features.
