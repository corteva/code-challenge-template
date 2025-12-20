import os
from flask import Flask, request, jsonify
from flasgger import Swagger
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE", "WEATHER_DB"),
    )

def parse_pagination():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 50))
    page = max(page, 1)
    page_size = min(max(page_size, 1), 500)
    offset = (page - 1) * page_size
    return page, page_size, offset

@app.route("/api/weather", methods=["GET"])
def get_weather():
    """Daily weather records
    ---
    parameters:
      - in: query
        name: station_id
        schema:
          type: string
      - in: query
        name: date
        schema:
          type: string
          format: date
      - in: query
        name: page
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: integer
    responses:
      200:
        description: List of daily weather records
    """
    station_id = request.args.get("station_id")
    date = request.args.get("date")
    page, page_size, offset = parse_pagination()

    base_sql = '''
        SELECT STATION_ID, DATE_KEY, MAX_TEMP_TENTHS, MIN_TEMP_TENTHS,
               PRECIP_TENTHS
        FROM WEATHER_DB.RAW.WEATHER_DAILY_RAW
        WHERE 1=1
    '''
    params = []

    if station_id:
        base_sql += " AND STATION_ID = %s"
        params.append(station_id)

    if date:
        base_sql += " AND DATE_KEY = %s"
        params.append(date)

    base_sql += " ORDER BY STATION_ID, DATE_KEY LIMIT %s OFFSET %s"
    params.extend([page_size, offset])

    conn = get_snowflake_conn()
    cur = conn.cursor()
    try:
        cur.execute(base_sql, params)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    data = [
        {
            "station_id": r[0],
            "date": str(r[1]),
            "max_temp_tenths_c": r[2],
            "min_temp_tenths_c": r[3],
            "precip_tenths_mm": r[4],
        }
        for r in rows
    ]

    return jsonify({
        "page": page,
        "page_size": page_size,
        "results": data
    })

@app.route("/api/weather/stats", methods=["GET"])
def get_weather_stats():
    """Yearly weather statistics
    ---
    parameters:
      - in: query
        name: station_id
        schema:
          type: string
      - in: query
        name: year
        schema:
          type: integer
      - in: query
        name: page
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: integer
    responses:
      200:
        description: Aggregated yearly weather statistics
    """
    station_id = request.args.get("station_id")
    year = request.args.get("year")
    page, page_size, offset = parse_pagination()

    base_sql = '''
        SELECT STATION_ID, YEAR, AVG_MAX_TEMP_C, AVG_MIN_TEMP_C, TOTAL_PRECIP_CM
        FROM WEATHER_DB.ANALYTICS.WEATHER_YEARLY_STATS
        WHERE 1=1
    '''
    params = []

    if station_id:
        base_sql += " AND STATION_ID = %s"
        params.append(station_id)

    if year:
        base_sql += " AND YEAR = %s"
        params.append(int(year))

    base_sql += " ORDER BY STATION_ID, YEAR LIMIT %s OFFSET %s"
    params.extend([page_size, offset])

    conn = get_snowflake_conn()
    cur = conn.cursor()
    try:
        cur.execute(base_sql, params)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    data = [
        {
            "station_id": r[0],
            "year": int(r[1]),
            "avg_max_temp_c": float(r[2]) if r[2] is not None else None,
            "avg_min_temp_c": float(r[3]) if r[3] is not None else None,
            "total_precip_cm": float(r[4]) if r[4] is not None else None,
        }
        for r in rows
    ]

    return jsonify({
        "page": page,
        "page_size": page_size,
        "results": data
    })

@app.route("/apidocs")
def apidocs_redirect():
    return "Swagger UI available at /apidocs"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
