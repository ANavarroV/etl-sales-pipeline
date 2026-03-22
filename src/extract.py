from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")

"""Extracción de datos desde archivos CSV. Cada función carga un conjunto de datos específico 
    y devuelve un DataFrame de pandas."""
def extract_customers() -> pd.DataFrame:
    """Load customers data from CSV."""
    file_path = RAW_DATA_PATH / "customers.csv"
    customers_df = pd.read_csv(file_path)
    return customers_df


def extract_products() -> pd.DataFrame:
    """Load products data from CSV."""
    file_path = RAW_DATA_PATH / "products.csv"
    products_df = pd.read_csv(file_path)
    return products_df


def extract_orders() -> pd.DataFrame:
    """Load orders data from CSV."""
    file_path = RAW_DATA_PATH / "orders.csv"
    orders_df = pd.read_csv(file_path)
    return orders_df


def extract_all_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all source datasets and return them as DataFrames."""
    customers_df = extract_customers()
    products_df = extract_products()
    orders_df = extract_orders()

    return customers_df, products_df, orders_df