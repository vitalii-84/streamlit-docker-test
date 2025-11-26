import psycopg2

try:
    conn = psycopg2.connect(
        host="postgres",
        database="your_database",
        user="your_user",
        password="your_password"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("PostgreSQL version:")
    print(cur.fetchone())
    cur.close()
    conn.close()
    print("✅ З'єднання успішне!")
except Exception as e:
    print(f"❌ Помилка: {e}")
