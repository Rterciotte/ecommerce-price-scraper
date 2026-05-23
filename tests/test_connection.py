import psycopg

conn = psycopg.connect(
    host="127.0.0.1",
    port=5432,
    dbname="ecommerce_scraper",
    user="admin",
    password="admin"
)

print("CONNECTED")
conn.close()