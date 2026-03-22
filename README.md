# ETL Sales Pipeline

Small data engineering project built with Python, pandas and PostgreSQL.

## Project goal

This project implements a simple ETL pipeline for ecommerce sales data:

- Extract data from CSV files
- Transform and clean the data with pandas
- Load the processed data into PostgreSQL
- Query the data with SQL for business analysis

## Tech stack

- Python
- pandas
- PostgreSQL
- SQL
- Git / GitHub

## Project structure

```text
etl-sales-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
│   ├── create_tables.sql
│   └── analytics_queries.sql
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── .gitignore
├── README.md
└── requirements.txt