# E-Commerce Analytics Dashboard (Python + Streamlit)

A professional, interactive e-commerce analytics project built with **Python**, **Streamlit**, **Pandas**, **Matplotlib**, and **Plotly**.

This repository includes:
- A **database-driven dashboard** for real transaction reporting.
- A **sample-data dashboard** for local demo/testing without a database.

## Project Overview

The dashboards provide a quick business view of sales performance, including:
- Revenue and order KPIs
- Monthly sales trend analysis
- Product revenue share visualization
- Product-month heatmap
- Interactive filters and product drill-down

## Tech Stack

- Python 3.9+
- Streamlit
- Pandas
- Matplotlib
- Plotly
- SQLAlchemy + PyMySQL (for MySQL-connected version)

## Project Structure

```
.
|-- app.py
|-- ecommerce.py
|-- ecommerce_dashboard.py
`-- README.md
```

- `ecommerce.py`: Streamlit dashboard using in-memory sample data (no DB required).
- `ecommerce_dashboard.py`: Streamlit dashboard connected to MySQL via SQLAlchemy.
- `app.py`: currently empty (can be used as an entry module later).

## Features

- KPI cards: total revenue, total orders, average basket size
- Monthly sales line chart
- Product revenue pie chart
- Heatmap of monthly product sales
- Sidebar filters (month, product)
- Drill-down table by selected product

## Getting Started

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd python
```

### 2. Create virtual environment (recommended)

```bash
python -m venv .venv
```

Activate environment:

- Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

- Windows (Command Prompt)

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install streamlit pandas matplotlib plotly sqlalchemy pymysql
```

## Run the Application

### Option A: Run sample-data dashboard

```bash
streamlit run ecommerce.py
```

### Option B: Run MySQL-connected dashboard

```bash
streamlit run ecommerce_dashboard.py
```

## Database Setup (for `ecommerce_dashboard.py`)

The dashboard expects a MySQL database named `ecommercedb` and these tables:
- `Transaction`
- `TransactionProduct`
- `Product`

The SQL query in the app uses:
- `Transaction.TransactionID`, `Transaction.TransactionDate`
- `TransactionProduct.TransactionID`, `TransactionProduct.ProductID`, `TransactionProduct.Quantity`
- `Product.ProductID`, `Product.ProductName`, `Product.Price`

Update database credentials in `ecommerce_dashboard.py` before running:

```python
user = "root"
password = "TIGER"
host = "localhost"
database = "ecommercedb"
```

## Security Note

Do not keep real database credentials hardcoded in production. Use environment variables or a secrets manager.

Example (recommended approach):
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_NAME`

## Troubleshooting

- If Streamlit command is not found:

```bash
python -m streamlit run ecommerce.py
```

- If MySQL connection fails:
1. Verify MySQL service is running.
2. Confirm database/table names match the query.
3. Check host, username, and password.
4. Ensure `pymysql` is installed.

## Learning Context

This project is well-suited for:
- first-year internship portfolio work
- learning dashboarding with Streamlit
- understanding SQL + Python analytics integration

## Future Improvements

- Move credentials to environment variables
- Add date range filter
- Add CSV export for filtered data
- Add deployment (Streamlit Community Cloud / Docker)
- Add unit tests for data transformations

## Author

Prepared as part of a Python internship learning project.
