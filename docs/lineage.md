# ETL lineage — LTA mobility marts

**Source:** [apac-data-foundation](https://github.com/vanithar75/apac-data-foundation) LTA bus arrival layers.

| Mart | Upstream input | Transform |
|------|----------------|-----------|
| fact_bus_arrivals | gold `lta_bus_arrival_hourly.parquet` | Rename keys, add time_key |
| dim_bus_stop | gold `bus_stop_code` | Distinct + label |
| dim_service | silver `service_no`, `operator` | Distinct services |
| dim_time | gold `arrival_hour` | Hour-of-day dimension |

**Region:** Singapore only.

**Hosted demo:** `sample_data/marts/` ships a small fixture-derived snapshot for Streamlit Cloud.
