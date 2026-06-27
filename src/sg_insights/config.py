"""Paths to D1 lakehouse outputs and local mart storage."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

DEFAULT_D1_ROOT = REPO_ROOT.parent / "apac_data_foundation"


def d1_data_root() -> Path:
    raw = os.getenv("D1_DATA_ROOT", "").strip()
    return Path(raw) if raw else DEFAULT_D1_ROOT


def d1_gold_lta_hourly() -> Path:
    return d1_data_root() / "data" / "gold" / "sg" / "lta_bus_arrival" / "lta_bus_arrival_hourly.parquet"


def d1_silver_lta() -> Path:
    return d1_data_root() / "data" / "silver" / "sg" / "lta_bus_arrival" / "lta_bus_arrival.parquet"


MARTS_ROOT = REPO_ROOT / "data" / "marts"
FACT_BUS_ARRIVALS = MARTS_ROOT / "facts" / "fact_bus_arrivals.parquet"
DIM_BUS_STOP = MARTS_ROOT / "dimensions" / "dim_bus_stop.parquet"
DIM_SERVICE = MARTS_ROOT / "dimensions" / "dim_service.parquet"
DIM_TIME = MARTS_ROOT / "dimensions" / "dim_time.parquet"
