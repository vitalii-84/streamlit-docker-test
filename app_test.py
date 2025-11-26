import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

st.title("🧪 Тест Streamlit + PostgreSQL")

# Параметри підключення
DB_CONFIG = {
    'host': 'postgres',  # Ім'я сервісу з docker-compose.yml
    'database': 'your_database',
    'user': 'your_user',
    'password': 'your_password'
}

# Тест підключення до PostgreSQL
st.header("1️⃣ Перевірка PostgreSQL")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Версія PostgreSQL
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    st.success("✅ Підключення до PostgreSQL успішне!")
    st.code(version)
    
    # Створити тестову таблицю
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    
    # Додати тестові дані
    cur.execute("INSERT INTO test_table (name) VALUES ('Test 1'), ('Test 2'), ('Test 3');")
    conn.commit()
    
    # Отримати дані
    cur.execute("SELECT * FROM test_table;")
    rows = cur.fetchall()
    
    df = pd.DataFrame(rows, columns=['ID', 'Name', 'Created At'])
    st.dataframe(df)
    
    cur.close()
    conn.close()
    
except Exception as e:
    st.error(f"❌ Помилка підключення: {e}")

# Тест Streamlit функціоналу
st.header("2️⃣ Перевірка Streamlit")

st.write("Якщо ви бачите цей текст, Streamlit працює! 🎉")

# Інтерактивний віджет
name = st.text_input("Введіть своє ім'я:")
if name:
    st.write(f"Привіт, {name}! 👋")

# Графік
chart_data = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})
st.line_chart(chart_data.set_index('x'))

# SQL запит
st.header("3️⃣ Виконати SQL запит")
query = st.text_area("Введіть SQL запит:", "SELECT NOW();")

if st.button("Виконати"):
    try:
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )
        result = pd.read_sql(query, engine)
        st.dataframe(result)
    except Exception as e:
        st.error(f"Помилка: {e}")
