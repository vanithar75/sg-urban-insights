# ETL lineage — D2 LTA mobility marts

**Source:** D1 `apac_data_foundation` LTA bus arrival layers only.

| Mart | D1 input | Transform |
|------|----------|-----------|
| fact_bus_arrivals | `data/gold/sg/lta_bus_arrival/lta_bus_arrival_hourly.parquet` | Rename keys, add time_key |
| dim_bus_stop | gold `bus_stop_code` | Distinct + label |
| dim_service | silver `service_no`, `operator` | Distinct services |
| dim_time | gold `arrival_hour` | Hour-of-day dimension |

**Region:** Singapore only (`sg`).
