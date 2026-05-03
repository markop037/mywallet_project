"""
Seed script — creates 5 test users with monthly income & expense data.

Run from the backend directory:
    python seed_users.py

Requires the same .env (DATABASE_URL) that the backend uses.
"""

import random
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from models.database import SessionLocal, engine, Base  # noqa: E402
import models.user   # noqa: F401, E402 — registers User with Base
import models.finance  # noqa: F401, E402 — registers Finance models with Base
from models.user import User  # noqa: E402
from models.finance import (  # noqa: E402
    Income, Expense, IncomeCategory, ExpenseCategory,
)

Base.metadata.create_all(engine)

# ── Credentials ──────────────────────────────────────────────────────────────

USERS = [
    dict(first_name="Alice",  last_name="Johnson", username="alice_j",  email="alice@mywallet.test",  password="Alice1234!"),
    dict(first_name="Bob",    last_name="Smith",   username="bob_s",    email="bob@mywallet.test",    password="Bob1234!"),
    dict(first_name="Carol",  last_name="White",   username="carol_w",  email="carol@mywallet.test",  password="Carol1234!"),
    dict(first_name="David",  last_name="Brown",   username="david_b",  email="david@mywallet.test",  password="David1234!"),
    dict(first_name="Emma",   last_name="Davis",   username="emma_d",   email="emma@mywallet.test",   password="Emma1234!"),
]

# ── Category definitions ──────────────────────────────────────────────────────

INCOME_CATEGORIES  = ["Salary", "Freelance", "Investments", "Rental", "Bonus"]
EXPENSE_CATEGORIES = ["Housing", "Food", "Transport", "Utilities",
                      "Healthcare", "Entertainment", "Shopping", "Education"]

# ── Per-user monthly financial profiles ──────────────────────────────────────
#   Each entry: list of (category_name, base_amount, jitter_pct)

USER_PROFILES = [
    # Alice — steady salary + occasional freelance
    {
        "incomes":  [("Salary", 4500, 0.02), ("Freelance", 900, 0.40)],
        "expenses": [("Housing", 1200, 0.01), ("Food", 550, 0.15),
                     ("Transport", 200, 0.20), ("Utilities", 130, 0.10),
                     ("Entertainment", 180, 0.30), ("Shopping", 250, 0.35)],
    },
    # Bob — higher salary + investment income
    {
        "incomes":  [("Salary", 5200, 0.02), ("Investments", 400, 0.50)],
        "expenses": [("Housing", 1600, 0.01), ("Food", 700, 0.15),
                     ("Transport", 350, 0.20), ("Utilities", 160, 0.10),
                     ("Healthcare", 120, 0.40), ("Entertainment", 300, 0.30),
                     ("Shopping", 400, 0.40)],
    },
    # Carol — modest salary, careful spender
    {
        "incomes":  [("Salary", 3800, 0.02)],
        "expenses": [("Housing", 1000, 0.01), ("Food", 480, 0.12),
                     ("Transport", 150, 0.18), ("Utilities", 110, 0.10),
                     ("Healthcare", 80, 0.50), ("Shopping", 200, 0.30)],
    },
    # David — high earner, freelancer
    {
        "incomes":  [("Salary", 6000, 0.02), ("Freelance", 1500, 0.45),
                     ("Bonus", 800, 0.80)],
        "expenses": [("Housing", 1800, 0.01), ("Food", 800, 0.15),
                     ("Transport", 500, 0.25), ("Utilities", 200, 0.12),
                     ("Entertainment", 500, 0.35), ("Shopping", 600, 0.40),
                     ("Education", 300, 0.50)],
    },
    # Emma — salary + rental income
    {
        "incomes":  [("Salary", 4000, 0.02), ("Rental", 1200, 0.05)],
        "expenses": [("Housing", 1100, 0.01), ("Food", 600, 0.15),
                     ("Transport", 250, 0.20), ("Utilities", 140, 0.10),
                     ("Healthcare", 100, 0.40), ("Entertainment", 220, 0.30),
                     ("Shopping", 300, 0.35)],
    },
]

