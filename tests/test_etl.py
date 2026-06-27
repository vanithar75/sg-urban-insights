"""ETL tests using synthetic D1-shaped parquet."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from sg_insights.etl.lta_marts import build_marts


@pytest.fixture
def d1_layers(tmp_path: Path) -> tuple[Path, Path]:
    gold_dir = tmp_path / "gold"
    silver_dir = tmp_path / "silver"
    gold_dir.mkdir(parents=True)
    silver_dir.mkdir(parents=True)

    gold = pd.DataFrame(
        {
            "bus_stop_code": ["83139", "83139"],
            "service_no": ["15", "10"],
            "arrival_hour": pd.to_datetime(
                ["2026-06-27T02:00:00Z", "2026-06-27T03:00:00Z"],
                utc=True,
            ),
            "arrival_count": [2, 1],
            "ingest_date": [pd.Timestamp("2026-06-27").date()] * 2,
        }
    )
    silver = pd.DataFrame(
        {
            "bus_stop_code": ["83139"],
            "ingested_at_utc": pd.to_datetime(["2026-06-27T01:00:00Z"], utc=True),
            "service_no": ["15"],
            "operator": ["SBST"],
            "status": ["In Operation"],
            "arrival_sequence": [1],
            "estimated_arrival": pd.to_datetime(["2026-06-27T02:00:00Z"], utc=True),
            "origin_code": ["77009"],
            "destination_code": ["77009"],
            "latitude": [1.35],
            "longitude": [103.95],
            "load": ["SEA"],
        }
    )

    gold_path = gold_dir / "lta_bus_arrival_hourly.parquet"
    silver_path = silver_dir / "lta_bus_arrival.parquet"
    gold.to_parquet(gold_path, index=False)
    silver.to_parquet(silver_path, index=False)
    return gold_path, silver_path


def test_build_marts_creates_star_schema(
    d1_layers: tuple[Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gold_path, silver_path = d1_layers
    marts = tmp_path / "marts"
    monkeypatch.setattr("sg_insights.etl.lta_marts.MARTS_ROOT", marts)

    outputs = build_marts(gold_path=gold_path, silver_path=silver_path)

    assert outputs["fact_bus_arrivals"].is_file()
    fact = pd.read_parquet(outputs["fact_bus_arrivals"])
    assert len(fact) == 2
    assert "bus_stop_key" in fact.columns

    dim_service = pd.read_parquet(outputs["dim_service"])
    assert "operator" in dim_service.columns
