# MyWallet

MyWallet is a web app for tracking your personal finances. You can log your incomes and expenses, see your current balance, and check charts that show where your money is coming from and where it's going.

## Features

- Register and log in (or use Google to sign in)
- Add income and expense transactions with a category and amount
- See your current balance update automatically
- View pie charts for income and expense breakdown
- Browse your recent transactions and delete any of them

## How it's built

The app has three parts: a React frontend, a FastAPI backend, and a PostgreSQL database hosted on Supabase.

The frontend is built with React and TypeScript. It uses React Query to fetch data from the backend, Tailwind CSS for styling, Recharts for the charts, and Zustand to keep track of the login token. The Supabase JS client is used for Google and GitHub OAuth login.

The backend is a FastAPI app that handles all the API endpoints. It uses SQLAlchemy to talk to the database, Werkzeug to hash passwords, and python-jose to create and verify JWT tokens. Every endpoint (except login and register) requires a valid token.

The database runs on Supabase (PostgreSQL). It has tables for users, income/expense categories, incomes, and expenses.

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
