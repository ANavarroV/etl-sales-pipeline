from __future__ import annotations

import json
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


API_BASE_URL = "https://api.frankfurter.app"


def fetch_exchange_rates(
    start_date: date,
    end_date: date,
    base_currency: str = "EUR",
    target_currencies: tuple[str, ...] = ("USD", "GBP"),
) -> pd.DataFrame:
    """
    Fetch exchange rates from Frankfurter API for the given date range.
    """
    if start_date > end_date:
        raise ValueError("start_date cannot be later than end_date")

    params = urlencode(
        {
            "from": base_currency,
            "to": ",".join(target_currencies),
        }
    )
    url = f"{API_BASE_URL}/{start_date.isoformat()}..{end_date.isoformat()}?{params}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "etl-sales-pipeline/1.0",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = _read_http_error(error)
        raise RuntimeError(
            f"Frankfurter API request failed with HTTP {error.code}: {message}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Could not connect to Frankfurter API: {error.reason}") from error

    rates = payload.get("rates")
    if not rates:
        raise RuntimeError("Frankfurter API returned no exchange rates")

    rows = []
    for rate_date, values in rates.items():
        row = {"order_date": pd.to_datetime(rate_date)}
        for currency in target_currencies:
            column_name = f"exchange_rate_{currency.lower()}"
            row[column_name] = values.get(currency)
        rows.append(row)

    exchange_rates_df = pd.DataFrame(rows).sort_values("order_date").reset_index(drop=True)
    exchange_rates_df = _fill_missing_calendar_dates(
        exchange_rates_df,
        start_date,
        end_date,
    )

    missing_columns = [
        f"exchange_rate_{currency.lower()}"
        for currency in target_currencies
        if f"exchange_rate_{currency.lower()}" not in exchange_rates_df
        or exchange_rates_df[f"exchange_rate_{currency.lower()}"].isna().any()
    ]
    if missing_columns:
        raise RuntimeError(
            "Frankfurter API response is missing rates for: "
            + ", ".join(missing_columns)
        )

    return exchange_rates_df


def _fill_missing_calendar_dates(
    exchange_rates_df: pd.DataFrame,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    calendar_df = pd.DataFrame(
        {"order_date": pd.date_range(start=start_date, end=end_date)}
    )

    exchange_rates_df = (
        pd.concat([exchange_rates_df, calendar_df], ignore_index=True)
        .sort_values("order_date", kind="mergesort")
        .drop_duplicates(subset=["order_date"], keep="first")
        .ffill()
        .reset_index(drop=True)
    )
    exchange_rates_df = exchange_rates_df[
        (exchange_rates_df["order_date"].dt.date >= start_date)
        & (exchange_rates_df["order_date"].dt.date <= end_date)
    ].reset_index(drop=True)

    return exchange_rates_df


def _read_http_error(error: HTTPError) -> str:
    try:
        body = error.read().decode("utf-8")
        payload = json.loads(body)
        return payload.get("message", body)
    except Exception:
        return error.reason
