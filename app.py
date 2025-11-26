import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

# Отримайте URL бази даних
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://your_user:your_password@localhost:5432/your_database')

# Функція підключення до БД
@st.cache_resource
def get_connection():
    engine = create_engine(DATABASE_URL)
    return engine

# Заголовок додатку
st.title("Streamlit + PostgreSQL у Codespace")

# Підключення до БД
try:
    engine = get_connection()
    
    # Приклад запиту
    query = st.text_area("Введіть SQL запит:", "SELECT version();")
    
    if st.button("Виконати"):
        df = pd.read_sql(query, engine)
        st.dataframe(df)
        
except Exception as e:
    st.error(f"Помилка підключення: {e}")
