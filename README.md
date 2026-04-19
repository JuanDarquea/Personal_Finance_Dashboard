# Personal Finance Dashboard

A local dashboard to track and visualize personal spending from bank CSV exports.

## Features
- Import CSV exports from any bank (Date, Description, Amount columns)
- Auto-categorizes transactions (Groceries, Transport, Dining, Subscriptions, etc.)
- Stores data in a local SQLite database — your data stays on your machine
- Interactive dashboard: monthly spending, category breakdown, transaction table

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run src/dashboard.py
```

Then open `http://localhost:8501` in your browser.

## Import Transactions

Use the sidebar to upload a CSV file. Expected format:

```csv
Date,Description,Amount
2026-03-01,Whole Foods Market,-82.45
2026-03-04,Salary Deposit,2500.00
```

## Run Tests

```bash
pytest -v
```

## Project Structure

```
src/categories.py   — keyword-based category rules
src/db.py           — SQLite interface
src/ingestor.py     — CSV parsing and categorization
src/dashboard.py    — Streamlit app
```
