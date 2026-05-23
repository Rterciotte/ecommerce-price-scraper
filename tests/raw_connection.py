import psycopg

conn = psycopg.connect(
    host="127.0.0.1",
    port=5432,
    database="ecommerce_scraper",
    user="admin",
    password="admin"
)

print("CONECTOU")

conn.close()