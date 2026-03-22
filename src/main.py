from extract import extract_all_data
from transform import transform_data


def main() -> None:
    customers_df, products_df, orders_df = extract_all_data()

    sales_df = transform_data(customers_df, products_df, orders_df)

    print("\n=== TRANSFORMED SALES DATA ===")
    print(sales_df.head())
    print(f"\nShape: {sales_df.shape}")
    print("\nColumns:")
    print(list(sales_df.columns))


if __name__ == "__main__":
    main()