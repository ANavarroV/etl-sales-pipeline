from extract import extract_all_data

"""Punto de entrada principal para la ejecución del pipeline ETL. 
Este módulo se encarga de coordinar la extracción de datos y mostrar un resumen de los datasets cargados."""
def main() -> None:
    customers_df, products_df, orders_df = extract_all_data()

    print("\n=== CUSTOMERS ===")
    print(customers_df.head())
    print(f"\nShape: {customers_df.shape}")

    print("\n=== PRODUCTS ===")
    print(products_df.head())
    print(f"\nShape: {products_df.shape}")

    print("\n=== ORDERS ===")
    print(orders_df.head())
    print(f"\nShape: {orders_df.shape}")


if __name__ == "__main__":
    main()