import pandas as pd

"""Transformación de datos para limpiar, enriquecer y consolidar los datasets extraídos.
Esta función toma los DataFrames de clientes, productos y órdenes, realiza operaciones de limpieza, fusiones y 
crea un DataFrame final de ventas listo para análisis o carga en un sistema de destino."""
def transform_data(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    orders_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean and transform raw datasets into a consolidated sales DataFrame.
    """

    # Work on copies to avoid mutating original DataFrames
    customers = customers_df.copy()
    products = products_df.copy()
    orders = orders_df.copy()

    # Remove duplicates
    customers = customers.drop_duplicates()
    products = products.drop_duplicates()
    orders = orders.drop_duplicates()

    # Ensure correct data types
    customers["customer_id"] = customers["customer_id"].astype(int)
    customers["age"] = customers["age"].astype(int)

    products["product_id"] = products["product_id"].astype(int)
    products["unit_price"] = products["unit_price"].astype(float)

    orders["order_id"] = orders["order_id"].astype(int)
    orders["customer_id"] = orders["customer_id"].astype(int)
    orders["product_id"] = orders["product_id"].astype(int)
    orders["quantity"] = orders["quantity"].astype(int)

    # Convert order_date to datetime
    orders["order_date"] = pd.to_datetime(orders["order_date"])

    # Merge orders with customers
    sales_df = orders.merge(customers, on="customer_id", how="left")

    # Merge result with products
    sales_df = sales_df.merge(products, on="product_id", how="left")

    # Create derived columns
    sales_df["total_amount"] = sales_df["quantity"] * sales_df["unit_price"]
    sales_df["year"] = sales_df["order_date"].dt.year
    sales_df["month"] = sales_df["order_date"].dt.month

    # Reorder columns for readability
    sales_df = sales_df[
        [
            "order_id",
            "customer_id",
            "customer_name",
            "city",
            "age",
            "product_id",
            "product_name",
            "category",
            "order_date",
            "quantity",
            "unit_price",
            "total_amount",
            "year",
            "month",
        ]
    ]

    return sales_df