import os
import glob
import logging
from datetime import datetime
from dotenv import load_dotenv
import snowflake.connector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

load_dotenv()

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
    )

def parse_line(line: str):
    # Expected format: DATE	MAX_TEMP	MIN_TEMP	PRECIP
    parts = line.strip().split("\t")
    if len(parts) != 4:
        return None
    raw_date, max_t, min_t, precip = parts
    try:
        date_key = datetime.strptime(raw_date, "%Y%m%d").date()
    except ValueError:
        return None

    def to_int_or_none(v):
        i = int(v)
        return None if i == -9999 else i

    return date_key, to_int_or_none(max_t), to_int_or_none(min_t), to_int_or_none(precip)

def ingest_file(cur, file_path: str) -> int:
    station_id = os.path.splitext(os.path.basename(file_path))[0]
    inserted = 0
    logging.info(f"Processing file {file_path} for station {station_id}")

    rows = []
    with open(file_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parsed = parse_line(line)
            if not parsed:
                continue
            date_key, max_t, min_t, precip = parsed
            rows.append((station_id, date_key, max_t, min_t, precip, file_path))

    if not rows:
        return 0

    merge_sql = '''
        MERGE INTO WEATHER_DAILY_RAW t
        USING (
          SELECT
            %(station_id)s      AS STATION_ID,
            %(date_key)s        AS DATE_KEY,
            %(max_temp)s        AS MAX_TEMP_TENTHS,
            %(min_temp)s        AS MIN_TEMP_TENTHS,
            %(precip)s          AS PRECIP_TENTHS,
            %(file_name)s       AS FILE_NAME
        ) v
        ON t.STATION_ID = v.STATION_ID AND t.DATE_KEY = v.DATE_KEY
        WHEN MATCHED THEN UPDATE SET
            MAX_TEMP_TENTHS = v.MAX_TEMP_TENTHS,
            MIN_TEMP_TENTHS = v.MIN_TEMP_TENTHS,
            PRECIP_TENTHS   = v.PRECIP_TENTHS,
            FILE_NAME       = v.FILE_NAME
        WHEN NOT MATCHED THEN INSERT (STATION_ID, DATE_KEY,
                                      MAX_TEMP_TENTHS, MIN_TEMP_TENTHS,
                                      PRECIP_TENTHS, FILE_NAME)
        VALUES (v.STATION_ID, v.DATE_KEY, v.MAX_TEMP_TENTHS,
                v.MIN_TEMP_TENTHS, v.PRECIP_TENTHS, v.FILE_NAME)
    '''

    for (station_id, date_key, max_t, min_t, precip, file_name) in rows:
        params = {
            "station_id": station_id,
            "date_key": date_key,
            "max_temp": max_t,
            "min_temp": min_t,
            "precip": precip,
            "file_name": file_name,
        }
        cur.execute(merge_sql, params)
        inserted += 1

    return inserted

def main():
    wx_path = os.getenv("WX_DATA_PATH", "/app/data/wx_data")
    pattern = os.path.join(wx_path, "*.txt")
    files = glob.glob(pattern)

    if not files:
        logging.warning(f"No weather files found at {pattern}")
        return

    conn = get_snowflake_conn()
    cur = conn.cursor()

    total_records = 0
    start = datetime.utcnow()
    logging.info("Starting weather ingestion")

    try:
        for file_path in files:
            inserted = ingest_file(cur, file_path)
            total_records += inserted
        conn.commit()
    finally:
        cur.close()
        conn.close()

    end = datetime.utcnow()
    logging.info(
        f"Completed weather ingestion. Total records processed: {total_records}. "
        f"Start: {start.isoformat()} | End: {end.isoformat()}"
    )

if __name__ == "__main__":
    main()
