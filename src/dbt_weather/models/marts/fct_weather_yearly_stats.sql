{{ config(
    materialized='table',
    alias='WEATHER_YEARLY_STATS'
) }}

WITH daily AS (
    SELECT * FROM {{ ref('stg_weather_daily') }}
)

SELECT
    STATION_ID,
    YEAR,
    AVG(MAX_TEMP_C)                        AS AVG_MAX_TEMP_C,
    AVG(MIN_TEMP_C)                        AS AVG_MIN_TEMP_C,
    SUM(PRECIP_MM) / 10.0                  AS TOTAL_PRECIP_CM
FROM daily
GROUP BY STATION_ID, YEAR
ORDER BY STATION_ID, YEAR;
