"""Build star-schema marts from D1 LTA bus arrival layers (mobility subject area only)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from sg_insights.config import (
    DIM_BUS_STOP,
    DIM_SERVICE,
    DIM_TIME,
    FACT_BUS_ARRIVALS,
    MARTS_ROOT,
    d1_gold_lta_hourly,
    d1_silver_lta,
)


def _ensure_mart_dirs() -> None:
    for path in (MARTS_ROOT / "facts", MARTS_ROOT / "dimensions"):
        path.mkdir(parents=True, exist_ok=True)


def build_marts(
    gold_path: Path | None = None,
    silver_path: Path | None = None,
) -> dict[str, Path]:
    """Transform D1 LTA gold/silver into dashboard marts. Returns output paths."""
    gold_path = gold_path or d1_gold_lta_hourly()
    silver_path = silver_path or d1_silver_lta()

    if not gold_path.is_file():
        msg = f"D1 gold not found: {gold_path}. Run D1 pipeline or set D1_DATA_ROOT."
        raise FileNotFoundError(msg)
    if not silver_path.is_file():
        msg = f"D1 silver not found: {silver_path}. Run D1 pipeline or set D1_DATA_ROOT."
        raise FileNotFoundError(msg)

    gold = pd.read_parquet(gold_path)
    silver = pd.read_parquet(silver_path)

    _ensure_mart_dirs()

    fact = gold.rename(
        columns={
            "bus_stop_code": "bus_stop_key",
            "service_no": "service_key",
        }
    ).copy()
    fact["time_key"] = pd.to_datetime(fact["arrival_hour"], utc=True).dt.strftime("%Y%m%d%H")
    fact_path = FACT_BUS_ARRIVALS
    fact.to_parquet(fact_path, index=False)

    dim_bus_stop = (
        gold[["bus_stop_code"]]
        .drop_duplicates()
        .rename(columns={"bus_stop_code": "bus_stop_key"})
        .assign(bus_stop_label=lambda df: "Stop " + df["bus_stop_key"])
    )
    dim_bus_stop.to_parquet(DIM_BUS_STOP, index=False)

    dim_service = (
        silver[["service_no", "operator"]]
        .drop_duplicates(subset=["service_no"])
        .rename(columns={"service_no": "service_key"})
    )
    dim_service.to_parquet(DIM_SERVICE, index=False)

    hours = pd.to_datetime(gold["arrival_hour"], utc=True)
    dim_time = pd.DataFrame(
        {
            "time_key": hours.dt.strftime("%Y%m%d%H"),
            "arrival_hour": hours,
            "hour_of_day": hours.dt.hour,
            "ingest_date": gold["ingest_date"].values,
        }
    ).drop_duplicates(subset=["time_key"])
    dim_time.to_parquet(DIM_TIME, index=False)

    return {
        "fact_bus_arrivals": fact_path,
        "dim_bus_stop": DIM_BUS_STOP,
        "dim_service": DIM_SERVICE,
        "dim_time": DIM_TIME,
    }


def main() -> None:
    paths = build_marts()
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
