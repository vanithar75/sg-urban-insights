# Singapore Urban Insights Dashboard

**Track B D2** — Batch ETL and Streamlit dashboard over **D1 LTA Bus Arrival** data only (no NEA, SingStat, or IMD in this MVP).

Depends on [apac-data-foundation](https://github.com/vanithar75/apac-data-foundation) (D1) gold/silver layers.

## Architecture

```
D1 gold/silver (LTA)  →  ETL star schema  →  Streamlit dashboard
apac_data_foundation      sg_urban_insights     mobility KPIs
```

### Marts (mobility subject area)

| Mart | Source |
|------|--------|
| `fact_bus_arrivals` | D1 gold hourly counts |
| `dim_bus_stop` | Distinct stops |
| `dim_service` | Service + operator (D1 silver) |
| `dim_time` | Hour-of-day from arrival timestamps |

## Quick start

```bash
# 1. Ensure D1 has data (fixture or live)
cd ../apac_data_foundation
LTA_USE_FIXTURE=1 python -m apac_data.pipelines.lta_bus_arrival --fixture

# 2. Build marts and run dashboard
cd ../sg_urban_insights
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e .
python -m sg_insights.etl.lta_marts
streamlit run src/sg_insights/dashboard/app.py
```

Set `D1_DATA_ROOT` in `.env` if D1 is not a sibling folder.

## Deferred (full D2 charter)

- NEA weather / air quality marts
- SingStat demographics
- Public deploy (GitHub Pages / Vercel) — stretch

## License

Dashboard code: MIT (TBD). Data: Singapore Open Government Licence via LTA DataMall.