# ── Months to seed ────────────────────────────────────────────────────────────

def months_to_seed():
    """2025 Jan–Dec  +  2026 Jan–Apr"""
    result = []
    for m in range(1, 13):
        result.append((2025, m))
    for m in range(1, 5):
        result.append((2026, m))
    return result


def jitter(base: float, pct: float) -> float:
    factor = 1 + random.uniform(-pct, pct)
    return round(base * factor, 2)


def mid_month_dt(year: int, month: int, day_offset: int = 0) -> datetime:
    day = min(15 + day_offset, 28)
    return datetime(year, month, day, 12, 0, 0, tzinfo=timezone.utc)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    random.seed(42)
    db = SessionLocal()

    # ── Ensure categories exist ───────────────────────────────────────────────
    inc_cat_map: dict[str, int] = {}
    for name in INCOME_CATEGORIES:
        cat = db.query(IncomeCategory).filter_by(CategoryName=name).first()
        if not cat:
            cat = IncomeCategory(CategoryName=name)
            db.add(cat)
            db.flush()
        inc_cat_map[name] = cat.CategoryID

    exp_cat_map: dict[str, int] = {}
    for name in EXPENSE_CATEGORIES:
        cat = db.query(ExpenseCategory).filter_by(CategoryName=name).first()
        if not cat:
            cat = ExpenseCategory(CategoryName=name)
            db.add(cat)
            db.flush()
        exp_cat_map[name] = cat.CategoryID

    db.commit()

    months = months_to_seed()
    created: list[dict] = []

    for idx, user_data in enumerate(USERS):
        profile = USER_PROFILES[idx]

        # Skip if user already exists
        existing = db.query(User).filter_by(Username=user_data["username"]).first()
        if existing:
            print(f"  [skip] User '{user_data['username']}' already exists.")
            created.append(user_data)
            continue

        user = User(
            FirstName=user_data["first_name"],
            LastName=user_data["last_name"],
            Username=user_data["username"],
            Password=generate_password_hash(user_data["password"]),
            Email=user_data["email"],
        )
        db.add(user)
        db.flush()

        for year, month in months:
            # ── Incomes ──
            for cat_name, base, jitter_pct in profile["incomes"]:
                # Skip bonus/freelance some months randomly (realistic)
                if cat_name in ("Bonus", "Freelance") and random.random() < 0.35:
                    continue
                amount = jitter(base, jitter_pct)
                db.add(Income(
                    Amount=amount,
                    UserID=user.UserID,
                    CategoryID=inc_cat_map[cat_name],
                    Description=f"{cat_name} — {year}/{month:02d}",
                    created_at=mid_month_dt(year, month, day_offset=random.randint(-3, 3)),
                ))

            # ── Expenses ──
            for cat_name, base, jitter_pct in profile["expenses"]:
                amount = jitter(base, jitter_pct)
                db.add(Expense(
                    Amount=amount,
                    UserID=user.UserID,
                    CategoryID=exp_cat_map[cat_name],
                    Description=f"{cat_name} — {year}/{month:02d}",
                    created_at=mid_month_dt(year, month, day_offset=random.randint(-5, 5)),
                ))

        db.commit()
        print(f"  [ok]   Created user '{user_data['username']}'")
        created.append(user_data)

    db.close()

    # ── Print credentials table ───────────────────────────────────────────────
    print()
    print("=" * 65)
    print(f"{'Name':<18} {'Username':<12} {'Email':<28} {'Password'}")
    print("-" * 65)
    for u in created:
        name = f"{u['first_name']} {u['last_name']}"
        print(f"{name:<18} {u['username']:<12} {u['email']:<28} {u['password']}")
    print("=" * 65)
    print(f"\nData seeded for months: 2025 Jan–Dec  +  2026 Jan–Apr")


if __name__ == "__main__":
    main()
