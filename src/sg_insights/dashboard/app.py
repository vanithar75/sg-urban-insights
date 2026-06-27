"""Singapore Urban Insights — LTA mobility dashboard (D2 MVP, LTA-only)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from sg_insights.config import MARTS_ROOT
from sg_insights.etl.lta_marts import build_marts


@st.cache_data
def load_marts(marts_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fact = pd.read_parquet(marts_dir / "facts" / "fact_bus_arrivals.parquet")
    dim_stop = pd.read_parquet(marts_dir / "dimensions" / "dim_bus_stop.parquet")
    dim_service = pd.read_parquet(marts_dir / "dimensions" / "dim_service.parquet")
    dim_time = pd.read_parquet(marts_dir / "dimensions" / "dim_time.parquet")
    return fact, dim_stop, dim_service, dim_time


def render_dashboard() -> None:
    st.set_page_config(page_title="SG Urban Insights", layout="wide")
    st.title("Singapore Urban Insights")
    st.caption(
        "Track B D2 · Mobility subject area · LTA Bus Arrival (D1 gold layer) · "
        "Open Government Licence"
    )

    marts_root = MARTS_ROOT
    fact_path = marts_root / "facts" / "fact_bus_arrivals.parquet"

    if not fact_path.is_file():
        st.warning("Marts not built yet. Running ETL from D1…")
        try:
            build_marts()
            st.success("ETL complete.")
        except FileNotFoundError as exc:
            st.error(str(exc))
            st.info(
                "Run D1 pipeline first: `python -m apac_data.pipelines.lta_bus_arrival --fixture` "
                "then `python -m sg_insights.etl.lta_marts`"
            )
            return

    fact, dim_stop, dim_service, dim_time = load_marts(marts_root)

    enriched = fact.merge(dim_stop, on="bus_stop_key", how="left")
    enriched = enriched.merge(dim_service, on="service_key", how="left")
    enriched = enriched.merge(dim_time, on="time_key", how="left")

    col1, col2, col3 = st.columns(3)
    col1.metric("Bus stops", dim_stop["bus_stop_key"].nunique())
    col2.metric("Services", dim_service["service_key"].nunique())
    col3.metric("Total arrivals", int(enriched["arrival_count"].sum()))

    st.subheader("Arrivals by hour of day")
    by_hour = enriched.groupby("hour_of_day", as_index=False)["arrival_count"].sum()
    st.bar_chart(by_hour.set_index("hour_of_day"))

    left, right = st.columns(2)
    with left:
        st.subheader("Top services")
        by_service = (
            enriched.groupby(["service_key", "operator"], as_index=False)["arrival_count"]
            .sum()
            .sort_values("arrival_count", ascending=False)
            .head(10)
        )
        st.dataframe(by_service, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Arrivals by bus stop")
        by_stop = (
            enriched.groupby(["bus_stop_key", "bus_stop_label"], as_index=False)["arrival_count"]
            .sum()
            .sort_values("arrival_count", ascending=False)
        )
        st.bar_chart(by_stop.set_index("bus_stop_label")["arrival_count"])

    st.subheader("Operator share")
    by_operator = enriched.groupby("operator", as_index=False)["arrival_count"].sum()
    st.bar_chart(by_operator.set_index("operator"))

    st.divider()
    st.caption(
        "Data: LTA DataMall Bus Arrival via "
        "[apac-data-foundation](https://github.com/vanithar75/apac-data-foundation). "
        "Singapore-only · No PII."
    )


def main() -> None:
    render_dashboard()


render_dashboard()
