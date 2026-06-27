# Singapore Urban Insights Dashboard

Batch ETL and Streamlit dashboard over **LTA Bus Arrival** data from [apac-data-foundation](https://github.com/vanithar75/apac-data-foundation).

## Live demo

**[Open dashboard](https://sg-urban-insights-2axfg7as5gjdmwmmbdmbsu.streamlit.app)**

Hosted on Streamlit Community Cloud (`streamlit_app.py`). Uses bundled sample marts in `sample_data/marts/` (no upstream repo required on Cloud).

## Architecture

```
apac-data-foundation (LTA gold/silver)  →  ETL star schema  →  Streamlit dashboard
```

### Marts (mobility)

| Mart | Source |
|------|--------|
| `fact_bus_arrivals` | Gold hourly counts |
| `dim_bus_stop` | Distinct stops |
| `dim_service` | Service + operator (silver) |
| `dim_time` | Hour-of-day dimension |

## Local development

```bash
# 1. Refresh upstream lakehouse data (optional)
cd ../apac_data_foundation
LTA_USE_FIXTURE=1 python -m apac_data.pipelines.lta_bus_arrival --fixture

# 2. Build marts and run dashboard
cd ../sg_urban_insights
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e .
python -m sg_insights.etl.lta_marts
streamlit run streamlit_app.py
```

Set `D1_DATA_ROOT` in `.env` if the lakehouse repo is not a sibling folder.

## Deferred

- NEA weather / air quality marts
- SingStat demographics
- REST API layer for chart data

## License

Dashboard code: MIT (TBD). Data: Singapore Open Government Licence via LTA DataMall.
