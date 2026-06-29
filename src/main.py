from pathlib import Path

from api_clients.exchange_rates_api import fetch_exchange_rates
from enrich import enrich_sales_with_exchange_rates
from extract import extract_all_data
from transform import transform_data


PROCESSED_DATA_PATH = Path("data/processed")


def main() -> None:
    customers_df, products_df, orders_df = extract_all_data()

    sales_df = transform_data(customers_df, products_df, orders_df)

    start_date = sales_df["order_date"].min().date()
    end_date = sales_df["order_date"].max().date()
    exchange_rates_df = fetch_exchange_rates(start_date, end_date)
    enriched_sales_df = enrich_sales_with_exchange_rates(sales_df, exchange_rates_df)

    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    enriched_file_path = PROCESSED_DATA_PATH / "sales_enriched.csv"
    enriched_sales_df.to_csv(enriched_file_path, index=False)

    print("\n=== TRANSFORMED SALES DATA ===")
    print(sales_df.head())
    print(f"\nShape: {sales_df.shape}")
    print("\nColumns:")
    print(list(sales_df.columns))

    print("\n=== ENRICHED SALES DATA ===")
    print(enriched_sales_df.head())
    print(f"\nShape: {enriched_sales_df.shape}")
    print(f"\nSaved enriched data to: {enriched_file_path}")


if __name__ == "__main__":
    main()
