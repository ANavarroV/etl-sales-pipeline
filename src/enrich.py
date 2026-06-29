import pandas as pd


def enrich_sales_with_exchange_rates(
    sales_df: pd.DataFrame,
    exchange_rates_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join sales data with exchange rates and calculate amounts in USD and GBP.
    """
    sales = sales_df.copy()
    exchange_rates = exchange_rates_df.copy()

    sales["order_date"] = pd.to_datetime(sales["order_date"])
    exchange_rates["order_date"] = pd.to_datetime(exchange_rates["order_date"])

    enriched_df = sales.merge(exchange_rates, on="order_date", how="left")

    missing_rates = enriched_df[
        enriched_df[["exchange_rate_usd", "exchange_rate_gbp"]].isna().any(axis=1)
    ]
    if not missing_rates.empty:
        missing_dates = (
            missing_rates["order_date"].dt.date.astype(str).drop_duplicates().tolist()
        )
        raise ValueError(
            "Missing exchange rates for order dates: " + ", ".join(missing_dates)
        )

    enriched_df["total_amount_usd"] = (
        enriched_df["total_amount"] * enriched_df["exchange_rate_usd"]
    ).round(2)
    enriched_df["total_amount_gbp"] = (
        enriched_df["total_amount"] * enriched_df["exchange_rate_gbp"]
    ).round(2)

    return enriched_df
