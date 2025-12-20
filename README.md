# Corteva Weather Data Engineering Project  
**Tech Stack:** Snowflake • DBT • Python (Flask) • Docker • Medallion Architecture (Bronze → Silver → Gold)

---

## Project Overview

This project implements a complete end-to-end data engineering pipeline for ingesting, transforming, and serving weather data through a REST API.

It follows a **Medallion Architecture** using:

- **Bronze** → Raw ingestion into Snowflake  
- **Silver** → Cleaned, standardized, deduplicated data using dbt  
- **Gold** → Yearly aggregated curated tables  
- **Flask REST API** → Exposes both raw & aggregated data  
- **Docker** → Ensures consistent and reproducible execution  

The goal is to simulate a production-grade data pipeline.

---

## Architecture Diagram (Conceptual)

wx_data/*.txt → Ingestion Job (Python) → Snowflake RAW (Bronze)
↓
dbt Models
↓
RAW → SILVER (clean/unit convert/dedup) → GOLD (yearly aggregates)
↓
Flask REST API


---

## Features

### Ingestion Layer (Python → Snowflake)
- Reads raw weather `.txt` files
- Converts -9999 to NULL
- Parses dates & numeric fields
- Loads into `RAW.WEATHER_DAILY_RAW` using **MERGE → idempotent**
- Logs record counts and timestamps

---

### Transformations (dbt)
**Silver Layer**
- Deduplicates rows using window functions  
- Standardizes units (tenths → Celsius/mm)  
- Produces `stg_weather_daily` view  

**Gold Layer**
- Aggregates by station & year  
- Computes  
  - Average max temp  
  - Average min temp  
  - Total precipitation (converted to cm)  
- Materializes as `WEATHER_YEARLY_STATS` table  

---

### REST API (Flask)
Two endpoints:

| Endpoint | Description |
|---------|-------------|
| `/api/weather` | Raw daily weather data |
| `/api/weather/stats` | Yearly aggregated metrics |


## Snowflake Setup

Run the SQL scripts in `sql/` in order:

```sql
-- 1. Create database, schemas
!source sql/00_create_database_and_schema.sql

-- 2. Create raw and analytics tables
!source sql/01_weather_tables.sql
```

Or simply open each file and execute in Snowflake UI.

Tables created:

- `WEATHER_DB.RAW.WEATHER_DAILY_RAW`    (Bronze)
- `WEATHER_DB.ANALYTICS.WEATHER_YEARLY_STATS` (Gold – dbt materialization)

## Environment Variables

Copy `.env.example` to `.env` and fill in Snowflake credentials:

```bash
cp .env.example .env
```

`.env` variables are used by both the ingestion script and API containers.

## Ingestion – Bronze Layer

The ingestion job reads the raw `wx_data/*.txt` files and loads them into
`WEATHER_DB.RAW.WEATHER_DAILY_RAW` using MERGE (idempotent).

### Local run (no Docker)

```bash
cd ingestion
pip install -r requirements.txt
python ingest_weather.py
```

Make sure the following env vars are exported (from `.env`):

```bash
export $(grep -v '^#' ../.env | xargs)
```

Also ensure `WX_DATA_PATH` points to the directory where `*.txt` weather files live.

### Docker run

At project root:

```bash
docker-compose run --rm ingestion
```

This builds the ingestion image and runs it once, mounting the local `wx_data` folder
into the container at `/app/data/wx_data`.

## dbt – Bronze → Silver → Gold

Project is under `dbt_weather/`.

Models:

- `staging/stg_weather_daily.sql` – Silver:
  - Reads from `RAW.WEATHER_DAILY_RAW`
  - Handles NULLs and unit conversion
- `marts/fct_weather_yearly_stats.sql` – Gold:
  - Aggregates to yearly per station and writes to
    `WEATHER_DB.ANALYTICS.WEATHER_YEARLY_STATS`

### Configure dbt profiles

Copy `profiles.yml.example` to `~/.dbt/profiles.yml` (or adjust `DBT_PROFILES_DIR`):

```bash
mkdir -p ~/.dbt
cp dbt_weather/profiles.yml.example ~/.dbt/profiles.yml
```

Ensure the environment variables (`SNOWFLAKE_*`) are set.

### Run dbt

```bash
cd dbt_weather
dbt deps   # if you add packages later
dbt run
```

After this, you should see data in:

```sql
SELECT * FROM WEATHER_DB.ANALYTICS.WEATHER_YEARLY_STATS;
```

## Flask API – Serving the Data

The API exposes two main endpoints:

- `/api/weather` – daily weather records (Bronze table)
- `/api/weather/stats` – yearly aggregated stats (Gold table)

Swagger UI is available at `/apidocs`.

### Local run (no Docker)

```bash
cd api
pip install -r requirements.txt
export $(grep -v '^#' ../.env | xargs)
python app.py
```

Visit `http://localhost:5000/apidocs` in your browser.

### Docker / docker-compose

From project root:

```bash
docker-compose up --build api
```

API is available at `http://localhost:5000`.

## Medallion Architecture Mapping

- **Bronze**: `WEATHER_DB.RAW.WEATHER_DAILY_RAW`
- **Silver**: `dbt_weather.models.staging.stg_weather_daily` (view)
- **Gold**: `dbt_weather.models.marts.fct_weather_yearly_stats` (table)

In a real production setup, additional Silver/Gold models can be added to support more
use-cases (e.g., station-enriched facts, rolling windows, etc.).

## Notes

- This project is intentionally kept small and focused to fit in an interview assignment.
- For real workloads, you would likely:
  - Schedule ingestion and dbt jobs via Airflow/Cloud Composer/Prefect/etc.
  - Store environment secrets in a vault (AWS Secrets Manager, HashiCorp Vault, etc.).
  - Add unit tests and integration tests for both dbt and Flask.
