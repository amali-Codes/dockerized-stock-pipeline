import os
import requests
import mysql.connector

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "stocks")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "userpass")

def fetch_stock_data(symbol="AAPL"):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY" \
          f"&symbol={symbol}&interval=5min&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        time_series = data.get("Time Series (5min)", {})
        rows = []
        for ts, values in time_series.items():
            rows.append((symbol,
                         float(values["1. open"]),
                         int(values["5. volume"]),
                         ts))
        return rows
    except Exception as e:
        print("Error fetching data:", e)
        return []

def store_to_db(rows):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        query = "INSERT INTO stock_data (symbol, price, volume, timestamp) VALUES (%s, %s, %s, %s)"
        cur.executemany(query, rows)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error storing data:", e)

if __name__ == "__main__":
    rows = fetch_stock_data()
    if rows:
        store_to_db(rows)
