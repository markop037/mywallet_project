# MyWallet

MyWallet is a web app for tracking your personal finances. You can log your incomes and expenses, see your current balance, and check charts that show where your money is coming from and where it's going.

## Features

- Register and log in with a username and password, or sign in with Google
- Add income and expense transactions with a category and amount
- Filter transactions and charts by time range (today, this week, this month, this year, or all time)
- See your current balance update automatically
- View pie charts for income and expense breakdown by category
- Browse your transactions and delete any of them

## How it's built

The app has three parts: a React frontend, a FastAPI backend, and a PostgreSQL database hosted on Supabase.

The frontend is built with React and TypeScript. It uses React Query to fetch data from the backend, Tailwind CSS for styling, Recharts for the charts, and Zustand to keep track of the login token. The Supabase JS client is used for Google OAuth login.

The backend is a FastAPI app that handles all the API endpoints. It uses SQLAlchemy to talk to the database, Werkzeug to hash passwords, and python-jose to create and verify JWT tokens. Every endpoint (except login and register) requires a valid token.

The database runs on Supabase (PostgreSQL). It has tables for users, income/expense categories, incomes, and expenses.

## Demo accounts

The database comes pre-loaded with five demo users. Each account has income and expense data for every month of 2025 and January through April 2026, so you can explore the charts and filters straight away without adding any data yourself.

| Name | Username | Password |
|---|---|---|
| Alice Johnson | `alice_j` | `Alice1234!` |
| Bob Smith | `bob_s` | `Bob1234!` |
| Carol White | `carol_w` | `Carol1234!` |
| David Brown | `david_b` | `David1234!` |
| Emma Davis | `emma_d` | `Emma1234!` |

Sign in on the login page using the **username** and **password** columns above. Google sign-in is also available if you prefer to use your own Google account.

## Running the app

Backend:

```
cd backend
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

Frontend:

```
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Running tests

```
cd backend
pytest tests/ -v
```

Tests use SQLite so you don't need a real database connection to run them.
